#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 视图函数

# 从当前模块中导入蓝图对象
import os

from flask import render_template, redirect, url_for, flash, session, request

from app.admin.base import admin_login_req
from app.admin import admin

# 操作日志列表
@admin.route("/oplog/list")
@admin_login_req
def oplog_list():
    return render_template("admin/oplog_list.html")