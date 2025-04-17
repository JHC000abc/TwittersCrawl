# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: utils_check_env.py
@time: 2025/3/29 21:38 
@desc: 

"""
import os
from config.config import PROXY


def check_env():
    """

    :return:
    """
    # 检查 DISPLAY 环境变量
    if os.getenv("DISPLAY"):
        print("系统有图形界面（GUI）。配置代理")
        os.environ["http_proxy"] = f"{PROXY}"
        os.environ["https_proxy"] = f"{PROXY}"
        return True
    else:
        print("系统没有图形界面（无头系统）。不配置代理")
        return False
