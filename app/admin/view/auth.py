#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 视图函数

# 从当前模块中导入蓝图对象
import os

from flask import render_template, redirect, url_for, flash, session, request


from app.admin.base import admin_login_req
from app.admin import admin

# 添加权限
@admin.route("/auth/add")
@admin_login_req
def auth_add():
    return render_template("admin/auth_add.html")

# 权限列表
@admin.route("/auth/list")
@admin_login_req
def auth_list():
    return render_template("admin/auth_list.html")