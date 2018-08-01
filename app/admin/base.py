#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import redirect, url_for, session, request

from functools import wraps
import datetime
import uuid

# 定义访问控制装饰器
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# 修改文件名称
def change_filename(filename):
    fileinfo = os.path.split(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+str(uuid.uuid4().hex)+fileinfo[-1]
    return filename