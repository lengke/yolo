import os
import click
from flask import Flask
from yolo.blueprints.admin import admin_bp
from yolo.blueprints.ajax import ajax_bp
from yolo.blueprints.main import main_bp
from yolo.blueprints.user import user_bp
from yolo.blueprints.auth import auth_bp
from yolo.extentions import *
from yolo.settings import config
from yolo.models import Role


# 工厂函数
def create_app(config_name=None):
	if config_name == None:
		config_name = os.getenv("FLASK_ENV", "development")

	app = Flask("yolo")
	app.config.from_object(config[config_name])
	print("**** the Current Config is:" + config_name +" ****")

	register_blueprints(app)
	register_extensions(app)
	register_commands(app)

	return app


# 将5个蓝图注册到App上面
def register_blueprints(app):
	app.register_blueprint(main_bp)
	app.register_blueprint(admin_bp, url_prefix="/admin")
	app.register_blueprint(ajax_bp, url_prefix="/ajax")
	app.register_blueprint(user_bp, url_prefix="/user")
	app.register_blueprint(auth_bp, url_prefix="/auth")


# 将所有的拓展对象注册到App上面
def register_extensions(app):
	bootstrap.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)
	moment.init_app(app)
	avatars.init_app(app)
	dropzone.init_app(app)
	csrf.init_app(app)
	whooshee.init_app(app)


# 注册click命令行命令
def register_commands(app):

	# 初始化命令
	@app.cli.command()
	def init():
		click.echo("初始化数据库")
		# db.drop_all()
		db.create_all()
		click.echo("初始化角色和权限表")
		Role.init_role()
		click.echo("初始化完成")

