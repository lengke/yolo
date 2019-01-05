from flask import Blueprint, render_template, url_for, redirect, flash
from yolo.forms.auth import RegisterForm, LoginForm
from yolo.models import User
from yolo.extentions import db
from yolo.utils import validate_token, generate_token
from yolo.settings import Operations
from flask_login import login_required, current_user, login_user
from yolo.emails import send_confirm_email

auth_bp = Blueprint("auth", __name__)


# 新用户注册
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
	# db.drop_all()
	db.create_all()
	if current_user.is_authenticated:
		return redirect(url_for("main.index"))

	form = RegisterForm()
	if form.validate_on_submit():
		nickname = form.nickname.data
		email = form.email.data.lower() #防止用户用相同邮箱的大小写地址来作弊，全部视为小写处理
		username = form.username.data
		password = form.password.data
		user = User(username=username, nickname=nickname, email=email)
		user.set_password(password)
		db.session.add(user)
		db.session.commit()

		# 注册成功，写入数据库的同时
		# 生成确认邮箱的token并发email
		token = generate_token(user=user, operation=Operations.CONFIRM)
		send_confirm_email(user=user, token=token)
		flash("验证邮件已发送,请务必先在本页面登录后再进入邮箱点击确认链接", "info")
		return redirect(url_for("auth.login"))
	return render_template("auth/register.html", form=form)


# 验证用户token
@auth_bp.route("/confirm/<token>", methods=["GET"])
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for("main.index"))

	if validate_token(user=current_user, token=token, operation=Operations.CONFIRM):
		flash("账户确认成功", "success")
		return redirect(url_for("main.index"))
	else:
		flash("账户确认失败", "danger")
		return redirect(url_for("auth.resend_confirm_mail"))


# 重新发送确认邮件
@auth_bp.route("/resend-confirm-email")
@login_required
def resend_confirm_email():
	if current_user.confirmed:
		return redirect(url_for("main.index"))

	token = generate_token(user=current_user, operation=Operations.CONFIRM)
	send_confirm_email(user=current_user, token=token)
	flash("已重新发送验证邮件到您的邮箱", "info")
	return redirect(url_for("main.index"))


@auth_bp.route("/login", methods=["POST", "GET"])
def login():
	if current_user.is_authenticated:
		flash("请勿重复登录", "info")
		return redirect(url_for("main.index"))

	form = LoginForm()
	if form.validate_on_submit():
		username = form.username.data
		remember = form.remember.data
		user = User.query.filter_by(username = username).first()
		password = form.password.data
		if user is not None and user.validate_password(password):
			if login_user(user, remember=remember):
				flash("登录成功", "success")
				return redirect(url_for("main.index"))
			else:
				flash("账号被锁，暂时无法登录", "warning")
				return redirect(url_for("main.index"))
		flash("登录失败", "warning")
	return render_template("auth/login.html", form=form)


