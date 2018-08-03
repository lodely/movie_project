#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 视图函数


from flask import render_template, redirect, url_for, flash, session

from app.admin.base import admin_login_req
from app.admin import admin
from app.admin.form.forms import RoleForm
from app.models import Role, db, OpLog


# 添加角色
@admin.route("/role/add", methods=['GET', 'POST'])
@admin_login_req
def role_add():
    form = RoleForm()
    if form.validate_on_submit():
        data = form.data
        if Role.query.filter_by(name=data['name']).first():
            flash('已存在该角色，请不要重复添加', 'err')
            return redirect(url_for('admin.role_add'))
        with db.auto_commit():
            new_role = Role(name=data['name'])
            db.session.add(new_role)
            # 记录添加角色操作
            new_adminlog = OpLog(
                    admin_id=session['id'],
                    ip=session['login_ip'],
                    reason="添加角色: "+new_role.name)
            db.session.add(new_adminlog)
        return redirect(url_for('admin.role_add'))
    return render_template("admin/role_add.html", form=form)

# 删除角色
@admin.route("/role/del/<int:id>", methods=['GET'])
@admin_login_req
def role_del(id=None):
    role = Role.query.filter_by(id=id).first()
    if role:
        with db.auto_commit():
            db.session.delete(role)
            # 记录删除角色操作
            new_adminlog = OpLog(
                    admin_id=session['id'],
                    ip=session['login_ip'],
                    reason="删除角色: "+role.name)
            db.session.add(new_adminlog)
        return redirect(url_for('admin.role_list', page=1))
    return render_template("admin/role_list.html")

# 编辑角色
@admin.route("/role/edit/<int:id>", methods=['GET', 'POST'])
@admin_login_req
def role_edit(id=None):
    form = RoleForm()
    role = Role.query.filter_by(id=id).first()
    if form.validate_on_submit():
        data = form.data
        with db.auto_commit():
            role.name=data['name']
            db.session.add(role)
            # 记录编辑角色操作
            new_adminlog = OpLog(
                    admin_id=session['id'],
                    ip=session['login_ip'],
                    reason="编辑角色: "+role.name)
            db.session.add(new_adminlog)
        return redirect(url_for('admin.role_edit', id=id))
    form.name.data = role.name
    return render_template("admin/role_edit.html", form=form)

# 角色列表
@admin.route("/role/list/<int:page>", methods=['GET', 'POST'])
@admin_login_req
def role_list(page=0):
    if not page:
        page = 1
    roles = Role.get_ten_page(page=page)

    return render_template("admin/role_list.html", roles=roles)