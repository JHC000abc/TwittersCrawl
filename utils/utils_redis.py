# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: utils_redis.py
@time: 2025/3/29 20:45 
@desc: 

"""

import asyncio
import redis.asyncio as aioredis
import json
from config.config import REDIS


class asyncRedis(object):
    """

    """

    def __init__(self):
        self.redis = None
        self.load_config()

    def load_config(self):
        """
        Load Redis configuration from the config.
        """
        self.host = REDIS["host"]
        self.port = REDIS["port"]
        self.db = REDIS["db"]
        self.password = REDIS["password"]

    async def conn(self):
        """
        Establish a connection to Redis.
        """
        if not self.redis:
            self.redis = await aioredis.from_url(f"redis://:{self.password}@{self.host}:{self.port}/{self.db}",
                                                 encoding="utf-8")

    async def set(self, key, value):
        """
        Set a key-value pair in Redis.
        """
        await self.conn()
        return await self.redis.set(key, value)

    async def exists(self, key):
        """
        Check if a key exists in Redis.
        """
        await self.conn()
        return await self.redis.exists(key)

    async def get(self, key):
        """
        Get a value from Redis.
        """
        await self.conn()
        return await self.redis.get(key)

    async def close(self):
        """
        Close the Redis connection properly.
        """
        # if self.redis:
        try:
            await self.redis.aclose()
        except:
            pass

    async def set_enable_account_info(self, account_id, account_info, zset_name):
        """
        Set account information and add account to the Redis sorted set.
        """
        await self.conn()
        await self.redis.hset(f"{account_id}", mapping={"cookies": json.dumps(account_info["cookies"]),
                                                        "headers": json.dumps(account_info["headers"])})
        await self.redis.zadd(zset_name, {account_id: 0})

    async def get_enable_account_info_by_id(self, account_id):
        """
        Get account information by account ID.
        """
        await self.conn()
        cookies = json.loads(await self.redis.hget(f"{account_id}", "cookies"))
        headers = json.loads(await self.redis.hget(f"{account_id}", "headers"))
        return cookies, headers

    async def get_enable_account_used_times(self, zset_name, account_id):
        """
        Get the usage count of an account from a Redis sorted set.
        """
        await self.conn()
        used_times = await self.redis.zscore(zset_name, account_id)
        return used_times

    async def add_enable_account_user_times(self, zset_name, account_id, times=1):
        """
        Increase the usage count of an account.
        """
        await self.conn()
        await self.redis.zincrby(zset_name, times, account_id)

    async def get_least_times_accounts(self, zset_name, status=True):
        """
        Get the account IDs with the least usage count.
        """
        await self.conn()
        if not status:
            return await self.redis.zrange(zset_name, 0, -1)
        else:
            return await self.redis.zrange(zset_name, 0, 0)

    async def get_enable_account_nums(self, zset_name):
        """
        Get the total number of enabled accounts.
        """
        await self.conn()
        return await self.redis.zcard(zset_name)

    async def rm_disable_accounts_by_id(self, account_id, zset_name):
        """
        Remove an account from the Redis sorted set.
        """
        await self.conn()
        return await self.redis.zrem(zset_name, account_id)

    async def check_zset_exists(self, account_id, zset_name):
        """
        Check if an account exists in the Redis sorted set.
        """
        await self.conn()
        status = await self.redis.zrank(zset_name, account_id)
        if status is None:
            return False
        return True

    async def get_all_accounts_used_times(self, zset_name):
        """
        Get the usage count of all accounts.
        """
        await self.conn()
        enable_account_list = await self.get_least_times_accounts(zset_name, False)
        for account_id in enable_account_list:
            account_id = account_id.decode("utf-8")
            print(account_id, await self.get_enable_account_used_times(zset_name, account_id))

    async def push_monitor_name(self, token, name):
        """
        Push a monitor name to the list.
        """
        await self.conn()
        await self.redis.rpush(name, f"{token}")

    async def get_monitor_name(self, name):
        """
        Get all monitor names from the list.
        """
        await self.conn()
        return await self.redis.lrange(name, 0, -1)

    async def rm_monitor_name(self, token, name):
        """
        Remove a monitor name from the list.
        """
        await self.conn()
        return await self.redis.lrem(name, 0, token)

    async def check_monitor_name_exists(self, token, name):
        """
        Check if a monitor name exists in the list.
        """
        await self.conn()
        all = await self.get_monitor_name(name)
        for _name in all:
            _name = _name.decode("utf-8")
            if _name == token:
                return True
        return False

    async def add_set(self, token, set_name):
        """

        :param token:
        :param set_name:
        :return:
        """
        await self.conn()
        return await self.redis.sadd(set_name, json.dumps(token))

    async def get_set(self, set_name):
        """

        :param set_name:
        :return:
        """
        await self.conn()
        members = await self.redis.smembers(set_name)
        return members

    async def check_set_exists(self, token, set_name):
        """

        :param token:
        :param set_name:
        :return:
        """
        await self.conn()
        exists = await self.redis.sismember(set_name, token)
        return exists

    async def del_set(self, token, set_name):
        """

        :param k:
        :return:
        """
        await self.conn()
        return await self.redis.srem(set_name, token)


async def main():
    redis = asyncRedis()
    await redis.conn()
    """
    do something
    """
    await redis.close()


if __name__ == '__main__':
    asyncio.run(main())
