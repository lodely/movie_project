#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Blueprint

# 创建蓝图对象
admin = Blueprint("admin", __name__)

import app.admin.views