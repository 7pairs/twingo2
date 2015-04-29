# -*- coding: utf-8 -*-

#
# Copyright 2015 Jun-ya HASEBA
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
from mock import patch

import factory
from tweepy.error import TweepError

from django.test import TestCase
from django.test.utils import override_settings

from twingo2.models import User


class TwitterUser:
    """
    Twitterのユーザー情報を格納するテスト用クラス。
    """

    def __init__(self, **kwargs):
        """
        TwitterUserを構築する。

        :param kwargs: 設定するプロパティ名とその値
        :type kwargs: dict
        """
        # プロパティを設定する
        for k, v in kwargs.items():
            setattr(self, k, v)


class UserFactory(factory.DjangoModelFactory):
    """
    Userのテストデータを作成するファクトリー。
    """

    class Meta:
        model = User

    twitter_id = factory.Sequence(lambda x: x)
    screen_name = factory.Sequence(lambda x: 'screen_name_%02d' % x)
    name = factory.Sequence(lambda x: 'name_%02d' % x)
    description = factory.Sequence(lambda x: 'description_%02d' % x)
    location = factory.Sequence(lambda x: 'location_%02d' % x)
    url = factory.Sequence(lambda x: 'http://dummy.com/user_%02d.html' % x)
    profile_image_url = factory.Sequence(lambda x: 'http://dummy.com/user_%02d.jpg' % x)
    is_active = True
    is_superuser = False
    is_staff = False
    last_login = datetime.datetime.now()


class DisableUserFactory(UserFactory):
    """
    無効なユーザーを表すUserのテストデータを作成するファクトリー。
    """
    is_active = False


