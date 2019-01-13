from flask import render_template, jsonify, Blueprint
from flask_login import current_user

# from yolo.models import User, Photo, Notification
from yolo.notifications import push_collect_notification, push_follow_notification

ajax_bp = Blueprint('ajax', __name__)


@ajax_bp.route('/notifications-count')
def notifications_count():
    pass


@ajax_bp.route('/profile/<int:user_id>')
def get_profile(user_id):
    pass


@ajax_bp.route('/followers-count/<int:user_id>')
def followers_count(user_id):
    pass


@ajax_bp.route('/<int:photo_id>/followers-count')
def collectors_count(photo_id):
    pass


@ajax_bp.route('/collect/<int:photo_id>', methods=['POST'])
def collect(photo_id):
    pass


@ajax_bp.route('/uncollect/<int:photo_id>', methods=['POST'])
def uncollect(photo_id):
    pass


@ajax_bp.route('/follow/<username>', methods=['POST'])
def follow(username):
    pass


@ajax_bp.route('/unfollow/<username>', methods=['POST'])
def unfollow(username):
    pass
