# -*- coding: utf-8 -*-

"""
Twingoで利用する認証バックエンドを提供します。

@author: Jun-ya HASEBA
"""

import tweepy
from tweepy.error import TweepError

from django.conf import settings

from twingo2.models import User


class TwitterBackend:
    """
    TwitterのOAuthを利用した認証バックエンドです。
    django.contrib.auth.backends.ModelBackendの代替として使用してください。
    """

    def authenticate(self, access_token):
        """
        Twitterから取得したトークンをもとに認証を行います。

        @param access_token: Twitterから取得したトークン
        @type access_token: tuple
        @return: 認証成功時は認証したユーザー。認証失敗時はNone。
        @rtype: twingo.models.User
        """
        # APIオブジェクトを構築する
        oauth_handler = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        oauth_handler.set_access_token(access_token[0], access_token[1])
        api = tweepy.API(oauth_handler)

        # ログインユーザーのTwitter情報を取得する
        try:
            twitter_user = api.me()
        except TweepError:
            return None

        # DBからユーザーを取得/新規作成
        try:
            user = User.objects.get(twitter_id=twitter_user.id)
        except User.DoesNotExist:
            admin_twitter_id = getattr(settings, 'ADMIN_TWITTER_ID', None)
            if admin_twitter_id and twitter_user.id in admin_twitter_id:
                user = User.objects.create_superuser(
                    twitter_user.id,
                    twitter_user.screen_name,
                    twitter_user.name,
                    twitter_user.location,
                    twitter_user.url,
                    twitter_user.description,
                    twitter_user.profile_image_url
                )
            else:
                user = User.objects.create_user(
                    twitter_user.id,
                    twitter_user.screen_name,
                    twitter_user.name,
                    twitter_user.location,
                    twitter_user.url,
                    twitter_user.description,
                    twitter_user.profile_image_url
                )

        # ユーザーを返す
        return user

    def get_user(self, user_id):
        """
        指定されたIDのユーザー情報を取得します。

        @param user_id: 取得するユーザーのID
        @type user_id: int
        @return: 該当するユーザー。取得できなかった場合はNone。
        @rtype: twingo.models.User
        """
        # ユーザーを取得
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            return None
