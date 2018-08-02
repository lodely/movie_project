#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 视图函数

# 从当前模块中导入蓝图对象
import os

from flask import render_template, redirect, url_for, flash, session, request

from app.admin.base import admin_login_req
from app.admin import admin
from app.models import Moviecol, db

# 收藏列表
@admin.route("/moviecol/list/<int:page>", methods=['GET'])
@admin_login_req
def moviecol_list(page=0):
    if not page:
        page = 1
    moviecols = Moviecol.get_ten_page(page=page)
    return render_template("admin/moviecol_list.html", moviecols=moviecols)

# 收藏编辑
@admin.route("/moviecol/edit/<int:id>", methods=['GET'])
@admin_login_req
def moviecol_edit(id=None):
    return render_template("admin/moviecol_list.html")

# 收藏删除
@admin.route("/moviecol/del/<int:id>", methods=['GET'])
@admin_login_req
def moviecol_del(id=None):
    moviecol = Moviecol.query.filter_by(id=id).first()
    if moviecol:
        with db.auto_commit():
            db.session.delete(moviecol)
        return redirect(url_for('admin.moviecol_list', page=1))
    return render_template("admin/moviecol_list.html")