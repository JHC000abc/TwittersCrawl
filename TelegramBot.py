# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: TelegramBot.py
@time: 2025/3/30 14:55 
@desc: 

"""
import json
import traceback
from telegram import Update
from twitter.twitter import Twitter
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from config.config import MONITOR_LIST1, MONITOR_LIST2, ACCOUNT_ENABLE, WEBHOOK1, WEBHOOK2
from utils.utils_redis import asyncRedis
from utils.utils_monkey_patch import monkey_patch
from utils.utils_check_env import check_env


class TwitterBot:
    """

    """

    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.twitter = Twitter()

    async def parse_functions(self, text):
        """

        :param text:
        :return:
        """
        val = ""
        try:
            args = text.split(" ")
            if len(args) < 2:
                key = args.strip()
                if key in ("show", "showb"):
                    print(f"收到命令:{key}")
                else:
                    print("未知命令")
            else:
                key, val = args
                val = val.strip().replace(" ", "")
                print(f"收到命令:{key} value:{val}")
        except Exception as e:
            print("未知命令", traceback.format_exc())

        return val

    async def start(self, update: Update, context: CallbackContext) -> None:
        """

        :param update:
        :param context:
        :return:
        """
        await self.parse_functions(update.message.text)
        msg = (f"这是一个*Twitter*配置机器人\n当前支持命令:`/add` `/del` `/show` `/web` `/sleep` \n"
               f" `/addb` `/delb` `/showb` `/webb` `/sleepb`")
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=msg, parse_mode='Markdown')
        return

    async def show(self, update: Update, context: CallbackContext) -> None:
        """

        :param update:
        :param context:
        :return:
        """
        redis = asyncRedis()
        await redis.conn()
        members = await redis.get_set(MONITOR_LIST1)
        if len(members) <= 0:
            msg = f"当前监控列表1 被监控账号数量:0"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='Markdown')
            await redis.close()
            return
        members = [f"{ind}-->`{json.loads(json.loads(i.decode('utf-8')))['screen_name']}`" for ind, i in
                   enumerate(members, 1)]
        members_num = len(members)
        out_members = '\n'.join(members)
        set_webhook = await redis.get(WEBHOOK1)
        if set_webhook:
            set_webhook = set_webhook.decode('utf-8')
        msg = f"当前Webhook1:{set_webhook}\n当前监控列表1 存在被监控账号数量:{members_num}\n{out_members}"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='Markdown')
        await redis.close()
        return

    async def show2(self, update: Update, context: CallbackContext) -> None:
        """

        :param update:
        :param context:
        :return:
        """
        redis = asyncRedis()
        await redis.conn()
        members = await redis.get_set(MONITOR_LIST2)
        print("members", members)
        if len(members) <= 0:
            msg = f"当前监控列表2 被监控账号数量:0"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='Markdown')
            await redis.close()
            return

        members = [f"{ind}-->`{json.loads(json.loads(i.decode('utf-8')))['screen_name']}`" for ind, i in
                   enumerate(members, 1)]
        members_num = len(members)
        out_members = '\n'.join(members)
        set_webhook = await redis.get(WEBHOOK2)
        if set_webhook:
            set_webhook = set_webhook.decode('utf-8')
        msg = f"当前Webhook1:{set_webhook}\n当前监控列表2 存在被监控账号数量:{members_num}\n{out_members}"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='Markdown')
        await redis.close()
        return

    async def add(self, update: Update, context: CallbackContext) -> None:
        """

        :param update:
        :param context:
        :return:
        """
        add_name = await self.parse_functions(update.message.text)
        if add_name == "":
            msg = "未解析到要添加的用户信息"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='Markdown')
            return

        redis = asyncRedis()
        await redis.conn()
        try:
            enable_account = await redis.get_least_times_accounts(ACCOUNT_ENABLE)
            enable_account = enable_account[0].decode('utf-8')
            cookies, headers = await redis.get_enable_account_info_by_id(enable_account)
            data = await self.twitter.get_user_info_by_screen_name(f"{add_name}", headers, cookies)
            async for res in self.twitter.parse_user_info(data):
                screen_name = res.get("screen_name")
                if screen_name == add_name:
                    info_insert = json.dumps(res, indent=4, ensure_ascii=False)
                    await redis.add_set(info_insert, MONITOR_LIST1)
                    msg = f"成功添加用户信息:{info_insert}"
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='Markdown')
                    await redis.close()
                    return res
        except Exception as e:
            print(traceback.format_exc())

        msg = "未搜索到要添加的用户信息"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='Markdown')
        await redis.close()
        return

    async def add2(self, update: Update, context: CallbackContext) -> None:
        """

        :param update:
        :param context:
        :return:
        """
        add_name = await self.parse_functions(update.message.text)
        if add_name == "":
            msg = "未解析到要添加的用户信息"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='Markdown')
            return

        redis = asyncRedis()
        await redis.conn()
        try:
            enable_account = await redis.get_least_times_accounts(ACCOUNT_ENABLE)
            enable_account = enable_account[0].decode('utf-8')
            cookies, headers = await redis.get_enable_account_info_by_id(enable_account)
            data = await self.twitter.get_user_info_by_screen_name(f"{add_name}", headers, cookies)
            async for res in self.twitter.parse_user_info(data):
                screen_name = res.get("screen_name")
                if screen_name == add_name:
                    info_insert = json.dumps(res, indent=4, ensure_ascii=False)
                    await redis.add_set(info_insert, MONITOR_LIST2)
                    msg = f"成功添加用户信息:{info_insert}"
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='Markdown')
                    await redis.close()
                    return res
        except Exception as e:
            print(traceback.format_exc())

        msg = "未搜索到要添加的用户信息"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='Markdown')
        await redis.close()
        return

    async def delete(self, update: Update, context: CallbackContext) -> None:
        """

        :param update:
        :param context:
        :return:
        """
        redis = asyncRedis()
        await redis.conn()
        del_name = await self.parse_functions(update.message.text)
        print(f"删除:{del_name}")
        members = await redis.get_set(MONITOR_LIST1)
        for info in members:
            info_dic = json.loads(json.loads(info.decode('utf-8')))
            user_id = info_dic.get("id")
            user_screen_name = info_dic.get("screen_name")
            if user_screen_name == del_name:
                await redis.del_set(info, MONITOR_LIST1)
                msg = f"成功删除:`{del_name}`-->`{user_id}`"
                await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='Markdown')
                await redis.close()
                return
        msg = f"未找到匹配的用户信息:`{del_name}`"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='Markdown')
        await redis.close()
        return

    async def delete2(self, update: Update, context: CallbackContext) -> None:
        """

        :param update:
        :param context:
        :return:
        """
        redis = asyncRedis()
        await redis.conn()
        del_name = await self.parse_functions(update.message.text)
        print(f"删除:{del_name}")
        members = await redis.get_set(MONITOR_LIST2)
        for info in members:
            info_dic = json.loads(json.loads(info.decode('utf-8')))
            user_id = info_dic.get("id")
            user_screen_name = info_dic.get("screen_name")
            if user_screen_name == del_name:
                await redis.del_set(info, MONITOR_LIST2)
                msg = f"成功删除:`{del_name}`-->`{user_id}`"
                await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='Markdown')
                await redis.close()
                return
        msg = f"未找到匹配的用户信息:`{del_name}`"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='Markdown')
        await redis.close()
        return

    async def webhook1(self, update: Update, context: CallbackContext) -> None:
        """

        :param update:
        :param context:
        :return:
        """

        webhook = await self.parse_functions(update.message.text)
        print(f"配置webhook1:{webhook}")
        if webhook == "":
            msg = f"webhook1 地址为空 不进行配置"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='Markdown')
            return
        redis = asyncRedis()
        await redis.conn()
        await redis.set(WEBHOOK1, f"{webhook}")
        set_webhook = await redis.get(WEBHOOK1)
        if not set_webhook:
            msg = f"配置webhook1地址:`{webhook}`失败"
        else:
            set_webhook = set_webhook.decode("utf-8")
            if set_webhook == webhook:
                msg = f"成功配置webhook1地址:`{set_webhook}`"
            else:
                msg = f"配置webhook1地址:`{webhook}`失败"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='Markdown')
        await redis.conn()
        return

    async def webhook2(self, update: Update, context: CallbackContext) -> None:
        """

        :param update:
        :param context:
        :return:
        """

        webhook = await self.parse_functions(update.message.text)
        print(f"配置webhook2:{webhook}")
        if webhook == "":
            msg = f"webhook2 地址为空 不进行配置"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='Markdown')
            return
        redis = asyncRedis()
        await redis.conn()
        await redis.set(WEBHOOK2, f"{webhook}")
        set_webhook = await redis.get(WEBHOOK2)
        if not set_webhook:
            msg = f"配置webhook2地址:`{webhook}`失败"
        else:
            set_webhook = set_webhook.decode("utf-8")
            if set_webhook == webhook:
                msg = f"成功配置webhook2地址:`{set_webhook}`"
            else:
                msg = f"配置webhook2地址:`{webhook}`失败"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='Markdown')
        await redis.conn()
        return

    def process(self):
        monkey_patch()
        check_env()

        application = ApplicationBuilder().token(self.bot_token).build()
        application.add_handler(CommandHandler('start', self.start))

        application.add_handler(CommandHandler('show', self.show))
        application.add_handler(CommandHandler('showb', self.show2))

        application.add_handler(CommandHandler('add', self.add))
        application.add_handler(CommandHandler('addb', self.add2))

        application.add_handler(CommandHandler('del', self.delete))
        application.add_handler(CommandHandler('delb', self.delete2))

        application.add_handler(CommandHandler('web', self.webhook1))
        application.add_handler(CommandHandler('webb', self.webhook2))

        print("当前机器人已启动")
        application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    token = "7878875019:AAGQ9AihJyE5jmSoWMt4O1j1CQThjfwR0nk"
    tb = TwitterBot(token)
    tb.process()
