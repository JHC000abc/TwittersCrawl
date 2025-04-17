# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: utils_monkey_patch.py
@time: 2025/3/29 21:38 
@desc: 

"""
import logging
import builtins

def monkey_patch():
    """

    :return:
    """
    # 配置 logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )

    log = logging.getLogger()

    # 将 print 重定向为 log.info
    builtins.print = lambda *args, **kwargs: log.info(" ".join(map(str, args)))