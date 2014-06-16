# -*- coding: utf-8 -*-

"""
Twingoで利用する認証バックエンドを提供します。

@author: Jun-ya HASEBA
"""

from django.conf import settings

from twython import Twython, TwythonError

from twingo.models import User


class TwitterBackend:
    """
    TwitterのOAuthを利用した認証バックエンドです。
    django.contrib.auth.backends.ModelBackendの代替として使用してください。
    """

    def authenticate(self, tokens):
        """
        Twitterから取得したトークンをもとに認証を行います。

        @param tokens: Twitterから取得したトークン
        @type tokens: dict
        @return: 認証成功時は認証したユーザー。認証失敗時はNone。
        @rtype: twingo.models.User
        """
        # Twythonオブジェクトを生成
        twython = Twython(
            settings.TWITTER_API_KEY,
            settings.TWITTER_API_SECRET,
            tokens['oauth_token'],
            tokens['oauth_token_secret']
        )

        # Twitterプロフィールを取得
        try:
            profile = twython.verify_credentials()
            if not profile:
                return None
        except TwythonError:
            return None

        # DBからユーザーを取得/新規作成
        try:
            user = User.objects.get(twitter_id=profile['id'])
        except User.DoesNotExist:
            admin_twitter_id = getattr(settings, 'ADMIN_TWITTER_ID', None)
            if admin_twitter_id and profile['id'] in admin_twitter_id:
                user = User.objects.create_superuser(
                    profile['id'],
                    profile['screen_name'],
                    profile['name'],
                    profile['location'],
                    profile['url'],
                    profile['description'],
                    profile['profile_image_url']
                )
            else:
                user = User.objects.create_user(
                    profile['id'],
                    profile['screen_name'],
                    profile['name'],
                    profile['location'],
                    profile['url'],
                    profile['description'],
                    profile['profile_image_url']
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
