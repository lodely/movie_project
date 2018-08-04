#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from contextlib import contextmanager
from flask import flash, Flask
from app import app


from flask_script import Manager # flask脚本
from flask_migrate import Migrate, MigrateCommand #flask迁移数据

from flask_login import UserMixin

# 提交数据，若出错自动回滚
class SQLAlchemy(_SQLAlchemy):

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
            flash("数据库保存", "ok")
        except Exception as e:
            db.session.rollback()
            flash("数据库保存", "err")
            raise e

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+cymysql://root:root@localhost:3306/movie_project'
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db) # 传入两个对象，一个是app，另一个是SQLAlchemy对象
manager = Manager(app)
manager.add_command('db', MigrateCommand) #给manager添加一个db命令并且传入一个MigrateCommand的类

class Base(db.Model):
    __abstract__ = True
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 登录时间

    @classmethod
    def get_ten_page(cls, page):
        datas = cls.query.paginate(page=page, per_page=10)
        return datas


# 会员模型
class Users(Base, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100, collation='utf8_bin'), unique=True) # 昵称
    pwd = db.Column(db.String(100)) # 密码
    phone = db.Column(db.String(11), unique=True) # 电话
    email = db.Column(db.String(100, collation='utf8_bin'), unique=True) # 邮箱
    info = db.Column(db.Text)   # 个性简介
    face = db.Column(db.String(255), unique=True)   # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 注册时间
    uuid = db.Column(db.String(255), unique=True)   # 唯一标识符
    userlogs = db.relationship("UserLog", backref='user')   # 会员日志外键关联
    comments = db.relationship("Comment", backref='user')   # 评论外键关联
    moviecols = db.relationship("Moviecol", backref='user')   # 收藏外键关联
    status = db.Column(db.SmallInteger, default=1) # 状态为1正常，0冻结

    def __repr__(self):
        return '<Users %r>' % self.nickname

    @classmethod
    def get_all_user(cls):
        all_users = Users.query.all()
        return all_users

    # 验证密码
    def check_pwd(self, pwd):
        # 验证密码
        from werkzeug.security import check_password_hash
        # 相同返回True，不同返回False
        return check_password_hash(self.pwd, pwd)

    @property
    def password(self):
        return self.pwd

    # 密码加密
    @password.setter
    def password(self, pwd):
        from werkzeug.security import generate_password_hash
        self.pwd = generate_password_hash(pwd)



# 会员登录日志
class UserLog(Base):
    __tablename__ = 'userlog'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 登录时间

    def __repr__(self):
        return '<UserLog %r>' % self.id

    @classmethod
    def get_log(cls, uid):
        # 查询用户最后登录的十次时间
        datas = cls.query.filter_by(user_id=uid).order_by(cls.addtime.desc()).limit(10).all()
        return datas

# 标签模型
class Tags(Base):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)    # 标题
    moives = db.relationship("Movie", backref='tag')
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Tags %r>' % self.name


    @classmethod
    def get_all_tags(cls):
        # 查询所有标签

        """方法一"""
        # tags = []
        # data = Tags.query.all()
        # for value in data:
            # tag = (str(value.id), value.name)
            # tags.append(tag)

        """方法二"""
        tags = [(str(value.id), value.name) for value in Tags.query.all()]
        return tags

# 电影
class Movie(Base):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)  # 电影名
    url = db.Column(db.String(255), unique=True)
    logo = db.Column(db.String(255), unique=True)   # 封面
    info = db.Column(db.Text)   # 简介
    star = db.Column(db.SmallInteger)   # 星级
    playnum = db.Column(db.BigInteger, default=0)  # 播放量
    commentnum = db.Column(db.BigInteger, default=0)   # 评论量
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id')) # 所属标签
    area = db.Column(db.String(255))    # 上映地区
    release_time = db.Column(db.Date)   # 上映时间
    length = db.Column(db.String(100))  # 播放时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 添加时间
    comments = db.relationship("Comment", backref='movie')  # 评论外键关联
    moviecols = db.relationship("Moviecol", backref='movie')   #收藏外键关联

    def __repr__(self):
        return '<Movie %r>' % self.title


