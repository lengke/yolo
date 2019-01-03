from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, AnonymousUserMixin
from flask_mail import Mail
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_avatars import Avatars
from flask_dropzone import Dropzone
from flask_whooshee import Whooshee
from flask_wtf import CSRFProtect


bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
moment = Moment()
avatars = Avatars()
dropzone = Dropzone()
csrf = CSRFProtect()
whooshee = Whooshee()


login_manager.login_view = 'auth.login'
# login_manager.login_message = 'Your custom message'
login_manager.login_message_category = 'warning'

login_manager.refresh_view = 'auth.re_authenticate'
# login_manager.needs_refresh_message = 'Your custom message'
login_manager.needs_refresh_message_category = 'warning'



@login_manager.user_loader
def load_user(user_id):
	from yolo.models import User
	user = User.query.get(int(user_id))
	return user