#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Flask, render_template
import os
# from app.models import db
from flask_login import LoginManager


app = Flask(__name__)
app.debug = True

# 配置连接的数据库
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+cymysql://root:root@localhost:3306/movie_project'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SECRET_KEY"] = '205YWHhaG0ASHGghaoghaQA0TGAHLHG'
app.config["UP_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/")

"""使用该方法导入app只能在视图函数中使用数据库模型"""
# db.init_app(app)
# db.create_all(app=app)

# 保持登录状态
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'home.login'
login_manager.login_message = '请先登录或注册'

from app.admin import admin as admin_blueprint
from app.home import home as home_blueprint

# url_prefix区分两个蓝图
app.register_blueprint(admin_blueprint, url_prefix="/admin")
app.register_blueprint(home_blueprint)

# 404
@app.errorhandler(404)
def page_not_find(error):
    return render_template("home/404.html"), 404