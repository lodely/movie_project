#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 视图函数


from flask import render_template, redirect, url_for, flash, session, request
from app.admin.base import admin_login_req
from app.admin import admin
from app.admin.form.forms import AdminForm
from app.models import Admin, db

# 添加管理员
@admin.route("/admin/add", methods=['GET', 'POST'])
@admin_login_req
def admin_add():
    form = AdminForm()
    if form.validate_on_submit():
        pass
    return render_template("admin/admin_add.html", form=form)

# 删除管理员
@admin.route("/admin/del/<int:id>", methods=['GET'])
@admin_login_req
def admin_del(id=None):
    admin = Admin.query.filter_by(id=id).first()
    if admin:
        with db.auto_commit():
            db.session.delete(admin)
        return redirect(url_for('admin.admin_list', page=1))
    return render_template("admin/admin_list.html")

# 管理员列表
@admin.route("/admin/list/<int:page>", methods=['GET', 'POST'])
@admin_login_req
def admin_list(page=0):
    if not page:
        page = 1
    admins = Admin.get_ten_page(page=page)
    return render_template("admin/admin_list.html", admins=admins)
