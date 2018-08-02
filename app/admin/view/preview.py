#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 视图函数

import os

from flask import render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename

from app import app
from app.admin.base import admin_login_req, change_filename
from app.admin.form.forms import PreviewForm
from app.models import Preview, db
from app.admin import admin

# 添加预告
@admin.route("/preview/add", methods=['GET', 'POST'])
@admin_login_req
def preview_add():
    form = PreviewForm()
    if form.validate_on_submit():
        data = form.data
        # 如果已有该预告则不添加
        if Preview.query.filter_by(title=data['title']).first():
            flash("预告已经存在，请不要重复添加", "err")
        else:
            with db.auto_commit():
                file_logo = secure_filename(form.logo.data.filename)
                if not os.path.exists(app.config["UP_DIR"]):
                        os.makedirs(app.config["UP_DIR"])
                        os.chmod(app.config["UP_DIR"], "rw")

                logo = change_filename(file_logo)
                form.logo.data.save(app.config["UP_DIR"]+logo)
                new_preview = Preview(
                    title=data['title'],
                    logo=logo
                )
                db.session.add(new_preview)
        return redirect(url_for("admin.preview_add"))
    return render_template("admin/preview_add.html", form=form)

# 预告列表
@admin.route("/preview/list/<int:page>", methods=['GET', 'POST'])
@admin_login_req
def preview_list(page=0):
    if not page:
        page=1
    previews = Preview.get_ten_page(page=page)
    return render_template("admin/preview_list.html", previews=previews)

# 预告删除
@admin.route("/preview/del/<int:id>", methods=['GET'])
@admin_login_req
def preview_del(id=None):
    preview = Preview.query.filter_by(id=id).first_or_404()
    if preview:
        with db.auto_commit():
            db.session.delete(preview)
        return redirect(url_for('admin.preview_list', page=1))
    return render_template("admin/preview_list.html")

# 编辑预告
@admin.route("/preview/edit/<int:id>", methods=['GET', 'POST'])
@admin_login_req
def preview_edit(id=None):
    form = PreviewForm()
    if form.validate_on_submit():
        data = form.data
        preview = Preview.query.filter_by(id=id).first()
        with db.auto_commit():
            # 修改logo名
            file_logo = secure_filename(form.logo.data.filename)
            if not os.path.exists(app.config["UP_DIR"]):
                    os.makedirs(app.config["UP_DIR"])
                    os.chmod(app.config["UP_DIR"], "rw")

            logo = change_filename(file_logo)
            # 保存logo图片
            form.logo.data.save(app.config["UP_DIR"]+logo)

            preview.title=data['title'],
            preview.logo=logo

            db.session.add(preview)
        return redirect(url_for("admin.preview_add"))
    return render_template("admin/preview_add.html", form=form)