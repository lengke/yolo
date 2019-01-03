from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp
from wtforms import ValidationError
from yolo.models import User


class RegisterForm(FlaskForm):
	nickname = StringField("昵称", validators=[DataRequired(), Length(1,50)])
	email = StringField("邮箱地址", validators=[DataRequired(),Email(), Length(1,128)])
	username = StringField(
		"用户名",
		validators=[DataRequired(), Length(1,20), Regexp('^[a-zA-Z0-9]*$', message="用户名只能由大小写字母或数字组成")]
	)
	password = PasswordField("密码", validators=[DataRequired(), Length(6,128), EqualTo("password2")])
	password2 = PasswordField("确认密码", validators=[DataRequired()])
	submit = SubmitField()

	# 验证邮箱是否重复
	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError("邮箱已被注册，换一个试试")

	# 验证用户名是否重复
	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError("用户名已被注册，换一个试试")

