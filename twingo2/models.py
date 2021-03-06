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

import datetime

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
    Userモデルを制御するマネージャー。
    """

    def create_user(self, twitter_id, screen_name, name, **extra_fields):
        """
        新規ユーザー(一般)を作成する。

        :param twitter_id: Twitter ID
        :type twitter_id: int
        :param screen_name: ユーザー名
        :type screen_name: str
        :param name: 名前
        :type name: str
        :param extra_fields: 任意入力のフィールド
        :type extra_fields: dict
        :return: 作成したユーザー
        :rtype: User
        """
        # 新規ユーザー(一般)を作成する
        return self._create_user(twitter_id, screen_name, name, False, False, **extra_fields)

    def create_superuser(self, twitter_id, screen_name, name, **extra_fields):
        """
        新規ユーザー(管理者)を作成する。

        :param twitter_id: Twitter ID
        :type twitter_id: int
        :param screen_name: ユーザー名
        :type screen_name: str
        :param name: 名前
        :type name: str
        :param extra_fields: 任意入力のフィールド
        :type extra_fields: dict
        :return: 作成したユーザー
        :rtype: User
        """
        # 新規ユーザー(管理者)を作成する
        return self._create_user(twitter_id, screen_name, name, True, True, **extra_fields)

    def _create_user(self, twitter_id, screen_name, name, is_superuser, is_staff, **extra_fields):
        """
        新規ユーザーを作成する。

        :param twitter_id: Twitter ID
        :type twitter_id: int
        :param screen_name: ユーザー名
        :type screen_name: str
        :param name: 名前
        :type name: str
        :param is_superuser: 管理者権限
        :type is_superuser: bool
        :param is_staff: 管理画面操作権限
        :type is_staff: bool
        :param extra_fields: 任意入力のフィールド
        :type extra_fields: dict
        :return: 作成したユーザー
        :rtype: User
        """
        # 引数をチェックする
        if not twitter_id or not screen_name or not name:
            raise ValueError('twitter_id and screen_name and name are required.')

        # 新規ユーザーを作成する
        user = self.model(
            twitter_id=twitter_id,
            screen_name=screen_name,
            name=name,
            is_active=True,
            is_superuser=is_superuser,
            is_staff=is_staff,
            last_login=datetime.datetime.now(),
            **extra_fields
        )
        user.set_unusable_password()
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    ユーザー情報を格納するモデル。
    """

    twitter_id = models.IntegerField('Twitter ID', unique=True)
    """Twitter ID"""

    screen_name = models.CharField('ユーザー名', max_length=15)
    """ユーザー名"""

    name = models.CharField('名前', max_length=20)
    """名前"""

    description = models.CharField('自己紹介', max_length=160, blank=True)
    """自己紹介"""

    location = models.CharField('場所', max_length=30, blank=True)
    """場所"""

    url = models.URLField('ホームページ', blank=True)
    """ホームページのURL"""

    profile_image_url = models.URLField('プロフィール画像', blank=True)
    """プロフィール画像のURL"""

    is_active = models.BooleanField('有効', default=False)
    """有効"""

    is_superuser = models.BooleanField('管理者権限', default=False)
    """管理者権限"""

    is_staff = models.BooleanField('管理画面操作権限', default=False)
    """管理画面操作権限"""

    created_at = models.DateTimeField('登録日時', auto_now_add=True)
    """登録日時"""

    updated_at = models.DateTimeField('更新日時', auto_now=True)
    """更新日時"""

    objects = UserManager()
    """マネージャー"""

    USERNAME_FIELD = 'twitter_id'
    """Twitter IDをusernameとして使用する"""

    def __str__(self):
        """
        当モデルの文字列表現を取得する。

        :return: モデルの文字列表現
        :rtype: str
        """
        # Twitter IDを返す
        return str(self.twitter_id)

    def get_full_name(self):
        """
        フルネームを取得する。

        :return: フルネーム
        :rtype: str
        """
        # ユーザー名と名前を返す
        return '%s（%s）' % (self.screen_name, self.name)

    def get_short_name(self):
        """
        短縮名を取得する。

        :return: 短縮名
        :rtype: str
        """
        # ユーザー名を返す
        return self.screen_name
