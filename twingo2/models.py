# -*- coding: utf-8 -*-

"""
Twingoで利用するモデルを提供します。

@author: Jun-ya HASEBA
"""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
    Userモデルを制御するマネージャーです。
    """

    def create_user(self, twitter_id, screen_name, name, location, url, description, profile_image_url):
        """
        新規ユーザーを作成します。

        @param twitter_id: Twitter ID
        @type twitter_id: int
        @param screen_name: ユーザー名
        @type screen_name: str
        @param name: 名前
        @type name: str
        @param location: 場所
        @type name: str
        @param url: ホームページ
        @type url: str
        @param description: 自己紹介
        @type description: str
        @param profile_image_url: 画像
        @type profile_image_url: str
        @return: 作成したユーザー
        @rtype: User
        """
        # 引数をチェック
        if not twitter_id or not screen_name or not name:
            raise ValueError()

        # 新規ユーザーを作成
        user = self.model()
        user.twitter_id = twitter_id
        user.screen_name = screen_name
        user.name = name
        user.location = location
        user.url = url
        user.description = description
        user.profile_image_url = profile_image_url
        user.is_admin = False
        user.save(using=self._db)

        # 作成したユーザーを返す
        return user

    def create_superuser(self, twitter_id, screen_name, name, location, url, description, profile_image_url):
        """
        管理者ユーザーを作成します。

        @param twitter_id: Twitter ID
        @type twitter_id: int
        @param screen_name: ユーザー名
        @type screen_name: str
        @param name: 名前
        @type name: str
        @param location: 場所
        @type name: str
        @param url: ホームページ
        @type url: str
        @param description: 自己紹介
        @type description: str
        @param profile_image_url: 画像
        @type profile_image_url: str
        @return: 作成したユーザー
        @rtype: User
        """
        # 新規ユーザーを作成
        user = self.create_user(twitter_id, screen_name, name, location, url, description, profile_image_url)
        user.is_admin = True
        user.save(using=self._db)

        # 作成したユーザーを返す
        return user


class User(AbstractBaseUser):
    """
    ユーザー情報を格納するテーブルです。
    """

    twitter_id = models.IntegerField('Twitter ID', db_index=True, unique=True)
    """Twitter ID"""

    screen_name = models.CharField('ユーザー名', max_length=15)
    """ユーザー名"""

    name = models.CharField('名前', max_length=20)
    """名前"""

    location = models.CharField('場所', max_length=30, blank=True)
    """場所"""

    url = models.URLField('ホームページ', blank=True)
    """ホームページ"""

    description = models.CharField('自己紹介', max_length=160, blank=True)
    """自己紹介"""

    profile_image_url = models.URLField('画像', blank=True)
    """画像"""

    is_admin = models.BooleanField('管理者')
    """管理者"""

    created_at = models.DateTimeField('登録日時', auto_now_add=True)
    """登録日時"""

    updated_at = models.DateTimeField('更新日時', auto_now=True)
    """更新日時"""

    objects = UserManager()
    """マネージャー"""

    USERNAME_FIELD = 'twitter_id'
    """usernameとして使用するフィールド"""
