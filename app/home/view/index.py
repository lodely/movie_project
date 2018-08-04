#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 视图函数

# 从当前模块中导入蓝图对象
from app.home import home
from flask import render_template, redirect, url_for

# 主页
@home.route("/")
def index():
    return render_template("home/index.html")

# 动画
@home.route("/animation")
def animation():
    return render_template("home/animation.html")

# 搜索电影
@home.route("/search")
def search():
    return render_template("home/search.html")

# 播放电影
@home.route("/play")
def play():
    return render_template("home/play.html")

