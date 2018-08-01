#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 视图函数


from flask import render_template, redirect, url_for, flash, session, request
from app.admin.base import admin_login_req
from app.admin import admin

# 添加管理员
@admin.route("/admin/list")
@admin_login_req
def admin_add():
    return render_template("admin/admin_add.html")

# 管理员列表
@admin.route("/admin/list")
@admin_login_req
def admin_list():
    return render_template("admin/admin_list.html")
