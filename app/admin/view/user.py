#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 视图函数


from flask import render_template, redirect, url_for, flash, session, request

from app.admin.base import admin_login_req
from app.admin import admin

# 会员列表
@admin.route("/user/list")
@admin_login_req
def user_list():
    return render_template("admin/user_list.html")

# 会员登录日志列表
@admin.route("/userloginlog/list")
@admin_login_req
def userloginlog_list():
    return render_template("admin/userloginlog_list.html")

# 会员列表
@admin.route("/user/view")
@admin_login_req
def user_view():
    return render_template("admin/user_view.html")