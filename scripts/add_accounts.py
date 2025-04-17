# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: add_accounts.py
@time: 2025/3/29 21:37 
@desc: 

"""
import asyncio
import traceback
from twitter.twitter import Twitter
from utils.utils_redis import asyncRedis
from config.config import ACCOUNT_ENABLE
from utils.utils_send import UtilsSend



class AddAccounts(object):
    """

    """

    def __init__(self):
        self.twitter = Twitter()
        self.send = UtilsSend()

    async def read_account_from_file(self, file):
        """

        :param file:
        :return:
        """
        with open(file, 'r', encoding="utf-8") as f:
            for i in f:
                line = i.strip()
                yield line

    def parse_accounts(self, line):
        """

        :param line:
        :return:
        """
        lis = line.split("----")
        user_name, password, email, auth_token, ct0, twofaCode, BackupCode = lis
        cookies = {"user_name": user_name, "email": email, "password": password,
                   "auth_token": auth_token, "ct0": ct0, "twofaCode": twofaCode, "BackupCode": BackupCode}
        return cookies

    async def process(self, line, redis):
        """

        :param line:
        :param redis:
        :return:
        """

        cookie_buy = self.parse_accounts(line)
        auth_token = cookie_buy["auth_token"]
        try:
            await self.twitter.login(cookie_buy)
            account_data = await self.twitter.parse_login_data()
            if await self.twitter.verify_account(cookie_buy):
                print(f"账号可用 {auth_token}")
                if await redis.check_zset_exists(auth_token, ACCOUNT_ENABLE):
                    await redis.add_enable_account_user_times(ACCOUNT_ENABLE, auth_token)
                    print(f"已存在 {auth_token} 使用次数:",
                          await redis.get_enable_account_used_times(ACCOUNT_ENABLE, auth_token))
                else:
                    await redis.set_enable_account_info(auth_token, account_data, ACCOUNT_ENABLE)
                    print(f"已添加 {auth_token}")
            else:
                await redis.rm_disable_accounts_by_id(auth_token, ACCOUNT_ENABLE)
                print(f"账号不可用 {auth_token} 已删除")
        except Exception as e:
            print(f"异常,已删除 {auth_token}", traceback.format_exc())
            await redis.rm_disable_accounts_by_id(auth_token, ACCOUNT_ENABLE)

        finally:
            return redis

    async def check_account(self):
        """

        :return:
        """
        redis = asyncRedis()
        await redis.conn()
        try:
            async for line in self.read_account_from_file(r"./config/accounts.list"):
                redis = await self.process(line, redis)
        except Exception as e:
            print(traceback.format_exc())
        finally:
            enable_nums = await redis.get_enable_account_nums(ACCOUNT_ENABLE)
            msg = f"当前可用账号数量:{enable_nums}"
            await self.send.send_tg(msg)
            await redis.close()

if __name__ == '__main__':
    asyncio.run(AddAccounts().check_account())