#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Blueprint

# 创建蓝图对象
home = Blueprint("home", __name__)

import app.home.views