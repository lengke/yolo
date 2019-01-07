from flask import current_app, render_template
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired

from yolo.extentions import db
from yolo.settings import Operations
from yolo.models import User


def generate_token(user, operation, expire_in=None, **kwargs):
	s = Serializer(current_app.config["SECRET_KEY"], expire_in)

	data = {"id":user.id, "operation": operation}
	data.update(**kwargs)
	return s.dumps(data)  # 这个dumps是Serializer对象的内置方法


def validate_token(user, token, operation, new_password=None):
	s = Serializer(current_app.config["SECRET_KEY"])

	try:
		data = s.loads(token)
	except (SignatureExpired, BadSignature):
		return False

	if operation != data.get("operation") or user.id != data.get("id"):
		return False

	if operation == Operations.CONFIRM:
		user.confirmed = True

	elif operation == Operations.RESET_PASSWORD:
		user.set_password(new_password)

	else:
		return False

	db.session.commit()
	return True






