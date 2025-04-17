# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: utils_send.py
@time: 2025/3/29 16:26 
@desc: 

"""
import traceback
from telegram import Bot
import aiohttp
from config.config import TELEGRAM_BOT_TOKEN,CHAT_ID


class UtilsSend:
    """

    """

    async def send_tg(self, msg, bot_token=TELEGRAM_BOT_TOKEN, chat_id=CHAT_ID):
        """

        :param msg:
        :param bot_token:
        :param chat_id:
        :return:
        """
        try:
            bot = Bot(token=bot_token)
            print(f"msg_tg:{msg}")
            await bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
            return True
        except Exception as e:
            print(traceback.format_exc())
            return False

    async def send_web_hook(self, msg, host):
        """

        :param msg:
        :param hook_tag:
        :return:
        """
        url = f"http://{host}/webhook"
        headers = {
            "Content-Type": "application/json",
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=msg, headers=headers, ssl=False,
                                        timeout=aiohttp.ClientTimeout(total=2)) as response:
                    if response.status == 200:
                        print(f"msg_web_hook:{url}---{msg}")
                        return True
                    else:
                        print(response.status)
                        return False
            except Exception as e:
                print(f"webhook 发送失败:{url}----{msg}，{e}")
                return False