# 上映预告
class Preview(Base):
    __tablename__ = 'preview'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)  # 电影名
    logo = db.Column(db.String(255), unique=True)   # 封面
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 添加时间

    def __repr__(self):
        return '<Preview %r>' % self.title


# 评论
class Comment(Base):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id')) # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) # 所属会员
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 添加时间

    def __repr__(self):
        return '<Comment %r>' % self.id

    @classmethod
    def get_ten_commets(cls, page, uid):
        datas = cls.query.filter_by(user_id=uid).paginate(page=page, per_page=10)
        return datas


# 电影收藏
class Moviecol(Base):
    __tablename__ = 'moviecol'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id')) # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) # 所属会员
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 添加时间

    def __repr__(self):
        return '<Moviecol %r>' % self.id

    @classmethod
    def get_ten_moviecols(cls, page, uid):
        datas = cls.query.filter_by(user_id=uid).paginate(page=page, per_page=10)
        return datas


# 权限
class Auth(Base):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 添加时间

    def __repr__(self):
        return '<Auth %r>' % self.name

# 角色
class Role(Base):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    auths = db.Column(db.String(600))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 添加时间
    admin_id = db.relationship("Admin", backref='role') # 管理员外键关联

    def __repr__(self):
        return '<Auth %r>' % self.name

    @classmethod
    def get_all_roles(cls):
        roles = [(str(value.id), value.name) for value in cls.query.all()]
        return roles

# 管理员模型
class Admin(Base):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    # 添加collation='utf8_bin'，该字段大小写敏感
    name = db.Column(db.String(100, collation='utf8_bin'), unique=True)
    pwd = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 添加时间
    is_super = db.Column(db.SmallInteger) # 是否是超级管理员， 0为超级管理员
    role_id = db.Column(db.Integer, db.ForeignKey('role.id')) # 所属角色
    adminlogs = db.relationship("AdminLog", backref='admin')    #管理员登录日志外键关联
    oplogs = db.relationship("OpLog", backref='admin')  # 管理员操作日志外键关联

    def __repr__(self):
        return '<Admin %r>' % self.name

    # 验证密码
    def check_pwd(self, pwd):
        # 验证密码
        from werkzeug.security import check_password_hash
        # 相同返回True，不同返回False
        return check_password_hash(self.pwd, pwd)
    #     if self.pwd == pwd:
    #         return True
    #     else:
    #         return False

    @property
    def password(self):
        return self.pwd

    # 密码加密
    @password.setter
    def password(self, pwd):
        from werkzeug.security import generate_password_hash
        self.pwd = generate_password_hash(pwd)


# 管理员登录日志模型
class AdminLog(Base):
    __tablename__ = 'adminlog'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id')) # 所属管理员
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 登录时间

    def __repr__(self):
        return '<AdminLog %r>' % self.id

# 管理员操作日志模型
class OpLog(Base):
    __tablename__ = 'oplog'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id')) # 所属管理员
    ip = db.Column(db.String(100))
    reason = db.Column(db.String(600)) # 操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 操作时间

    def __repr__(self):
        return '<OpLog %r>' % self.id

from app import login_manager
# 必须要定义该函数传入用户id，以便重载时调用
@login_manager.user_loader
def get_user(uid):
    return Users.query.get(int(uid))


# if __name__ == "__main__":
#     # db.drop_all()
#     db.create_all()
#     from werkzeug.security import generate_password_hash
#     pwd = generate_password_hash("adminadmin")
#     role = Role(name='ROLE')
#     admin = Admin(name='admin', pwd=pwd, is_super=0, role_id=1)
#     db.session.add_all([admin, role])
#     db.session.commit()