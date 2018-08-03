#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask_wtf import FlaskForm
from sqlalchemy import or_
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, SelectField, DateField
from wtforms.validators import DataRequired, ValidationError, Length, EqualTo

from app.models import Users


class LoginForm(FlaskForm):
    # 用户登录表单
    account = StringField(
        "账号",
        validators=[DataRequired("请输入账号!")],
        description="账号",
        render_kw={
            "id" : "input_contact",
            "class" : "form-control input-lg",
            "placeholder" : "用户名/邮箱/手机号码",
        }
    )
    pwd = PasswordField(
        "密码",
        validators=[DataRequired("请输入密码！")],
        description="密码",
        render_kw={
            "id" : "input_pwd",
            "class" : "form-control input-lg",
            "placeholder" : "请输入密码",
        }
    )
    submit = SubmitField(
        "登录",
        render_kw={
            "class" : "btn btn-lg btn-success btn-block"
        }
    )

    # 视图函数中运行validate_on_submit()的时候会自动验证类中所有的字段
    # 并且会自动运行validate_为函数名开头的方法
    def validate_account(self, field):
        account = field.data
        user = Users.query.filter(or_(Users.nickname==account, Users.email==account, Users.phone==account)).all()
        if not user:
            # 抛出异常
            raise ValidationError("账号不存在")

# 注册
class RegisterForm(FlaskForm):
    # 用户注册表单
    nickname = StringField(
        "账号",
        validators=[DataRequired("请输入账号!")],
        description="账号",
        render_kw={
            "id" : "input_nickname",
            "class" : "form-control input-lg",
            "placeholder" : "用户名",
        }
    )
    email = StringField(
        "邮箱",
        validators=[DataRequired("请输入邮箱!")],
        description="邮箱",
        render_kw={
            "id" : "input_email",
            "class" : "form-control input-lg",
            "placeholder" : "邮箱",
        }
    )
    phone = StringField(
        "手机号",
        validators=[DataRequired("请输入手机号!"),
                    Length(8, 11, message=u'长度位于8~11之间')],
        description="手机号",
        render_kw={
            "id" : "input_phone",
            "class" : "form-control input-lg",
            "placeholder" : "手机号",
        }
    )
    pwd = PasswordField(
        "密码",
        validators=[DataRequired("请输入密码！"),
                    Length(6, 20, message=u'长度位于6~20之间'),
                    EqualTo('re_pwd', message=u'两次输入的密码不一致')],
        description="密码",
        render_kw={
            "id" : "input_pwd",
            "class" : "form-control input-lg",
            "placeholder" : "请输入密码",
        }
    )
    re_pwd = PasswordField(
        "确认密码",
        validators=[DataRequired("请重复输入密码！"),
                    Length(6, 20, message=u'长度位于6~20之间')],
        description="确认密码",
        render_kw={
            "id" : "input_re_pwd",
            "class" : "form-control input-lg",
            "placeholder" : "确认密码",
        }
    )
    submit = SubmitField(
        "注册",
        render_kw={
            "class" : "btn btn-lg btn-success btn-block"
        }
    )

    # 视图函数中运行validate_on_submit()的时候会自动验证类中所有的字段
    # 并且会自动运行validate_为函数名开头的方法
    def validate_nickname(self, field):
        nickname = field.data
        user = Users.query.filter_by(nickname=nickname).first()
        if user:
            # 抛出异常
            raise ValidationError("该昵称已被注册")
    def validate_email(self, field):
        email = field.data
        if Users.query.filter_by(email=email).first():
            # 抛出异常
            raise ValidationError("该邮箱已被注册")
    def validate_phone(self, field):
        phone = field.data
        if Users.query.filter_by(phone=phone).first():
            # 抛出异常
            raise ValidationError("该手机号已被注册")

# 会员中心
class MemberCentreForm(FlaskForm):
    # 用户会员中心表单
    nickname = StringField(
        "昵称",
        validators=[DataRequired("请输入昵称!")],
        description="昵称",
        render_kw={
            "id" : "input_name",
            "class" : "form-control",
            "placeholder" : "昵称",
        }
    )
    email = StringField(
        "邮箱",
        validators=[DataRequired("请输入邮箱!")],
        description="邮箱",
        render_kw={
            "id" : "input_email",
            "class" : "form-control",
            "placeholder" : "邮箱",
        }
    )
    phone = StringField(
        "手机号",
        validators=[DataRequired("请输入手机号!"),
                    Length(8, 11, message=u'长度位于8~11之间')],
        description="手机号",
        render_kw={
            "id" : "input_phone",
            "class" : "form-control",
            "placeholder" : "手机号",
        }
    )
    face = FileField(
        "头像",
        description="头像",
        render_kw={
            "id" : "input_face",
            "class" : "control-control",
            "placeholder" : "上传头像",
            "type" : "hidden",
            "autofocus" : ""
        }
    )
    info = TextAreaField(
        "简介",
        description="简介",
        render_kw={
            "id" : "input_info",
            "rows" : "10",
            "class" : "form-control",
        }
    )
    submit = SubmitField(
        "保存修改",
        render_kw={
            "class" : "btn btn-success glyphicon glyphicon-saved"
        }
    )

    # 视图函数中运行validate_on_submit()的时候会自动验证类中所有的字段
    # 并且会自动运行validate_为函数名开头的方法
    def validate_nickname(self, field):
        nickname = field.data
        user = Users.query.filter_by(nickname=nickname).first()
        if user:
            # 抛出异常
            raise ValidationError("该昵称已被注册")
    def validate_email(self, field):
        email = field.data
        if Users.query.filter_by(email=email).first():
            # 抛出异常
            raise ValidationError("该邮箱已被注册")
    def validate_phone(self, field):
        phone = field.data
        if Users.query.filter_by(phone=phone).first():
            # 抛出异常
            raise ValidationError("该手机号已被注册")