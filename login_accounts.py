# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: login_accounts.py
@time: 2025/3/30 20:19 
@desc: 

"""
import asyncio
from utils.utils_check_env import check_env
from utils.utils_monkey_patch import monkey_patch
from utils.utils_redis import asyncRedis
from twitter.twitter import Twitter
from scripts.add_accounts import AddAccounts


async def check_account_async():
    """
    检查文件里的
    :return:
    """
    monkey_patch()
    check_env()
    aa = AddAccounts()
    await aa.check_account()


async def check_exists_account():
    """
    检查库里的
    :return:
    """
    monkey_patch()
    check_env()
    redis = asyncRedis()
    await redis.conn()
    t = Twitter()
    z_set_name = "ACCOUNT_ENABLE"
    res = await redis.get_least_times_accounts(z_set_name, False)
    for i in res:
        id = i.decode("utf-8")
        try:
            ck, hd = await redis.get_enable_account_info_by_id(id)
            if not await t.verify_account(ck):
                await redis.rm_disable_accounts_by_id(id, z_set_name)
            else:
                print("id", id)
        except:
            pass
    await redis.close()


if __name__ == '__main__':
    asyncio.run(check_exists_account())
