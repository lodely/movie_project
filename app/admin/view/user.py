#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 视图函数


from flask import render_template, redirect, url_for, flash, session, request

from app.admin.base import admin_login_req
from app.admin import admin
from app.models import Users, db


# 会员列表
@admin.route("/user/list/<int:page>", methods=['GET', 'POST'])
@admin_login_req
def user_list(page=None):
    if page is None:
        page = 1
    users = Users.get_ten_page(page=page)
    return render_template("admin/user_list.html", users=users)

# 查看会员
@admin.route("/user/view/<int:id>", methods=['GET'])
@admin_login_req
def user_view(id=None):
    user = Users.query.filter_by(id=id).first()
    return render_template("admin/user_view.html", user=user)

# 删除会员
@admin.route("/user/del/<int:id>", methods=['GET'])
@admin_login_req
def user_del(id=None):
    user = Users.query.filter_by(id=id).first()
    if user:
        with db.auto_commit():
            db.session.delete(user)
        return redirect(url_for("admin.user_list", page=1))
    return render_template("admin/user_list.html", user=user)

# 冻结会员
@admin.route("/user/freeze/<int:id>", methods=['GET'])
@admin_login_req
def user_freeze(id=None):
    user = Users.query.filter_by(id=id).first()
    if user:
        with db.auto_commit():
            user.status = 0
            db.session.add(user)
        return redirect(url_for("admin.user_list", page=1))
    return render_template("admin/user_list.html", user=user)

# 解冻会员
@admin.route("/user/thaw/<int:id>", methods=['GET'])
@admin_login_req
def user_thaw(id=None):
    user = Users.query.filter_by(id=id).first()
    if user:
        with db.auto_commit():
            user.status = 1
            db.session.add(user)
        return redirect(url_for("admin.user_list", page=1))
    return render_template("admin/user_list.html", user=user)
