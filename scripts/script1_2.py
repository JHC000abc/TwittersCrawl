# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: script1_2.py
@time: 2025/4/4 18:01 
@desc: 

"""
import datetime
import json
import asyncio
from twitter.twitterV2 import TwitterV2
from utils.utils_redis import asyncRedis
from utils.utils_check_env import check_env
from utils.utils_monkey_patch import monkey_patch
from config.config import MONITOR_LIST1, MONITOR_LIST2, ACCOUNT_ENABLE, WEBHOOK1, WEBHOOK2
from utils.utils_send import UtilsSend


class Scripts(object):
    """

    """

    async def process2(self, user_info, redis):
        """
        推文+回复
        :param user_info:
        :param redis:
        :return:
        """
        tag = "process2"
        enable_account = await redis.get_least_times_accounts(ACCOUNT_ENABLE)
        if not enable_account:
            print("号池中没有可用账号")
            return
        enable_account = enable_account[0].decode('utf-8')
        while True:
            try:
                cookies, headers = await redis.get_enable_account_info_by_id(enable_account)
                break
            except:
                await redis.rm_disable_accounts_by_id(enable_account, ACCOUNT_ENABLE)

        await redis.add_enable_account_user_times(ACCOUNT_ENABLE, cookies["auth_token"])

        webhook = await redis.get(WEBHOOK2)
        if webhook:
            webhook = webhook.decode('utf-8')
        tw = TwitterV2()
        data = await tw.crawl_articles_replies(user_info, headers, cookies)
        if data:
            try:
                us = UtilsSend()
                async for _type, msg_send_webhook in tw.parse_articles_replies(data, user_info):
                    _data = msg_send_webhook["data"]
                    create_at = _data["created_at"]
                    id_str = f'{_data["id_str"]}_{tag}'

                    if not await redis.exists(id_str):
                        await redis.set(id_str, id_str)
                        time_verify, create_at = await tw.check_times(create_at, 60)
                        if not time_verify:
                            break

                        msg_send_webhook["data"]["created_at"] = create_at
                        push_status = "推送成功"
                        push_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        if not await redis.exists(f"{id_str}_send_{tag}"):
                            await redis.set(id_str, f"{id_str}_send_{tag}")

                            if not await us.send_web_hook(msg_send_webhook, webhook):
                                push_status = "推送失败"
                            msg_send_tg = await tw.make_send_to_tg(msg_send_webhook, _type)
                            msg_send_tg += f"\n推送时间:{push_time}\n推送地址:{webhook}\n推送状态:{push_status}"
                            await us.send_tg(msg_send_tg)
            except:
                print(f"请求到的数据格式异常1：{data}")

    async def process1(self, user_info, redis):
        """
        推文
        :param user_info:
        :param redis:
        :return:
        """
        tag = "process1"
        enable_account = await redis.get_least_times_accounts(ACCOUNT_ENABLE)
        if not enable_account:
            print("号池中没有可用账号")
            return
        enable_account = enable_account[0].decode('utf-8')
        while True:
            try:
                cookies, headers = await redis.get_enable_account_info_by_id(enable_account)
                break
            except:
                await redis.rm_disable_accounts_by_id(enable_account, ACCOUNT_ENABLE)

        await redis.add_enable_account_user_times(ACCOUNT_ENABLE, cookies["auth_token"])

        webhook = await redis.get(WEBHOOK1)
        if webhook:
            webhook = webhook.decode('utf-8')
        tw = TwitterV2()
        data = await tw.crawl_articles_replies(user_info, headers, cookies)
        if data:
            try:
                us = UtilsSend()
                async for _type, msg_send_webhook in tw.parse_articles_replies(data, user_info):
                    if _type == "article":
                        _data = msg_send_webhook["data"]
                        create_at = _data["created_at"]
                        id_str = f'{_data["id_str"]}_{tag}'
                        if not await redis.exists(id_str):
                            await redis.set(id_str, id_str)
                            time_verify, create_at = await tw.check_times(create_at, 60)
                            if not time_verify:
                                break
                            msg_send_webhook["data"]["created_at"] = create_at
                            push_status = "推送成功"
                            push_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                            if not await redis.exists(f"{id_str}_send_{tag}"):
                                await redis.set(id_str, f"{id_str}_send_{tag}")
                                if not await us.send_web_hook(msg_send_webhook, webhook):
                                    push_status = "推送失败"
                                msg_send_tg = await tw.make_send_to_tg(msg_send_webhook, _type)
                                msg_send_tg += f"\n推送时间:{push_time}\n推送地址:{webhook}\n推送状态:{push_status}"
                                await us.send_tg(msg_send_tg)
            except:
                print(f"请求到的数据格式异常2：{data}")

    async def task_async(self):
        """

        :return:
        """
        monkey_patch()
        check_env()
        redis = asyncRedis()
        await redis.conn()
        try:
            members = await redis.get_set(MONITOR_LIST2)
            tasks = []
            for info in members:
                user_info = json.loads(json.loads(info.decode('utf-8')))
                tasks.append(self.process2(user_info, redis))
            members = await redis.get_set(MONITOR_LIST1)
            for info in members:
                user_info = json.loads(json.loads(info.decode('utf-8')))
                tasks.append(self.process1(user_info, redis))

            await asyncio.gather(*tasks)
        finally:
            await redis.close()


if __name__ == '__main__':
    s = Scripts()
    asyncio.run(s.task_async())
