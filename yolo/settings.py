import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Operations:
	CONFIRM = "confirm"
	RESET_PASSWORD = "reset-password"
	CHANGE_EMAIL = "change-email"


class BaseConfig():

	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = os.getenv("SECRET_KEY", "itisTseOcrPETyCantGuESs")

	YOLO_ADMIN_EMAIL = "20167591@qq.com"
	YOLO_MAIL_SUBJECT_PREFIX = "【YOLO】"

	CKEDITOR_SERVE_LOCAL = True
	MAIL_SERVER = "smtp.qq.com"
	MAIL_SUPPRESS_SEND = False
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USE_TLS = False
	MAIL_USERNAME = "20167591@qq.com"
	MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
	MAIL_DEFAULT_SENDER = ("20167591@qq.com")

	BOOTSTRAP_SERVE_LOCAL = True

	YOLO_UPLOAD_PATH = os.path.join(basedir, "uploads")
	YOLO_PHOTO_SIZE = {"small":400, "medium":800}
	YOLO_PHOTO_SUFFIX = {
		YOLO_PHOTO_SIZE["small"]: "_s",
		YOLO_PHOTO_SIZE["medium"]:"_m"
	}


	# flask-dropzone的配置
	DROPZONE_ALLOWED_FILE_TYPE = 'image'
	MAX_CONTENT_LENGTH = 3 * 1024 * 1024
	DROPZONE_MAX_FILE_SIZE = 3
	DROPZONE_MAX_FILES = 30
	DROPZONE_ENABLE_CSRF = True


class DevelopmentConfig(BaseConfig):
	SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI_DEV")


class ProductionConfig(BaseConfig):
	SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI_PRO")


config = {
	"development": DevelopmentConfig,
	"production": ProductionConfig
}