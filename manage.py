#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app import app
from app.models import manager

if __name__ == "__main__":
    
    # thread开启多线程，任意ip可以访问
    app.run(host='0.0.0.0', threaded=True)
    # manager.run()