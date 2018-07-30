#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 视图函数

# 从当前模块中导入蓝图对象
from . import home
from flask import render_template, redirect, url_for

# 列表
@home.route("/")
def index():
    return render_template("home/index.html")

# 动画
@home.route("/animation")
def animation():
    return render_template("home/animation.html")

# 登录
@home.route("/login")
def login():
    return render_template("home/login.html")

# 注销
@home.route("/logout")
def logout():
    return redirect(url_for("home.login"))

# 注册
@home.route("/register")
def register():
    return render_template("home/register.html")

# 会员中心
@home.route("/user")
def user():
    return render_template("home/user.html")

# 修改密码
@home.route("/pwd")
def pwd():
    return render_template("home/pwd.html")

# 评论
@home.route("/comments")
def comments():
    return render_template("home/comments.html")

# 登录日志
@home.route("/loginlog")
def loginlog():
    return render_template("home/loginlog.html")

# 收藏电影
@home.route("/moviecol")
def moviecol():
    return render_template("home/moviecol.html")

# 搜索电影
@home.route("/search")
def search():
    return render_template("home/search.html")

# 搜索电影
@home.route("/play")
def play():
    return render_template("home/play.html")

