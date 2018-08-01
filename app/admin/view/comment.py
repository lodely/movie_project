#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 视图函数


from flask import render_template, redirect, url_for, flash, session, request

from app.admin.base import admin_login_req
from app.admin import admin


# 评论列表
@admin.route("/comment/list")
@admin_login_req
def comment_list():
    return render_template("admin/comment_list.html")