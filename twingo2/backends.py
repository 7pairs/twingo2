# -*- coding: utf-8 -*-

#
# Copyright 2015-2019 HASEBA Junya
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from tweepy import API, OAuthHandler
from tweepy.error import TweepError

from django.conf import settings

from twingo2.models import User


class TwitterBackend:
    """
    TwitterのOAuthを利用した認証バックエンド。
    ModelBackendの代替として使用することを想定している。
    """

    def authenticate(self, access_token):
        """
        Twitterから取得したアクセストークンをもとに認証を行う。

        :param access_token: アクセストークン
        :type access_token: tuple
        :return: ユーザー情報
        :rtype: twingo2.models.User
        """
        # APIオブジェクトを構築する
        oauth_handler = OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        oauth_handler.set_access_token(access_token[0], access_token[1])
        api = API(oauth_handler)

        # ログインユーザーのTwitter情報を取得する
        try:
            twitter_user = api.me()
        except TweepError:
            return None

        # Userを取得/作成する
        try:
            user = User.objects.get(twitter_id=twitter_user.id)
        except User.DoesNotExist:
            admin_twitter_id = getattr(settings, 'ADMIN_TWITTER_ID', ())
            if twitter_user.id in admin_twitter_id:
                # 管理者ユーザーを作成する
                user = User.objects.create_superuser(
                    twitter_id=twitter_user.id,
                    screen_name=twitter_user.screen_name,
                    name=twitter_user.name,
                    description=twitter_user.description,
                    location=twitter_user.location,
                    url=twitter_user.url,
                    profile_image_url=twitter_user.profile_image_url
                )
            else:
                # 一般ユーザーを作成する
                user = User.objects.create_user(
                    twitter_id=twitter_user.id,
                    screen_name=twitter_user.screen_name,
                    name=twitter_user.name,
                    description=twitter_user.description,
                    location=twitter_user.location,
                    url=twitter_user.url,
                    profile_image_url=twitter_user.profile_image_url
                )

        # 有効なユーザーであるかチェックする
        if user.is_active:
            return user
        else:
            return None

    def get_user(self, user_id):
        """
        指定されたIDのユーザー情報を取得する。

        :param user_id: UserのID
        :type user_id: int
        :return: ユーザー情報
        :rtype: twingo2.models.User
        """
        # ユーザー情報を取得する
        try:
            user = User.objects.get(pk=user_id, is_active=True)
            return user
        except User.DoesNotExist:
            return None
