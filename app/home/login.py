#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 视图函数

# 从当前模块中导入蓝图对象
from sqlalchemy import or_

from . import home
from flask import render_template, redirect, url_for, flash, request
from app.home.form.forms import LoginForm, RegisterForm
from app.models import Users, db, UserLog

from flask_login import logout_user, login_required, login_user, current_user
from app.home.base import get_rand_uuid
from time import sleep

# 登录
@home.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        # 查询该用户
        user = Users.query.filter(
                or_(
                        Users.nickname==data['account'],
                        Users.phone==data['account'],
                        Users.email==data['account'])
        ).first()
        # 验证该用户密码与输入密码是否一致
        if not user.check_pwd(data['pwd']):
            flash('密码错误！', 'pwderr')
            return redirect(url_for('home.login'))

        # 让浏览器保存cookie一段时间
        login_user(user, remember=True)

        # 记录用户登录
        new_userlog = UserLog(
                user_id=current_user.id,
                ip=request.remote_addr
        )
        db.session.add(new_userlog)
        db.session.commit()
        return redirect(url_for('home.index'))
    return render_template("home/login.html", form=form)

# 注销
@home.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home.login"))

# 注册
@home.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        with db.auto_commit():
            new_user = Users(
                nickname=data['nickname'],
                email=data['email'],
                phone=data['phone'],
                password=data['pwd'],
                uuid=get_rand_uuid()
            )
            db.session.add(new_user)
            # 记录用户注册
            # new_adminlog = OpLog(
            #         admin_id=session['id'],
            #         ip=session['login_ip'],
            #         reason="编辑管理员: "+admin.name)
            # db.session.add(new_adminlog)
        return redirect(url_for("home.registerOK"))
    return render_template("home/register.html", form=form)

# 注册成功
@home.route("/register/ok", methods=['GET'])
def registerOK():
    flash('注册成功！', 'registerOK')
    return render_template("home/registerOK.html")
