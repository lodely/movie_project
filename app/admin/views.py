#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 视图函数

# 从当前模块中导入蓝图对象
from . import admin

@admin.route("/")
def index():
    return "admin"