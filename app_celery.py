# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: app_celery.py
@time: 2025/3/30 00:02 
@desc: 

"""
from config.config import REDIS
from celery import Celery

broker = f"redis://:{REDIS.get('password2', '')}{REDIS['host']}:{REDIS['port']}/{REDIS['db_broker']}"
backend = f"redis://:{REDIS.get('password2', '')}{REDIS['host']}:{REDIS['port']}/{REDIS['db_backend']}"
app_celery = Celery('tasks', broker=broker, backend=backend)
app_celery.conf.timezone = 'Asia/Shanghai'
app_celery.conf.enable_utc = False
app_celery.conf.result_serializer = 'json'
app_celery.conf.task_result_expires = 60*60*60



app_celery.conf.beat_schedule = {
    "add_accounts": {
        "task": "tasks.add_accounts",
        "schedule": 300.0,
        "args": (),
        "options": {"countdown": 0},
    },

    "tasks": {
        "task": "tasks.task_all",
        "schedule": 1.0,
        "args": (),
        "options": {"countdown": 0},
    }
}
