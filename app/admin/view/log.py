#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 视图函数


from flask import render_template, redirect, url_for, flash, session, request

from app.admin.base import admin_login_req
from app.admin import admin
from app.models import OpLog, AdminLog, UserLog

# 操作日志列表
@admin.route("/oplog/list/<int:page>", methods=['GET'])
@admin_login_req
def oplog_list(page=0):
    if not page:
        page = 1
    oplogs = OpLog.get_ten_page(page=page)
    return render_template("admin/oplog_list.html", oplogs=oplogs)

# 会员登录日志列表
@admin.route("/userloginlog/list/<int:page>", methods=['GET'])
@admin_login_req
def userloginlog_list(page=0):
    if not page:
        page = 1
    userlogs = UserLog.get_ten_page(page=page)
    return render_template("admin/userloginlog_list.html", userlogs=userlogs)

# 管理员登录日志列表
@admin.route("/adminloginlog/list/<int:page>", methods=['GET'])
@admin_login_req
def adminloginlog_list(page=0):
    if not page:
        page = 1
    adminlogs = AdminLog.get_ten_page(page=page)
    return render_template("admin/adminloginlog_list.html", adminlogs=adminlogs)