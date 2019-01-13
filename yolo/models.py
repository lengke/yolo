from yolo.extentions import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_avatars import Identicon


# 用户表
class User(db.Model, UserMixin):
	# 重写init方法，为用户自动分配角色
	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)
		self.set_role()
		self.generate_avatar()

	def __str__(self):
		return "<Name={} & Class 'yolo.models.User'>".format(self.username)

	id = db.Column(db.Integer, primary_key=True)
	# 用户基本资料
	username = db.Column(db.String(20), unique=True, index=True)  #这个字段是用户的独特身份标识
	email = db.Column(db.String(254), unique=True, index=True)
	password_hash = db.Column(db.String(128))
	nickname = db.Column(db.String(30))   #这个字段可以重复，不是身份标识
	website = db.Column(db.String(255))
	bio = db.Column(db.String(120))
	location = db.Column(db.String(50))
	member_since = db.Column(db.DateTime, default=datetime.utcnow)
	confirmed = db.Column(db.Boolean, default=False)
	# 用户头像
	avator_s = db.Column(db.String(64))
	avator_m = db.Column(db.String(64))
	avator_l = db.Column(db.String(64))
	avator_raw = db.Column(db.String(64))

	def generate_avatar(self):
		avatar = Identicon()
		filenames = avatar.generate(text=self.username)
		self.avator_s = filenames[0]
		self.avator_m = filenames[1]
		self.avator_l = filenames[2]
		db.session.commit()

	# 生成用户密码hash值
	def set_password(self,password):
		self.password_hash = generate_password_hash(password)

	# 校验用户密码
	def validate_password(self, password):
		return check_password_hash(self.password_hash, password)

	# User与Role的一对多关系属性，以及外键定义
	role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
	its_role = db.relationship("Role", back_populates="its_users")

	#用户与图片的一对多关系定义
	its_photos = db.relationship("Photo", back_populates="its_author", cascade="all")

	# 为每个user自动设置角色
	# 根据邮箱地址判断是否管理员
	def set_role(self):
		if self.its_role is None:
			if self.email == current_app.config["YOLO_ADMIN_EMAIL"]:
				self.its_role = Role.query.filter_by(name="Administrator").first()
			else:
				self.its_role = Role.query.filter_by(name="User").first()
			db.session.commit()

	# 判断用户是否是管理员
	@property
	def is_admin(self):
		return self.its_role.name == "Administrator"

	# 判断用户是否具有某项权限
	def can(self, permission_name):
		permission = Permission.query.filter_by(name=permission_name).first()
		return permission is not None and self.its_role is not None and permission in self.its_role.its_permissions


# 角色与权限多对多关系的关联表
# 注意这张表要放在Role和Permission表前面
# 因为后两张表要引用它

# 角色和权限的多对多关系关联表
roles_permissions = db.Table(
	"roles_permissions",
	db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
	db.Column("permission_id", db.Integer, db.ForeignKey("permission.id"))
	)

# 角色表
class Role(db.Model):

	def __str__(self):
		return "<Name={} & Class 'yolo.models.Role'>".format(self.name)

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), unique=True)

	its_permissions = db.relationship("Permission", secondary=roles_permissions, back_populates="its_roles")
	its_users = db.relationship("User", back_populates="its_role")

	# 初始化角色和权限两张表的内容
	@staticmethod
	def init_role():
		roles_permissions_map = {
		"Locked":["FOLLOW", "COLLECT"],
		"User":["FOLLOW", "COLLECT","COMMENT", "UPLOAD"],
		"Moderator":["FOLLOW", "COLLECT","COMMENT", "UPLOAD", "MODERATE"],
		"Administrator":["FOLLOW", "COLLECT","COMMENT", "UPLOAD", "MODERATE", "ADMINISTER"]
		}
		for role_name in roles_permissions_map:
			role = Role.query.filter_by(name=role_name).first()
			if role is None:
				role = Role(name=role_name)
				db.session.add(role)
			role.its_permissions = []
			for permission_name in roles_permissions_map[role_name]:
				permission = Permission.query.filter_by(name=permission_name).first()
				if permission is None:
					permission = Permission(name = permission_name)
					db.session.add(permission)
				role.its_permissions.append(permission)
			db.session.commit()


# 权限表
class Permission(db.Model):

	def __str__(self):
		return "<Name={} & Class 'yolo.models.Permission'>".format(self.name)

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), unique=True)

	its_roles = db.relationship("Role", secondary=roles_permissions, back_populates="its_permissions")

# 图片表
class Photo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(500))
	filename = db.Column(db.String(64))
	filename_s = db.Column(db.String(64))
	filename_m = db.Column(db.String(64))
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)
	authod_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	# 用户与图片的一对多关系定义
	its_author = db.relationship('User', back_populates="its_photos")

