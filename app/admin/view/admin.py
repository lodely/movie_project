#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 视图函数


from flask import render_template, redirect, url_for, flash, session, request
from app.admin.base import admin_login_req
from app.admin import admin
from app.admin.form.forms import AdminForm
from app.models import Admin, db, Role, OpLog


# 添加管理员
@admin.route("/admin/add", methods=['GET', 'POST'])
@admin_login_req
def admin_add():
    form = AdminForm()
    form.role_id.choices = Role.get_all_roles()
    if form.validate_on_submit():
        data = form.data
        # temp = Admin.query.filter(Admin.name == data['name']).first()
        if Admin.query.filter(Admin.name == data['name']).first():
            flash('已有该管理员', 'err')
            return redirect(url_for('admin.admin_add'))
        with db.auto_commit():
            new_admin = Admin(
                name=data['name'],
                password=data['pwd'],
                role_id=data['role_id'],
            )
            db.session.add(new_admin)

            # 记录添加管理员操作
            new_adminlog = OpLog(
                    admin_id=session['id'],
                    ip=session['login_ip'],
                    reason="添加管理员: "+data['name'])
            db.session.add(new_adminlog)
        return redirect(url_for('admin.admin_add'))
    return render_template("admin/admin_add.html", form=form)

# 删除管理员
@admin.route("/admin/del/<int:id>", methods=['GET'])
@admin_login_req
def admin_del(id=None):
    admin = Admin.query.filter_by(id=id).first()
    if admin:
        with db.auto_commit():
            db.session.delete(admin)

            # 记录删除管理员操作
            new_adminlog = OpLog(
                    admin_id=session['id'],
                    ip=session['login_ip'],
                    reason="删除管理员: "+admin.name)
            db.session.add(new_adminlog)
        return redirect(url_for('admin.admin_list', page=1))
    return render_template("admin/admin_list.html")

# 编辑管理员
@admin.route("/admin/edit/<int:id>", methods=['GET', 'POST'])
@admin_login_req
def admin_edit(id=None):
    form = AdminForm()
    form.role_id.choices = Role.get_all_roles()
    if form.validate_on_submit():
        data = form.data
        if Admin.query.filter_by(name=data['name']).first():
            flash('已有该管理员', 'err')
            return redirect(url_for('admin.admin_edit', id=id))

        admin = Admin.query.filter_by(id=id).first()
        with db.auto_commit():
            admin.name=data['name']
            admin.pwd=data['pwd']
            admin.role_id=data['role_id']
            db.session.add(admin)

            # 记录编辑管理员操作
            new_adminlog = OpLog(
                    admin_id=session['id'],
                    ip=session['login_ip'],
                    reason="编辑管理员: "+admin.name)
            db.session.add(new_adminlog)
        return redirect(url_for('admin.admin_edit', id=id))
    return render_template("admin/admin_edit.html", form=form)

# 管理员列表
@admin.route("/admin/list/<int:page>", methods=['GET', 'POST'])
@admin_login_req
def admin_list(page=0):
    if not page:
        page = 1
    admins = Admin.get_ten_page(page=page)
    return render_template("admin/admin_list.html", admins=admins)
