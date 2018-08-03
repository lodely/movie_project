#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 视图函数


from flask import render_template, redirect, url_for, flash, session, request

from app.admin.base import admin_login_req
from app.admin import admin
from app.models import Users, db, OpLog


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
            # 记录删除会员操作
            new_adminlog = OpLog(
                    admin_id=session['id'],
                    ip=session['login_ip'],
                    reason="删除会员: "+user.nickname)
            db.session.add(new_adminlog)
    return redirect(url_for("admin.user_list", page=1))

# 冻结会员
@admin.route("/user/freeze/<int:id>", methods=['GET'])
@admin_login_req
def user_freeze(id=None):
    user = Users.query.filter_by(id=id).first()
    if user.status == 1:
        with db.auto_commit():
            user.status = 0
            db.session.add(user)
            # 记录冻结会员操作
            new_adminlog = OpLog(
                    admin_id=session['id'],
                    ip=session['login_ip'],
                    reason="冻结会员: "+user.nickname)
            db.session.add(new_adminlog)
    return redirect(url_for("admin.user_list", page=1))

# 解冻会员
@admin.route("/user/thaw/<int:id>", methods=['GET'])
@admin_login_req
def user_thaw(id=None):
    user = Users.query.filter_by(id=id).first()
    if user.status == 0:
        with db.auto_commit():
            user.status = 1
            db.session.add(user)
            # 记录解冻会员操作
            new_adminlog = OpLog(
                    admin_id=session['id'],
                    ip=session['login_ip'],
                    reason="解冻会员: "+user.nickname)
            db.session.add(new_adminlog)
    return redirect(url_for("admin.user_list", page=1))

