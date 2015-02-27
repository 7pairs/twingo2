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

import factory
from nose.tools import *

from django.test import TestCase

from twingo2.models import User


class UserFactory(factory.DjangoModelFactory):
    """
    Userモデルを作成するファクトリー。
    """
    FACTORY_FOR = User
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


class ModelsTest(TestCase):
    """
    models.pyに対するテストコード。
    """

    def test_create_user_01(self):
        """
        [対象] create_user()
        [条件] 必須入力の項目のみを指定する。
        [結果] 一般ユーザーが作成される。
        """
        User.objects.create_user(
            twitter_id=1402804142,
            screen_name='7pairs',
            name='ちぃといつ'
        )

        user = User.objects.get(twitter_id=1402804142)
        assert_equal('7pairs', user.screen_name)
        assert_equal('ちぃといつ', user.name)
        assert_equal('', user.description)
        assert_equal('', user.location)
        assert_equal('', user.url)
        assert_equal('', user.profile_image_url)
        assert_equal(True, user.is_active)
        assert_equal(False, user.is_superuser)
        assert_equal(False, user.is_staff)

    def test_create_user_02(self):
        """
        [対象] create_user()
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
        assert_equal('7pairs', user.screen_name)
        assert_equal('ちぃといつ', user.name)
        assert_equal('This video has been deleted.', user.description)
        assert_equal('西武プリンスドーム', user.location)
        assert_equal('http://seven-pairs.hatenablog.jp/', user.url)
        assert_equal('https://pbs.twimg.com/profile_images/1402804142/icon_400x400.jpg', user.profile_image_url)
        assert_equal(True, user.is_active)
        assert_equal(False, user.is_superuser)
        assert_equal(False, user.is_staff)

    def test_create_superuser_01(self):
        """
        [対象] create_superuser()
        [条件] 必須入力の項目のみを指定する。
        [結果] 管理者ユーザーが作成される。
        """
        User.objects.create_superuser(
            twitter_id=1402804142,
            screen_name='7pairs',
            name='ちぃといつ'
        )

        user = User.objects.get(twitter_id=1402804142)
        assert_equal('7pairs', user.screen_name)
        assert_equal('ちぃといつ', user.name)
        assert_equal('', user.description)
        assert_equal('', user.location)
        assert_equal('', user.url)
        assert_equal('', user.profile_image_url)
        assert_equal(True, user.is_active)
        assert_equal(True, user.is_superuser)
        assert_equal(True, user.is_staff)

    def test_create_superuser_02(self):
        """
        [対象] create_superuser()
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
        assert_equal('7pairs', user.screen_name)
        assert_equal('ちぃといつ', user.name)
        assert_equal('This video has been deleted.', user.description)
        assert_equal('西武プリンスドーム', user.location)
        assert_equal('http://seven-pairs.hatenablog.jp/', user.url)
        assert_equal('https://pbs.twimg.com/profile_images/1402804142/icon_400x400.jpg', user.profile_image_url)
        assert_equal(True, user.is_active)
        assert_equal(True, user.is_superuser)
        assert_equal(True, user.is_staff)

    def test_get_full_name_01(self):
        """
        [対象] get_full_name()
        [条件] 実行する。
        [結果] ユーザー名と名前を結合した文字列を返す。
        """
        UserFactory(screen_name='screen_name01', name='ユーザー０１')

        user = User.objects.get(screen_name='screen_name01')
        assert_equal('screen_name01（ユーザー０１）', user.get_full_name())

    def test_get_short_name_01(self):
        """
        [対象] get_short_name()
        [条件] 実行する。
        [結果] ユーザー名を返す。
        """
        UserFactory(screen_name='screen_name01', name='ユーザー０１')

        user = User.objects.get(screen_name='screen_name01')
        assert_equal('screen_name01', user.get_short_name())