class BackendsTest(TestCase):
    """
    backends.pyに対するテストコード。
    """

    def _get_twitter_backend(self):
        """
        新しいTwitterBackendオブジェクトを取得する。

        :return: TwitterBackendオブジェクト
        :rtype: twingo2.backends.TwitterBackend
        """
        # TwitterBackendオブジェクトを返す
        from twingo2.backends import TwitterBackend
        return TwitterBackend()

    @patch('twingo2.backends.API')
    @patch('twingo2.backends.OAuthHandler')
    def test_authenticate_01(self, oauth_handler, api):
        """
        [対象] TwitterBackend.authenticate()
        [条件] 新規ユーザー(一般)でログインする。
        [結果] ユーザーの情報がデータベースに保存され、該当ユーザーのUserオブジェクトが返される。
        """
        api.return_value.me.return_value = TwitterUser(
            id=1402804142,
            screen_name='7pairs',
            name='Jun-ya HASEBA',
            description='This video has been deleted.',
            location='Seibu Prince Dome',
            url='http://seven-pairs.hatenablog.jp/',
            profile_image_url='https://pbs.twimg.com/profile_images/1402804142/icon_400x400.jpg'
        )

        twitter_backend = self._get_twitter_backend()
        actual = twitter_backend.authenticate(('key', 'secret'))

        user = User.objects.get(twitter_id=1402804142)
        self.assertEqual(user, actual)
        self.assertEqual('7pairs', user.screen_name)
        self.assertEqual('Jun-ya HASEBA', user.name)
        self.assertEqual('This video has been deleted.', user.description)
        self.assertEqual('Seibu Prince Dome', user.location)
        self.assertEqual('http://seven-pairs.hatenablog.jp/', user.url)
        self.assertEqual('https://pbs.twimg.com/profile_images/1402804142/icon_400x400.jpg', user.profile_image_url)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    @override_settings(ADMIN_TWITTER_ID=(1402804142,))
    @patch('twingo2.backends.API')
    @patch('twingo2.backends.OAuthHandler')
    def test_authenticate_02(self, oauth_handler, api):
        """
        [対象] TwitterBackend.authenticate()
        [条件] 新規ユーザー(管理者)でログインする。
        [結果] ユーザーの情報がデータベースに保存され、該当ユーザーのUserオブジェクトが返される。
        """
        api.return_value.me.return_value = TwitterUser(
            id=1402804142,
            screen_name='7pairs',
            name='Jun-ya HASEBA',
            description='This video has been deleted.',
            location='Seibu Prince Dome',
            url='http://seven-pairs.hatenablog.jp/',
            profile_image_url='https://pbs.twimg.com/profile_images/1402804142/icon_400x400.jpg'
        )

        twitter_backend = self._get_twitter_backend()
        actual = twitter_backend.authenticate(('key', 'secret'))

        user = User.objects.get(twitter_id=1402804142)
        self.assertEqual(user, actual)
        self.assertEqual('7pairs', user.screen_name)
        self.assertEqual('Jun-ya HASEBA', user.name)
        self.assertEqual('This video has been deleted.', user.description)
        self.assertEqual('Seibu Prince Dome', user.location)
        self.assertEqual('http://seven-pairs.hatenablog.jp/', user.url)
        self.assertEqual('https://pbs.twimg.com/profile_images/1402804142/icon_400x400.jpg', user.profile_image_url)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    @patch('twingo2.backends.API')
    @patch('twingo2.backends.OAuthHandler')
    def test_authenticate_03(self, oauth_handler, api):
        """
        [対象] TwitterBackend.authenticate()
        [条件] 既存ユーザーでログインする。
        [結果] 該当ユーザーのUserオブジェクトが返される。
        """
        user = UserFactory()
        api.return_value.me.return_value = TwitterUser(id=user.twitter_id)

        twitter_backend = self._get_twitter_backend()
        actual = twitter_backend.authenticate(('key', 'secret'))

        self.assertEqual(user, actual)

    @patch('twingo2.backends.API')
    @patch('twingo2.backends.OAuthHandler')
    def test_authenticate_04(self, oauth_handler, api):
        """
        [対象] TwitterBackend.authenticate()
        [条件] 無効なユーザーでログインする。
        [結果] Noneが返される。
        """
        user = DisableUserFactory()
        api.return_value.me.return_value = TwitterUser(id=user.twitter_id)

        twitter_backend = self._get_twitter_backend()
        actual = twitter_backend.authenticate(('key', 'secret'))

        self.assertIsNone(actual)

    @patch('twingo2.backends.API')
    @patch('twingo2.backends.OAuthHandler')
    def test_authenticate_05(self, oauth_handler, api):
        """
        [対象] TwitterBackend.authenticate()
        [条件] Twitterからエラーが返される。
        [結果] Noneが返される。
        """
        api.return_value.me.side_effect = TweepError('reason')

        twitter_backend = self._get_twitter_backend()
        actual = twitter_backend.authenticate(('key', 'secret'))

        self.assertIsNone(actual)

    def test_get_user_01(self):
        """
        [対象] TwitterBackend.get_user()
        [条件] 既存ユーザーのIDを指定する。
        [結果] 該当ユーザーのUserオブジェクトが返される。
        """
        user = UserFactory()

        twitter_backend = self._get_twitter_backend()
        actual = twitter_backend.get_user(user.id)

        self.assertEqual(user, actual)

    def test_get_user_02(self):
        """
        [対象] TwitterBackend.get_user()
        [条件] 存在しないユーザーのIDを指定する。
        [結果] Noneが返される。
        """
        user = UserFactory()

        twitter_backend = self._get_twitter_backend()
        actual = twitter_backend.get_user(user.id + 1)

        self.assertIsNone(actual)

    def test_get_user_03(self):
        """
        [対象] TwitterBackend.get_user()
        [条件] 無効なユーザーのIDを指定する。
        [結果] Noneが返される。
        """
        user = DisableUserFactory()

        twitter_backend = self._get_twitter_backend()
        actual = twitter_backend.get_user(user.id)

        self.assertIsNone(actual)
