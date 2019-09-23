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

import factory

from django.test import TestCase

from twingo2.models import User


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


class UserManagerTest(TestCase):
    """
    models.UserManagerに対するテストコード。
    """

    def test_create_user_01(self):
        """
        [対象] create_user() : No.01
        [条件] 必須入力の項目のみを指定する。
        [結果] 一般ユーザーが作成される。
        """
        User.objects.create_user(
            twitter_id=1402804142,
            screen_name='7pairs',
            name='ちぃといつ'
        )

        user = User.objects.get(twitter_id=1402804142)
        self.assertEqual('7pairs', user.screen_name)
        self.assertEqual('ちぃといつ', user.name)
        self.assertEqual('', user.description)
        self.assertEqual('', user.location)
        self.assertEqual('', user.url)
        self.assertEqual('', user.profile_image_url)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_user_02(self):
        """
        [対象] create_user() : No.02
        [条件] 任意入力の項目を指定する。
        [結果] 一般ユーザーが作成される。
        """
        User.objects.create_user(
            twitter_id=1402804142,
            screen_name='7pairs',
            name='ちぃといつ',
            description='This video has been deleted.',
            location='西武プリンスドーム',
            url='http://seven-pairs.hatenablog.jp/',
            profile_image_url='https://pbs.twimg.com/profile_images/1402804142/icon_400x400.jpg'
        )

        user = User.objects.get(twitter_id=1402804142)
        self.assertEqual('7pairs', user.screen_name)
        self.assertEqual('ちぃといつ', user.name)
        self.assertEqual('This video has been deleted.', user.description)
        self.assertEqual('西武プリンスドーム', user.location)
        self.assertEqual('http://seven-pairs.hatenablog.jp/', user.url)
        self.assertEqual('https://pbs.twimg.com/profile_images/1402804142/icon_400x400.jpg', user.profile_image_url)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_user_03(self):
        """
        [対象] create_user() : No.03
        [条件] Twitter IDを指定しない。
        [結果] ValueErrorが送出される。
        """
        with self.assertRaises(ValueError):
            User.objects.create_user(
                twitter_id=None,
                screen_name='7pairs',
                name='ちぃといつ'
            )

    def test_create_user_04(self):
        """
        [対象] create_user() : No.04
        [条件] ユーザー名を指定しない。
        [結果] ValueErrorが送出される。
        """
        with self.assertRaises(ValueError):
            User.objects.create_user(
                twitter_id=1402804142,
                screen_name=None,
                name='ちぃといつ'
            )

    def test_create_user_05(self):
        """
        [対象] create_user() : No.05
        [条件] 名前を指定しない。
        [結果] ValueErrorが送出される。
        """
        with self.assertRaises(ValueError):
            User.objects.create_user(
                twitter_id=1402804142,
                screen_name='7pairs',
                name=None
            )

    def test_create_superuser_01(self):
        """
        [対象] create_superuser() : No.01
        [条件] 必須入力の項目のみを指定する。
        [結果] 管理者ユーザーが作成される。
        """
        User.objects.create_superuser(
            twitter_id=1402804142,
            screen_name='7pairs',
            name='ちぃといつ'
        )

        user = User.objects.get(twitter_id=1402804142)
        self.assertEqual('7pairs', user.screen_name)
        self.assertEqual('ちぃといつ', user.name)
        self.assertEqual('', user.description)
        self.assertEqual('', user.location)
        self.assertEqual('', user.url)
        self.assertEqual('', user.profile_image_url)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_superuser_02(self):
        """
        [対象] create_superuser() : No.02
        [条件] 任意入力の項目を指定する。
        [結果] 管理者ユーザーが作成される。
        """
        User.objects.create_superuser(
            twitter_id=1402804142,
            screen_name='7pairs',
            name='ちぃといつ',
            description='This video has been deleted.',
            location='西武プリンスドーム',
            url='http://seven-pairs.hatenablog.jp/',
            profile_image_url='https://pbs.twimg.com/profile_images/1402804142/icon_400x400.jpg'
        )

        user = User.objects.get(twitter_id=1402804142)
        self.assertEqual('7pairs', user.screen_name)
        self.assertEqual('ちぃといつ', user.name)
        self.assertEqual('This video has been deleted.', user.description)
        self.assertEqual('西武プリンスドーム', user.location)
        self.assertEqual('http://seven-pairs.hatenablog.jp/', user.url)
        self.assertEqual('https://pbs.twimg.com/profile_images/1402804142/icon_400x400.jpg', user.profile_image_url)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_superuser_03(self):
        """
        [対象] create_superuser() : No.03
        [条件] Twitter IDを指定しない。
        [結果] ValueErrorが送出される。
        """
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                twitter_id=None,
                screen_name='7pairs',
                name='ちぃといつ'
            )

    def test_create_superuser_04(self):
        """
        [対象] create_superuser() : No.04
        [条件] ユーザー名を指定しない。
        [結果] ValueErrorが送出される。
        """
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                twitter_id=1402804142,
                screen_name=None,
                name='ちぃといつ'
            )

    def test_create_superuser_05(self):
        """
        [対象] create_superuser() : No.05
        [条件] 名前を指定しない。
        [結果] ValueErrorが送出される。
        """
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                twitter_id=1402804142,
                screen_name='7pairs',
                name=None
            )


class UserTest(TestCase):
    """
    models.Userに対するテストコード。
    """

    def test_str_01(self):
        """
        [対象] __str__() : No.01
        [条件] 実行する。
        [結果] Twitter IDの文字列表現が返却される。
        """
        UserFactory(twitter_id=12345, screen_name='screen_name01', name='ユーザー０１')

        user = User.objects.get(screen_name='screen_name01')
        actual = str(user)
        self.assertEqual('12345', actual)

    def test_get_full_name_01(self):
        """
        [対象] get_full_name() : No.01
        [条件] 実行する。
        [結果] ユーザー名と名前を結合した文字列が返却される。
        """
        UserFactory(twitter_id=12345, screen_name='screen_name01', name='ユーザー０１')

        user = User.objects.get(twitter_id=12345)
        actual = user.get_full_name()
        self.assertEqual('screen_name01（ユーザー０１）', actual)

    def test_get_short_name_01(self):
        """
        [対象] get_short_name() : No.01
        [条件] 実行する。
        [結果] ユーザー名が返却される。
        """
        UserFactory(twitter_id=12345, screen_name='screen_name01', name='ユーザー０１')

        user = User.objects.get(twitter_id=12345)
        actual = user.get_short_name()
        self.assertEqual('screen_name01', actual)
