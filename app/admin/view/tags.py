#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 视图函数


from flask import render_template, redirect, url_for, flash, session

from app.admin.base import admin_login_req
from app.admin.form.forms import TagForm, TagEditForm
from app.models import Tags, db, OpLog
from app.admin import admin

# 添加标签
@admin.route("/tag/add", methods=['GET', 'POST'])
@admin_login_req
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        # 查询是否已经存在该标签
        if Tags.query.filter_by(name=data['name']).first():
            flash("已经存在该标签！", "err")
        else:
            with db.auto_commit():
                tag = Tags(name=data['name'])
                db.session.add(tag)
                # 记录添加标签操作
                new_adminlog = OpLog(
                        admin_id=session['id'],
                        ip=session['login_ip'],
                        reason="添加标签: "+tag.name)
                db.session.add(new_adminlog)
            # flash("标签添加成功！", "ok")
            return redirect(url_for("admin.tag_add"))
    return render_template("admin/tag_add.html", form=form)

# 标签列表
@admin.route("/tag/list/<int:page>", methods=['GET', 'POST'])
@admin_login_req
def tag_list(page=None):
    if page is None:
        page = 1
    tags = Tags.get_ten_page(page=page)
    return render_template("admin/tag_list.html", tags=tags)

# 删除标签
@admin.route("/tag/del/<int:id>", methods=['GET'])
@admin_login_req
def tag_del(id=None):
    tag = Tags.query.filter_by(id=id).first_or_404()
    if tag:
        with db.auto_commit():
            db.session.delete(tag)
            # 记录删除标签操作
            new_adminlog = OpLog(
                    admin_id=session['id'],
                    ip=session['login_ip'],
                    reason="删除标签: "+tag.name)
            db.session.add(new_adminlog)

        return redirect(url_for("admin.tag_list", page=1))
    return render_template("admin/tag_list.html")

# 标签编辑
@admin.route("/tag/edit/<int:id>", methods=['GET', 'POST'])
@admin_login_req
def tag_edit(id=None):
    form = TagEditForm()
    tag = Tags.query.filter_by(id=id).first_or_404()
    if form.validate_on_submit():
        data = form.data

        if Tags.query.filter_by(name=data['name']).first():
            flash("标签已经存在！", "err")
        else:
            with db.auto_commit():
                tag.name = data['name']
                db.session.add(tag)
                # 记录删除标签操作
                new_adminlog = OpLog(
                        admin_id=session['id'],
                        ip=session['login_ip'],
                        reason="删除标签: "+tag.name)
                db.session.add(new_adminlog)

        return redirect(url_for("admin.tag_edit", id=id))
    return render_template("admin/tag_edit.html", form=form)