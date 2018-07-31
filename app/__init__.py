#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True

# 配置连接的数据库
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+cymysql://root:root@localhost:3306/movie_project'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = '205YWHhaG0ASHGghaoghaQA0TGAHLHG'

db = SQLAlchemy(app)

from app.admin import admin as admin_blueprint
from app.home import home as home_blueprint

# url_prefix区分两个蓝图
app.register_blueprint(admin_blueprint, url_prefix="/admin")
app.register_blueprint(home_blueprint)

# 404
@app.errorhandler(404)
def page_not_find(error):
    return render_template("home/404.html"), 404