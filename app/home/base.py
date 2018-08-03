#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime
import random

def get_rand_uuid():
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S") #生成当前时间
    randomNum = random.randint(0,100)  #生成的随机整数n，其中0<=n<=100
    randomNum = str(0) + str(randomNum)
    return str(nowTime) + str(randomNum)
