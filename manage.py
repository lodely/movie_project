#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app import app
from app.models import manager

if __name__ == "__main__":
    app.run()
    # manager.run()