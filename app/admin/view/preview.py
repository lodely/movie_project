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
def preview_list(page=None):
    if page is None:
        page=1
    previews = Preview.get_ten_previews(page=page)
    return render_template("admin/preview_list.html", previews=previews)