# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: tasks.py
@time: 2025/3/30 00:05 
@desc: 

"""
import asyncio
import json
from config.config import MONITOR_LIST1, MONITOR_LIST2
from utils.utils_redis import asyncRedis
from utils.utils_check_env import check_env
from utils.utils_monkey_patch import monkey_patch
from app_celery import app_celery
from scripts.add_accounts import AddAccounts
from scripts.script1_2 import Scripts
from scripts.task1 import TwitterMain1
from scripts.task2 import TwitterMain2
import warnings
from urllib3.exceptions import InsecureRequestWarning
import logging

# 忽略 InsecureRequestWarning 警告
warnings.simplefilter('ignore', InsecureRequestWarning)
logging.getLogger('apscheduler').setLevel(logging.ERROR)

scripts = Scripts()


async def check_account_async():
    """

    :return:
    """
    monkey_patch()
    check_env()
    aa = AddAccounts()
    await aa.check_account()



@app_celery.task
def add_accounts():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        # 你的异步代码
        result = loop.run_until_complete(check_account_async())
        return result
    finally:
        # 关闭事件循环
        loop.close()


@app_celery.task
def task_all():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        # 你的异步代码
        result = loop.run_until_complete(scripts.task_async())
        return result
    finally:
        # 关闭事件循环
        loop.close()
