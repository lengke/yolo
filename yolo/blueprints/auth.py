from flask import Blueprint, render_template, url_for, redirect, flash, request
from yolo.forms.auth import RegisterForm, LoginForm, ForgetPasswordForm, ResetPasswordForm
from yolo.models import User
from yolo.extentions import db
from yolo.utils import validate_token, generate_token
from yolo.settings import Operations
from flask_login import login_required, current_user, login_user, logout_user
from yolo.emails import send_confirm_email, send_reset_password_email

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


# 用户登录
@auth_bp.route("/login", methods=["POST", "GET"])
def login():
	if current_user.is_authenticated:
		flash("请勿重复登录", "info")
		return redirect(url_for("main.index"))

	form = LoginForm()
	if form.validate_on_submit():
		email = form.email.data.lower()
		remember = form.remember.data
		user = User.query.filter_by(email=email).first()
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


# 用户退出登录
@auth_bp.route("/logout")
@login_required
def logout():
	logout_user()
	flash("您已退出登录", "success")
	return redirect(url_for("main.index"))


# 忘记密码
@auth_bp.route("/forget-password", methods=["POST","GET"])
def forget_password():
	if current_user.is_authenticated:
		flash("您已登录", "info")
		return redirect(url_for("main.index"))

	form = ForgetPasswordForm()
	if form.validate_on_submit():
		email = form.email.data.lower()
		user = User.query.filter_by(email=email).first()
		if user:
			token = generate_token(user=user, operation=Operations.RESET_PASSWORD)
			send_reset_password_email(user=user, token=token)
			flash("重置密码邮件已发，请进入邮箱点击确认链接", "info")
			return redirect(url_for("auth.login"))
		else:
			flash("未查到该邮箱有注册用户，请确认地址无误", "warning")
			return redirect(url_for("auth.forget_password"))

	return render_template("auth/forget_password.html", form=form)


@auth_bp.route("/reset-password/<token>", methods=["POST","GET"])
def reset_password(token):
	if current_user.is_authenticated:
		flash("您已登录", "info")
		return redirect(url_for("main.index"))

	form = ResetPasswordForm()
	if form.validate_on_submit():
		email = form.email.data.lower()
		user = User.query.filter_by(email=email).first()
		new_password = form.password.data
		if user is None:
			flash("邮箱地址错误,请重新输入", "warning")
			return redirect(url_for("auth.reset_password"))

		if validate_token(user=user, token=token, operation=Operations.RESET_PASSWORD, new_password=new_password):
			flash("密码已更新，请重新登录", "success")
			return redirect(url_for("auth.login"))

	return render_template("auth/reset_password.html", form=form)






