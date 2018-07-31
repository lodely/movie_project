#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Length

from app.models import Admin


class LoginForm(FlaskForm):
    # 管理员登录表单
    account = StringField(
        "账号",
        validators=[DataRequired("请输入账号!")],
        description="账号",
        render_kw={
            "class" : "form-control",
            "placeholder" : "请输入账号！",
            # "required" : "required"
        }
    )
    pwd = PasswordField(
        "密码",
        validators=[DataRequired("请输入密码！"), Length(10,20,message=u'长度位于6~16之间')],
        description="密码",
        render_kw={
            "class" : "form-control",
            "placeholder" : "请输入密码！",
            # "required" : "required"
        }
    )
    submit = SubmitField(
        "登录",
        render_kw={
            "class" : "btn btn-primary btn-block btn-flat"
        }
    )

    # 识图函数中运行validate_on_submit()的时候会自动验证类中所有的字段
    # 并且会自动运行validate_为函数名开头的方法
    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            # 抛出异常
            raise ValidationError("账号不存在")

# 标签添加
class TagForm(FlaskForm):
    name = StringField(
        "标签名称",
        validators=[DataRequired("请输入标签!")],
        description="标签",
        render_kw={
            "class" : "form-control",
            "id" : "input_name",
            "placeholder" : "请输入标签！"
        }
    )
    submit = SubmitField(
        "添加",
        render_kw={
            "class" : "btn btn-primary"
        }
    )

# 标签编辑
class TagEditForm(FlaskForm):
    name = StringField(
        "标签名称",
        validators=[DataRequired("请输入标签!")],
        description="标签",
        render_kw={
            "class" : "form-control",
            "id" : "input_name",
            "placeholder" : "请输入标签！"
        }
    )
    submit = SubmitField(
        "编辑",
        render_kw={
            "class" : "btn btn-primary"
        }
    )