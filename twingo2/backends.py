# -*- coding: utf-8 -*-

import tweepy
from tweepy.error import TweepError

from django.conf import settings

from twingo2.models import User


class TwitterBackend:
    """
    TwitterのOAuthを利用した認証バックエンド。
    ModelBackendの代替として設定することを想定している。
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
        oauth_handler = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        oauth_handler.set_access_token(access_token[0], access_token[1])
        api = tweepy.API(oauth_handler)

        # ログインユーザーのTwitter情報を取得する
        try:
            twitter_user = api.me()
        except TweepError:
            return None

        # ユーザー情報を取得する
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

        # ユーザーが有効であるかチェックする
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
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            return None
