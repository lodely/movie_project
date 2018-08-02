#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, SelectField, DateField
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
            # "required" : ""
        }
    )
    pwd = PasswordField(
        "密码",
        validators=[DataRequired("请输入密码！"), Length(10,20,message=u'长度位于6~20之间')],
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

    # 视图函数中运行validate_on_submit()的时候会自动验证类中所有的字段
    # 并且会自动运行validate_为函数名开头的方法
    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            # 抛出异常
            raise ValidationError("账号不存在")

class ResetPwdForm(FlaskForm):
    old_pwd = PasswordField(
        "旧密码",
        validators=[DataRequired("请输入旧密码！"), Length(6,20,message=u'长度位于6~20之间')],
        description="旧密码",
        render_kw={
            "type" : "password",
            "class" : "form-control",
            "placeholder" : "请输入旧密码！",
            "id" : "input_pwd",
            # "required" : "required"
        }
    )
    new_pwd = PasswordField(
        "新密码",
        validators=[DataRequired("请输入新密码！"), Length(6,20,message=u'长度位于6~20之间')],
        description="新密码",
        render_kw={
            "type" : "password",
            "class" : "form-control",
            "placeholder" : "请输入新密码！",
            "id" : "input_newpwd",
            # "required" : "required"
        }
    )

    submit = SubmitField(
        "修改",
        render_kw={
            "class" : "btn btn-primary"
        }
    )

    def validate_old_pwd(self, field):
        pwd = field.data
        admin = Admin.query.filter_by(pwd=pwd).first()
        if admin:
            # 旧密码正确
            return True
        return False

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

# 添加电影
class MovieForm(FlaskForm):
    title = StringField(
        "片名",
        validators=[DataRequired("请输入片名！")],
        description="片名",
        render_kw={
            "class" : "form-control",
            "id" : "input_title",
            "placeholder" : "请输入片名！"
        }
    )
    url = FileField(
        "文件",
        validators=[DataRequired("请选择需要上传的文件!")],
        description="文件",
        render_kw={
            "id" : "input_url",
        }
    )

    logo = FileField(
        "封面",
        validators=[DataRequired("请选择需要上传的封面!")],
        description="封面",
        render_kw={
            "id" : "input_logo",
            "placeholder" : "选择文件"
        }
    )

    info = TextAreaField(
        "介绍",
        validators=[DataRequired("请输入电影介绍!")],
        description="介绍",
        render_kw={
            "class" : "form-control",
            "id" : "input_info",
            "rows" : "10",
            "placeholder" : "请输入电影简介！"
        }
    )
    star = SelectField(
        "星级",
        description="星级",
        render_kw={
            "class" : "form-control",
            "id" : "input_star",
        },
        choices=[('1', '1星'),
                 ('2', '2星'),
                 ('3', '3星'),
                 ('4', '4星'),
                 ('5', '5星')]
    )
    tag_id = SelectField(
        "标签",
        description="标签",
        render_kw={
            "class" : "form-control",
            "id" : "input_tag_id",
        },
        # 获取所有标签
        choices=[]
    )
    area = StringField(
        "上映地区",
        validators=[DataRequired("请输入上映地区!")],
        description="上映地区",
        render_kw={
            "class" : "form-control",
            "id" : "input_area",
            "placeholder" : "请输入上映地区！"
        }
    )
    release_time = StringField(
        "上映时间",
        validators=[DataRequired("请输入上映时间!")],
        description="上映时间",
        render_kw={
            "class" : "form-control",
            "id" : "input_release_time",
            "placeholder" : "请输入上映时间！"
        }
    )
    length = StringField(
        "片长",
        validators=[DataRequired("请输入片长!")],
        description="片长",
        render_kw={
            "class" : "form-control",
            "id" : "input_length",
            "placeholder" : "请输入片长！"
        }
    )
    submit = SubmitField(
        "添加",
        render_kw={
            "class" : "btn btn-primary"
        }
    )

# 编辑电影
class EditMovieForm(FlaskForm):
    title = StringField(
        "片名",
        validators=[DataRequired("请输入片名！")],
        description="片名",
        render_kw={
            "class" : "form-control",
            "id" : "input_title",
            "placeholder" : "请输入片名！"
        }
    )

    logo = FileField(
        "封面",
        description="封面",
        render_kw={
            "id" : "input_url",
            "placeholder" : "选择文件"
        }
    )

    info = TextAreaField(
        "介绍",
        validators=[DataRequired("请输入电影介绍!")],
        description="介绍",
        render_kw={
            "class" : "form-control",
            "id" : "input_info",
            "rows" : "10",
            "placeholder" : "请输入电影简介！"
        }
    )
    star = SelectField(
        "星级",
        description="星级",
        render_kw={
            "class" : "form-control",
            "id" : "input_star",
        },
        choices=[('1', '1星'),
                 ('2', '2星'),
                 ('3', '3星'),
                 ('4', '4星'),
                 ('5', '5星')]
    )
    tag_id = SelectField(
        "标签",
        description="标签",
        render_kw={
            "class" : "form-control",
            "id" : "input_tag_id",
        },
        # 获取所有标签
        choices=[]
    )
    area = StringField(
        "上映地区",
        validators=[DataRequired("请输入上映地区!")],
        description="上映地区",
        render_kw={
            "class" : "form-control",
            "id" : "input_area",
            "placeholder" : "请输入上映地区！"
        }
    )
    release_time = StringField(
        "上映时间",
        validators=[DataRequired("请输入上映时间!")],
        description="上映时间",
        render_kw={
            "class" : "form-control",
            "id" : "input_release_time",
            "placeholder" : "请输入上映时间！"
        }
    )
    length = StringField(
        "片长",
        validators=[DataRequired("请输入片长!")],
        description="片长",
        render_kw={
            "class" : "form-control",
            "id" : "input_length",
            "placeholder" : "请输入片长！"
        }
    )
    submit = SubmitField(
        "提交",
        render_kw={
            "class" : "btn btn-primary"
        }
    )

# 添加预告
class PreviewForm(FlaskForm):
    title = StringField(
        "预告标题",
        validators=[DataRequired("请输入预告标题！")],
        description="预告标题",
        render_kw={
            "class" : "form-control",
            "id" : "input_title",
            "placeholder" : "请输入预告标题！"
        }
    )
    logo = FileField(
        "预告封面",
        validators=[DataRequired("请选择需要上传的封面!")],
        description="预告封面",
        render_kw={
            "id" : "input_logo",
            "placeholder" : "选择文件"
        }
    )
    submit = SubmitField(
        "添加",
        render_kw={
            "class" : "btn btn-primary"
        }
    )