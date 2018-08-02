#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Blueprint

# 创建蓝图对象
admin = Blueprint("admin", __name__)

import app.admin.view.login
import app.admin.view.admin
import app.admin.view.auth
import app.admin.view.comment
import app.admin.view.movie
import app.admin.view.moviecol
import app.admin.view.log
import app.admin.view.preview
import app.admin.view.role
import app.admin.view.tags
import app.admin.view.user