# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: twitterV2.py
@time: 2025/4/4 15:05 
@desc: 

"""
import datetime
import pytz
import traceback
from twikit import Client
from utils.utils_send import UtilsSend
import aiohttp


class TwitterV2(object):
    """

    """

    def __init__(self):
        self.client = None
        self.utils_send = UtilsSend()

    async def login(self, cookies):
        """

        :return:
        """
        try:
            self.client = Client('en-US', timeout=2)
            self.client.set_cookies(cookies)
        except Exception as e:
            print(traceback.format_exc())

    async def parse_login_data(self):
        """

        :return:
        """
        return {
            "cookies": self.client.get_cookies(),
            "headers": self.client._base_headers,
        }

    async def check_times(self, created_at, seconds=60):
        """

        :param created_at:
        :param seconds:
        :return:
        """
        # 预设时间格式
        date_format = "%a %b %d %H:%M:%S +0000 %Y"
        date_format2 = "%Y-%m-%d %H:%M:%S"

        # 将 created_at 转换为 UTC 时间
        created_at_datetime = datetime.datetime.strptime(created_at, date_format)
        created_at_utc = pytz.utc.localize(created_at_datetime)

        # 转换为东八区时间（Asia/Shanghai）
        eastern_timezone = pytz.timezone("Asia/Shanghai")
        created_at_eastern = created_at_utc.astimezone(eastern_timezone)

        # 获取当前时间，并转化为东八区时间
        now_eastern = datetime.datetime.now(eastern_timezone)

        # 计算时间差并判断是否在 1 分钟内
        time_diff = abs(created_at_eastern - now_eastern)
        publish_time = created_at_eastern.strftime(date_format2)

        if time_diff < datetime.timedelta(seconds=seconds):
            return True, publish_time
        return False, publish_time

    async def get_data(self, url, params, headers, cookies):
        """

        :param url:
        :param params:
        :param headers:
        :param cookies:
        :return:
        """
        data = None
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            try:
                proxy_url = "http://172.17.0.1:10808"
                # proxy_url = None
                async with session.get(url, headers=headers, cookies=cookies, params=params,
                                       proxy=proxy_url) as response:
                    if response.status == 200:
                        data = await response.json()
            except Exception as e:
                # 在这里可以打印异常或进行异常处理
                print(f"请求异常")

        return data

    async def get_user_info_by_screen_name(self, screen_name, headers, cookies):
        """

        :param screen_name:
        :param headers:
        :param cookies:
        :return:
        """
        url = "https://x.com/i/api/graphql/NmwxTF-zpf84dOp-ppJOqA/SearchTimeline"
        params = {
            "variables": "{\"rawQuery\":\"" + screen_name + "\",\"count\":20,\"querySource\":\"typed_query\",\"product\":\"People\"}",
            "features": "{\"rweb_video_screen_enabled\":false,\"profile_label_improvements_pcf_label_in_post_enabled\":true,\"rweb_tipjar_consumption_enabled\":true,\"responsive_web_graphql_exclude_directive_enabled\":true,\"verified_phone_label_enabled\":false,\"creator_subscriptions_tweet_preview_api_enabled\":true,\"responsive_web_graphql_timeline_navigation_enabled\":true,\"responsive_web_graphql_skip_user_profile_image_extensions_enabled\":false,\"premium_content_api_read_enabled\":false,\"communities_web_enable_tweet_community_results_fetch\":true,\"c9s_tweet_anatomy_moderator_badge_enabled\":true,\"responsive_web_grok_analyze_button_fetch_trends_enabled\":false,\"responsive_web_grok_analyze_post_followups_enabled\":true,\"responsive_web_jetfuel_frame\":false,\"responsive_web_grok_share_attachment_enabled\":true,\"articles_preview_enabled\":true,\"responsive_web_edit_tweet_api_enabled\":true,\"graphql_is_translatable_rweb_tweet_is_translatable_enabled\":true,\"view_counts_everywhere_api_enabled\":true,\"longform_notetweets_consumption_enabled\":true,\"responsive_web_twitter_article_tweet_consumption_enabled\":true,\"tweet_awards_web_tipping_enabled\":false,\"responsive_web_grok_show_grok_translated_post\":false,\"responsive_web_grok_analysis_button_from_backend\":true,\"creator_subscriptions_quote_tweet_preview_enabled\":false,\"freedom_of_speech_not_reach_fetch_enabled\":true,\"standardized_nudges_misinfo\":true,\"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled\":true,\"longform_notetweets_rich_text_read_enabled\":true,\"longform_notetweets_inline_media_enabled\":true,\"responsive_web_grok_image_annotation_enabled\":true,\"responsive_web_enhance_cards_enabled\":false}"
        }
        return await self.get_data(url, params, headers, cookies)

    async def get_user_articles_by_id(self, user_id, headers, cookies):
        """

        :param user_id:
        :param headers:
        :param cookies:
        :return:
        """
        url = "https://x.com/i/api/graphql/gVT5sOlEY47S8Reakxjivw/UserTweets"
        params = {
            "variables": "{\"userId\":\"" + user_id + "\",\"count\":20,\"includePromotedContent\":true,\"withQuickPromoteEligibilityTweetFields\":true,\"withVoice\":true,\"withV2Timeline\":true}",
            "features": "{\"rweb_video_screen_enabled\":false,\"profile_label_improvements_pcf_label_in_post_enabled\":true,\"rweb_tipjar_consumption_enabled\":true,\"responsive_web_graphql_exclude_directive_enabled\":true,\"verified_phone_label_enabled\":false,\"creator_subscriptions_tweet_preview_api_enabled\":true,\"responsive_web_graphql_timeline_navigation_enabled\":true,\"responsive_web_graphql_skip_user_profile_image_extensions_enabled\":false,\"premium_content_api_read_enabled\":false,\"communities_web_enable_tweet_community_results_fetch\":true,\"c9s_tweet_anatomy_moderator_badge_enabled\":true,\"responsive_web_grok_analyze_button_fetch_trends_enabled\":false,\"responsive_web_grok_analyze_post_followups_enabled\":true,\"responsive_web_jetfuel_frame\":false,\"responsive_web_grok_share_attachment_enabled\":true,\"articles_preview_enabled\":true,\"responsive_web_edit_tweet_api_enabled\":true,\"graphql_is_translatable_rweb_tweet_is_translatable_enabled\":true,\"view_counts_everywhere_api_enabled\":true,\"longform_notetweets_consumption_enabled\":true,\"responsive_web_twitter_article_tweet_consumption_enabled\":true,\"tweet_awards_web_tipping_enabled\":false,\"responsive_web_grok_show_grok_translated_post\":false,\"responsive_web_grok_analysis_button_from_backend\":true,\"creator_subscriptions_quote_tweet_preview_enabled\":false,\"freedom_of_speech_not_reach_fetch_enabled\":true,\"standardized_nudges_misinfo\":true,\"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled\":true,\"longform_notetweets_rich_text_read_enabled\":true,\"longform_notetweets_inline_media_enabled\":true,\"responsive_web_grok_image_annotation_enabled\":true,\"responsive_web_enhance_cards_enabled\":false}",
            "fieldToggles": "{\"withArticlePlainText\":false}"
        }
        return await self.get_data(url, params, headers, cookies)

    async def parse_article_msg_send_to_tg(self, data, tag=""):
        """
        解析数据格式--发给telegram的
        :param data:
        :return:
        """
        _data = data["data"]
        user = _data["user"]
        medias = "\n".join([i.get('media_url_https') for i in _data["extended_entities"]["media"]])
        return f"用户名:{user['name']}\nScreenName:{user['screen_name']}\n" \
               f"发布时间:{_data['created_at']}\n" \
               f"推文内容:{_data['full_text'][:101]}\n" \
               f"媒体链接:{medias}\n" \
               f"类型:推文{tag}"

    async def parse_replies_msg_send_to_tg(self, data, tag=""):
        """
        解析数据格式--发给telegram的
        :param data:
        :return:
        """
        _data = data["data"]
        user = data["task"]["userinfo"]
        medias = "\n".join([i.get('media_url_https') for i in _data["reply_status"]["extended_entities"]["media"]])
        return f"Name:{user['name']}\nScreenName:{user['screen_name']}\n" \
               f"发布时间:{_data['created_at']}\n" \
               f"推文内容:{_data['full_text'][:101]}\n" \
               f"媒体链接:{medias}\n" \
               f"类型:回复{tag}"

    async def verify_account(self, account_buy_cookies):
        """
        验证账号可用性
        :param account_buy_cookies:
        :return:
        """
        user_id = "1903453809147322368"
        await self.login(account_buy_cookies)
        account_data = await self.parse_login_data()
        cookies = account_data["cookies"]
        headers = account_data["headers"]
        data = await self.get_user_articles_by_id(user_id, headers, cookies)
        # print(data)
        return bool(data)

    async def crawl_articles_replies(self, user_info, headers, cookies):
        """

        :param user_info:
        :param headers:
        :param cookies:
        :return:
        """
        userId = user_info['id']
        url = "https://x.com/i/api/graphql/pz0IHaV_t7T4HJavqqqcIA/UserTweetsAndReplies"
        params = {
            "variables": "{\"userId\":\"" + userId + "\",\"count\":20,\"includePromotedContent\":true,\"withCommunity\":true,\"withVoice\":true}",
            "features": "{\"rweb_video_screen_enabled\":false,\"profile_label_improvements_pcf_label_in_post_enabled\":true,\"rweb_tipjar_consumption_enabled\":true,\"responsive_web_graphql_exclude_directive_enabled\":true,\"verified_phone_label_enabled\":false,\"creator_subscriptions_tweet_preview_api_enabled\":true,\"responsive_web_graphql_timeline_navigation_enabled\":true,\"responsive_web_graphql_skip_user_profile_image_extensions_enabled\":false,\"premium_content_api_read_enabled\":false,\"communities_web_enable_tweet_community_results_fetch\":true,\"c9s_tweet_anatomy_moderator_badge_enabled\":true,\"responsive_web_grok_analyze_button_fetch_trends_enabled\":false,\"responsive_web_grok_analyze_post_followups_enabled\":true,\"responsive_web_jetfuel_frame\":false,\"responsive_web_grok_share_attachment_enabled\":true,\"articles_preview_enabled\":true,\"responsive_web_edit_tweet_api_enabled\":true,\"graphql_is_translatable_rweb_tweet_is_translatable_enabled\":true,\"view_counts_everywhere_api_enabled\":true,\"longform_notetweets_consumption_enabled\":true,\"responsive_web_twitter_article_tweet_consumption_enabled\":true,\"tweet_awards_web_tipping_enabled\":false,\"responsive_web_grok_show_grok_translated_post\":false,\"responsive_web_grok_analysis_button_from_backend\":true,\"creator_subscriptions_quote_tweet_preview_enabled\":false,\"freedom_of_speech_not_reach_fetch_enabled\":true,\"standardized_nudges_misinfo\":true,\"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled\":true,\"longform_notetweets_rich_text_read_enabled\":true,\"longform_notetweets_inline_media_enabled\":true,\"responsive_web_grok_image_annotation_enabled\":true,\"responsive_web_enhance_cards_enabled\":false}",
            "fieldToggles": "{\"withArticlePlainText\":false}"
        }
        return await self.get_data(url, params, headers, cookies)

    async def get_medias(self, extended_entities):
        """

        :param extended_entities:
        :return:
        """
        medias_lis = []
        if extended_entities:
            medias = extended_entities["media"]
            for media in medias:
                media_url_https = media["media_url_https"]
                _type = media["type"]
                medias_lis.append({"media_url_https": media_url_https, "type": _type})
        return medias_lis

    async def parse_legacy(self, legacy, id, screen_name):
        """

        :param legacy:
        :param id:
        :param screen_name:
        :return:
        """
        extended_entities = legacy.get("extended_entities", [])
        if extended_entities:
            extended_entities = await self.get_medias(extended_entities)
        id_str = legacy.get("id_str", "")
        url = ""
        if id_str:
            url = f"https://x.com/{screen_name}/status/{id_str}"
        return {
            "full_text": legacy.get("full_text", ""),
            "created_at": legacy.get("created_at", ""),
            "favorite_count": legacy.get("favorite_count", 0),
            "is_quote_status": legacy.get("is_quote_status", False),
            "quote_count": legacy.get("quote_count", 0),
            "retweet_count": legacy.get("retweet_count", 0),
            "is_retweet": legacy.get("retweeted", False),
            "user_id_str": legacy.get("user_id_str", ""),
            "id_str": id_str,
            "url": url,
            "quoted_status_id_str": legacy.get("quoted_status_id_str", ""),
            "in_reply_to_status_id_str": id,
            "reply_count": legacy.get("reply_count", 0),
            "extended_entities": extended_entities,
            "in_reply_to_screen_name": legacy.get("in_reply_to_screen_name", ""),
        }

    async def make_send_article(self, data, name, screen_name):
        """

        :param data:
        :param name:
        :param screen_name:
        :return:
        """
        return {
            "task": {
                "reason": "new_tweet",
                "userinfo": {
                    "name": name,
                    "screen_name": screen_name
                },
                "user": screen_name
            },
            "data": {
                "id_str": data["id_str"],
                "full_text": data["full_text"],
                "created_at": data["created_at"],
                "extended_entities": {"media": data["extended_entities"]},
                "user": {
                    "name": name,
                    "screen_name": screen_name
                }
            }
        }

    async def make_send_replies(self, data, name, screen_name):
        """

        :param data:
        :param name:
        :param screen_name:
        :return:
        """
        return {
            "task": {
                "reason": "new_tweet",
                "userinfo": {
                    "name": name,
                    "screen_name": screen_name
                },
                "user": screen_name
            },
            "data": {
                "id_str": data["id_str"],
                "full_text": data["full_text"],
                "created_at": data["created_at"],
                "reply_status": {
                    "extended_entities": {"media": data["extended_entities"]}
                },
                "is_retweet": data["is_retweet"],
                "is_reply": True,
                "in_reply_to_status_id_str": data["in_reply_to_status_id_str"],
                "user": {
                    "name": name,
                    "screen_name": screen_name
                }
            }
        }

    async def parse_articles_replies(self, data, user_info):
        """

        :param data:
        :param user_info:
        :return:
        """
        name = user_info['name']
        screen_name = user_info['screen_name']
        data_result = data["data"]["user"]["result"]
        timeline = data_result.get("timeline_v2")
        if not timeline:
            timeline = data_result.get("timeline")
        instructions = timeline["timeline"]["instructions"][-1]
        entries = instructions.get("entries")
        if not entries:
            return
        try:
            for entrie in entries:
                id = entrie["sortIndex"]
                content = entrie["content"]
                items = content.get("itemContent")
                if not items:
                    items = content.get("items")
                if isinstance(items, list):
                    be_replay_article_data = None
                    replay_data = None
                    if len(items) > 1:
                        be_reply_item = items[0]
                        tweet_results = be_reply_item["item"]["itemContent"].get("tweet_results")
                        if tweet_results:
                            result = tweet_results["result"]
                            legacy = result.get("legacy")
                            if not legacy:
                                legacy = result["tweet"]["legacy"]
                            # 正常的被回复 推文 只提取媒体信息
                            be_replay_article_data = await self.parse_legacy(legacy, id, screen_name)

                    reply_item = items[-1]
                    tweet_results = reply_item["item"]["itemContent"].get("tweet_results")
                    if tweet_results:
                        result = tweet_results["result"]
                        legacy = result["legacy"]
                        if not legacy:
                            legacy = result["tweet"]["legacy"]
                        # 正常的回复
                        replay_data = await self.parse_legacy(legacy, id, screen_name)

                    if replay_data:
                        webhook_replay = await self.make_send_replies(replay_data, name, screen_name)
                        webhook_data = webhook_replay
                        if be_replay_article_data:
                            webhook_article = await self.make_send_article(be_replay_article_data, name, screen_name)
                            if len(webhook_article["data"]["extended_entities"]["media"]) > 0:
                                webhook_data["data"]["reply_status"]["extended_entities"]["media"].extend(
                                    webhook_article["data"]["extended_entities"]["media"])

                        yield ("reply", webhook_data)


                elif isinstance(items, dict):
                    # print("items", items)
                    quoted_article_data = None
                    quoted_replay_data = None
                    webhook_article_data = None
                    result = items["tweet_results"]["result"]
                    legacy = result.get("legacy")
                    if not legacy:
                        legacy = result["tweet"]["legacy"]

                    # 引用回复/正常推文
                    quoted_replay_data = await self.parse_legacy(legacy, id, screen_name)

                    if not quoted_replay_data.get("is_quote_status"):
                        # 正常推文
                        webhook_article_data = await self.make_send_article(quoted_replay_data, name, screen_name)
                        if webhook_article_data:
                            yield ("article", webhook_article_data)

                    else:
                        # 被引用推文 只提取媒体
                        quoted_status_result = result.get("quoted_status_result")
                        if quoted_status_result:
                            quoted_legacy_result = quoted_status_result["result"]

                            quoted_legacy = quoted_legacy_result.get("legacy")
                            if not quoted_legacy:
                                quoted_legacy = quoted_legacy_result["tweet"]["legacy"]

                            if not quoted_legacy:
                                quoted_legacy = result["tweet"]["legacy"]
                            quoted_article_data = await self.parse_legacy(quoted_legacy, id, screen_name)

                        # 被引用回复
                        if quoted_replay_data:
                            quoted_webhook_replay = await self.make_send_replies(quoted_replay_data, name, screen_name)
                            quoted_webhook_data = quoted_webhook_replay
                            if quoted_article_data:
                                quoted_webhook_article = await self.make_send_article(quoted_article_data, name,
                                                                                      screen_name)
                                if len(quoted_webhook_article["data"]["extended_entities"]["media"]) > 0:
                                    quoted_webhook_data["data"]["reply_status"]["extended_entities"]["media"].extend(
                                        quoted_webhook_article["data"]["extended_entities"]["media"])

                            yield ("reply", quoted_webhook_data)
        except Exception as e:
            print("entries", user_info, e, e.__traceback__.tb_lineno)

    async def make_send_to_tg(self, data, kind=""):
        """

        :param data:
        :param kind:
        :return:
        """
        _data = data["data"]
        user = _data["user"]

        if not _data.get("reply_status"):
            medias = len(_data["extended_entities"]["media"])
        else:
            medias = len(_data["reply_status"]["extended_entities"]["media"])

        return f"ScreenName:{user['screen_name']}\n" \
               f"类型:{kind}\n" \
               f"发布时间:{_data['created_at']}\n" \
               f"内容:{_data['full_text'][:101]}\n" \
               f"媒体链接:{medias}"
