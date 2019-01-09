import os
from flask import Blueprint, render_template, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from flask_dropzone import random_filename
from yolo.decorators import confirm_required, permission_required
from yolo.models import Photo
from yolo.extentions import db

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
	return render_template("main/index.html")


@main_bp.route("/upload", methods=["POST", "GET"])
@login_required
@confirm_required
@permission_required("UPLOAD")
def upload():
	if request.method == "POST" and 'file' in request.files:
		f = request.files.get("file")
		filename = random_filename(f.filename)
		f.save(os.path.join(current_app.config['YOLO_UPLOAD_PATH'], filename))

		photo = Photo(
			filename = filename,
			its_author = current_user._get_current_object()
		)
		db.session.add(photo)
		db.session.commit()
	return render_template("main/upload.html")


@main_bp.route("/explore")
def explore():
	pass


@main_bp.route("/search")
def search():
	pass

