#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 视图函数


from flask import render_template, redirect, url_for, flash, session, request

from app.admin.base import admin_login_req
from app.admin.form.forms import LoginForm, ResetPwdForm
from app.models import Admin, db, AdminLog, OpLog
from app.admin import admin



# 控制面板
@admin.route("/")
@admin_login_req
def index():
    return render_template("admin/index.html")
    # pass

# 登录
@admin.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # form.validata_account(form.account)
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data['account']).first()
        if not admin.check_pwd(data['pwd']):
            flash("密码错误！", 'pwderr')
            return redirect(url_for("admin.login"))
        # 验证通过保存账号到session
        session["admin"] = data["account"]
        session['id'] = admin.id

        # 获取管理员登录ip
        admin_ip = request.remote_addr
        session['login_ip'] = admin_ip
        # 保存到登录日志
        new_adminlog = AdminLog(admin_id=session['id'], ip=session['login_ip'])
        db.session.add(new_adminlog)
        db.session.commit()

        return redirect(request.args.get("next") or url_for("admin.index"))
    return render_template("admin/login.html", form=form)

# 注销
@admin.route("/logout")
@admin_login_req
def logout():
    with db.auto_commit():
        # 记录注销操作
        new_adminlog = OpLog(
                admin_id=session['id'],
                ip=session['login_ip'],
                reason="注销")
        db.session.add(new_adminlog)
    # session.clear()
    session.pop("admin", None)
    session.pop("id", None)
    return redirect(url_for("admin.login"))

# 修改密码
@admin.route("/pwd", methods=['GET', 'POST'])
@admin_login_req
def pwd():
    form = ResetPwdForm()
    data = form.data

    if form.validate_on_submit():
        id = session['id']
        admin = Admin.query.filter_by(id=id, pwd=data['old_pwd']).first()
        if not admin:
            flash('旧密码输入有误，请重新输入', 'err')
            return redirect(url_for('admin.pwd'))

        with db.auto_commit():
            admin.pwd = data['new_pwd']
            db.session.add(admin)

            # 记录修改密码操作
            new_adminlog = OpLog(
                    admin_id=session['id'],
                    ip=session['login_ip'],
                    reason="修改密码")
            db.session.add(new_adminlog)

        return redirect(url_for('admin.pwd'))
    return render_template("admin/pwd.html", form=form)

# test
# @admin.route("/test", methods=['GET', 'POST'])
# @admin_login_req
# def test():
#     print("ip:%s" % request.remote_addr)
#     return "helo"

















