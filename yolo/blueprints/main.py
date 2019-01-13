import os
from flask import Blueprint, render_template, redirect, url_for, request, current_app, send_from_directory
from flask_login import login_required, current_user
from flask_dropzone import random_filename
from yolo.decorators import confirm_required, permission_required
from yolo.models import Photo
from yolo.extentions import db
from yolo.utils import resize_image

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
	return render_template("main/index.html")


@main_bp.route("/upload", methods=["POST", "GET"])
@login_required
@confirm_required
@permission_required("UPLOAD")
def upload():
	"""
	处理用户上传图片，生成多个尺寸，保存文件到uploads目录，保存文件名到数据库
	:return: 仍在本页面
	"""
	if request.method == "POST" and 'file' in request.files:
		f = request.files.get("file")
		filename = random_filename(f.filename)
		f.save(os.path.join(current_app.config['YOLO_UPLOAD_PATH'], filename))
		filename_s = resize_image(f, filename, current_app.config["YOLO_PHOTO_SIZE"]["small"])
		filename_m = resize_image(f, filename, current_app.config["YOLO_PHOTO_SIZE"]["medium"])
		photo = Photo(
			filename = filename,
			filename_s = filename_s,
			filename_m = filename_m,
			its_author = current_user._get_current_object()
		)
		db.session.add(photo)
		db.session.commit()
	return render_template("main/upload.html")


@main_bp.route("/uploads/<path:filename>")
def get_image(filename):
	"""
	获取指定图片用于展示
	:param filename:根据情况使用_s, _m, _l来指定尺寸
	:return: 指定的图片文件
	"""
	return send_from_directory(current_app.config["YOLO_UPLOAD_PATH"], filename)


# 获取用户头像用于展示
@main_bp.route("/avatars/<path:filename>")
def get_avatar(filename):
	"""
	获取指定用户头像用于展示
	:param filename:根据情况使用_s, _m, _l来指定尺寸
	:return: 指定的头像文件
	"""
	return send_from_directory(current_app.config["AVATARS_SAVE_PATH"], filename)


@main_bp.route("/explore")
def explore():
	pass


@main_bp.route("/search")
def search():
	pass


@main_bp.route('/notifications')
@login_required
def show_notifications():
	pass


@main_bp.route('/notification/read/<int:notification_id>', methods=['POST'])
@login_required
def read_notification(notification_id):
	pass


@main_bp.route('/notifications/read/all', methods=['POST'])
@login_required
def read_all_notification():
	pass


@main_bp.route('/photo/<int:photo_id>')
def show_photo(photo_id):
	pass


@main_bp.route('/photo/n/<int:photo_id>')
def photo_next(photo_id):
	pass


@main_bp.route('/photo/p/<int:photo_id>')
def photo_previous(photo_id):
	pass








