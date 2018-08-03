#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 视图函数


from flask import render_template, redirect, url_for, flash, session, request

from app.admin.base import admin_login_req
from app.admin import admin
from app.models import Comment, db, OpLog


# 评论列表
@admin.route("/comment/list/<int:page>", methods=['GET'])
@admin_login_req
def comment_list(page=0):
    if not page:
        page = 1
    comments = Comment.get_ten_page(page=page)
    return render_template("admin/comment_list.html", comments=comments)

# 评论删除
@admin.route("/movie/del/<int:id>", methods=['GET'])
@admin_login_req
def comment_del(id=None):
    comment = Comment.query.filter_by(id=id).first_or_404()
    if comment:
        with db.auto_commit():
            db.session.delete(comment)

            # 记录删除评论操作
            new_adminlog = OpLog(
                    admin_id=session['id'],
                    ip=session['login_ip'],
                    reason="删除评论--"+comment.user.nickname+" 关于《"+comment.movie.title+"》的评论: "+comment.content)
            db.session.add(new_adminlog)
        return redirect(url_for("admin.comment_list", page=1))
    return render_template("admin/comment_list.html")