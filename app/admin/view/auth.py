#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 视图函数


from flask import render_template, redirect, url_for, flash, session, request
from sqlalchemy import or_

from app.admin.base import admin_login_req
from app.admin import admin
from app.models import Auth, db
from app.admin.form.forms import AuthForm

# 添加权限
@admin.route("/auth/add", methods=['GET', 'POST'])
@admin_login_req
def auth_add():
    form = AuthForm()
    # 验证表单
    if form.validate_on_submit():
        data = form.data
        if Auth.query.filter(or_(Auth.name==data['name'], Auth.url==data['url'])).all():
            flash('已有该权限，请不要重复添加', 'err')
            return redirect(url_for('admin.auth_add'))
        new_auth = Auth(
            name=data['name'],
            url=data['url']
        )
        with db.auto_commit():
            db.session.add(new_auth)
        return redirect(url_for('admin.auth_add'))
    return render_template("admin/auth_add.html", form=form)

# 编辑权限
@admin.route("/auth/edit/<int:id>", methods=['GET', 'POST'])
@admin_login_req
def auth_edit(id=None):
    form = AuthForm()
    auth = Auth.query.filter_by(id=id).first()
    if form.validate_on_submit():
        data = form.data
        with db.auto_commit():
            auth.name = data['name']
            auth.url = data['url']
        return redirect(url_for('admin.auth_edit', id=id))
    form.name.data = auth.name
    form.url.data = auth.url
    return render_template("admin/auth_edit.html", form=form)

# 权限列表
@admin.route("/auth/list/<int:page>", methods=['GET'])
@admin_login_req
def auth_list(page=0):
    if not page:
        page = 1
    authes = Auth.get_ten_page(page=page)
    return render_template("admin/auth_list.html", authes=authes)

# 删除权限
@admin.route("/auth/del/<int:id>", methods=['GET'])
@admin_login_req
def auth_del(id=None):
    auth = Auth.query.filter_by(id=id).first()
    if auth:
        with db.auto_commit():
            db.session.delete(auth)
        return redirect(url_for('admin.auth_list', page=1))
    return render_template("admin/auth_list.html")