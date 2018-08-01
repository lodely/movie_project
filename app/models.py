#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from contextlib import contextmanager
from flask import flash

from . import app

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

db = SQLAlchemy(app)

# 会员模型
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    phone = db.Column(db.String(11), unique=True)
    email = db.Column(db.String(100), unique=True)
    info = db.Column(db.Text)   # 个性简介
    face = db.Column(db.String(255), unique=True)   # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   #注册时间
    uuid = db.Column(db.String(255), unique=True)   # 唯一标识符
    userlogs = db.relationship("UserLog", backref='user')   #会员日志外键关联
    comments = db.relationship("Comment", backref='user')   #评论外键关联
    moviecols = db.relationship("Moviecol", backref='user')   #收藏外键关联

    def __repr__(self):
        return '<Users %r>' % self.nickname

# 会员登录日志
class UserLog(db.Model):
    __tablename__ = 'userlog'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 登录时间

    def __repr__(self):
        return '<UserLog %r>' % self.id

# 标签模型
class Tags(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)    # 标题
    moives = db.relationship("Movie", backref='tag')
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Tags %r>' % self.name

    @classmethod
    def get_ten_tags(cls, page):
        # 每页查询10条
        tags = Tags.query.paginate(page=page, per_page=10)
        return tags

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
class Movie(db.Model):
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

    @classmethod
    def get_ten_movies(cls, page):
        # 每页查询10条
        movies = Movie.query.paginate(page=page, per_page=10)
        return movies

# 上映预告
class Preview(db.Model):
    __tablename__ = 'preview'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)  # 电影名
    logo = db.Column(db.String(255), unique=True)   # 封面
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 添加时间

    def __repr__(self):
        return '<Preview %r>' % self.title

    @classmethod
    def get_ten_previews(cls, page):
        # 每页查询10条
        previews = Preview.query.paginate(page=page, per_page=10)
        return previews

# 评论
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id')) # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) # 所属会员
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 添加时间

    def __repr__(self):
        return '<Comment %r>' % self.id

# 电影收藏
class Moviecol(db.Model):
    __tablename__ = 'moviecol'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id')) # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) # 所属会员
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 添加时间

    def __repr__(self):
        return '<Moviecol %r>' % self.id

# 权限
class Auth(db.Model):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 添加时间

    def __repr__(self):
        return '<Auth %r>' % self.name

# 角色
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    auths = db.Column(db.String(600))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 添加时间

    def __repr__(self):
        return '<Auth %r>' % self.name

# 管理员模型
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 添加时间
    is_super = db.Column(db.SmallInteger) # 是否是超级管理员， 0为超级管理员
    role_id = db.Column(db.Integer, db.ForeignKey('role.id')) # 所属角色
    adminlogs = db.relationship("AdminLog", backref='admin')    #管理员登录日志外键关联
    oplogs = db.relationship("OpLog", backref='admin')  # 管理员操作日志外键关联

    def __repr__(self):
        return '<Admin %r>' % self.name

    def check_pwd(self, pwd):
    #     # 验证密码
    #     from werkzeug.security import check_password_hash
    #     # 相同返回True，不同返回False
    #     return check_password_hash(self.pwd, pwd)
        if self.pwd == pwd:
            return True
        else:
            return False



# 管理员登录日志模型
class AdminLog(db.Model):
    __tablename__ = 'adminlog'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id')) # 所属管理员
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 登录时间

    def __repr__(self):
        return '<AdminLog %r>' % self.id

# 管理员操作日志模型
class OpLog(db.Model):
    __tablename__ = 'oplog'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id')) # 所属管理员
    ip = db.Column(db.String(100))
    reason = db.Column(db.String(600)) # 操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 登录时间

    def __repr__(self):
        return '<OpLog %r>' % self.id

# if __name__ == "__main__":
#     # db.drop_all()
#     # db.create_all()
#     admin = Admin(name='admin', pwd="adminadmin", is_super=0, role_id=1)
#     db.session.add(admin)
#     db.session.commit()