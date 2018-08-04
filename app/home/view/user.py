#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 视图函数

# 从当前模块中导入蓝图对象
from app.home import home
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.home.form.forms import MemberCentreForm, ResetPwdForm
from app.models import Users, db, UserLog, Comment, Moviecol


# 会员中心
@home.route("/user", methods=['GET', 'POST'])
@login_required
def user():
    form = MemberCentreForm()
    if form.validate_on_submit():
        data = form.data
        user = Users.query.filter_by(id=current_user.id).first()
        with db.auto_commit():
            user.nickname = data['nickname']
            user.email = data['email']
            user.phone = data['phone']
            user.info = data['info']
            db.session.add(user)
        flash('修改成功', 'save')
    return render_template("home/user.html", form=form)

# 修改密码
@home.route("/pwd", methods=['GET', 'POST'])
@login_required
def pwd():
    form = ResetPwdForm()
    if form.validate_on_submit():
        data = form.data
        user = Users.query.filter_by(id=current_user.id).first()
        if not user.check_pwd(data['oldpwd']):
            flash('密码错误', 'pwderr')
            return redirect(url_for('home.pwd'))
        with db.auto_commit():
            user.password = data['newpwd']
            db.session.add(user)
        flash('修改成功', 'save')
    return render_template("home/pwd.html", form=form)

# 评论
@home.route("/comments/<int:page>", methods=['GET'])
@login_required
def comments(page=0):
    if not page:
        page = 1
    comments = Comment.get_ten_commets(page=page, uid=current_user.id)
    return render_template("home/comments.html", comments=comments)

# 登录日志
@home.route("/loginlog")
@login_required
def loginlog():
    userlogs = UserLog.get_log(uid=current_user.id)
    return render_template("home/loginlog.html", userlogs=userlogs)

# 收藏电影
@home.route("/moviecol/<int:page>", methods=['GET'])
@login_required
def moviecol(page=0):
    if not page:
        page = 1
    moviecols = Moviecol.get_ten_moviecols(page=page, uid=current_user.id)

    return render_template("home/moviecol.html", moviecols=moviecols)
