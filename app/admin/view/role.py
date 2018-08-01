#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 视图函数


from flask import render_template

from app.admin.base import admin_login_req
from app.admin import admin

# 添加角色
@admin.route("/role/add")
@admin_login_req
def role_add():
    return render_template("admin/role_add.html")

# 角色列表
@admin.route("/role/list")
@admin_login_req
def role_list():
    return render_template("admin/role_list.html")