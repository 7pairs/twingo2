# -*- coding: utf-8 -*-

from nose.tools import *
from mock import patch

import factory
from tweepy.error import TweepError

from django.test import TestCase
from django.test.utils import override_settings

from twingo2.backends import TwitterBackend
from twingo2.models import User


class TwitterUser:
    """
    Twitterのユーザー情報を格納するテスト用クラス。
    """

    def __init__(self, **kwargs):
        """
        TwitterUserを構築する。
        :param kwargs: 設定するプロパティとその値
        :type kwargs: dict
        """
        # プロパティを設定する
        for k, v in kwargs.items():
            setattr(self, k, v)


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


class DisableUserFactory(UserFactory):
    """
    無効なユーザーのUserモデルを作成するファクトリー。
    """
    is_active = False


class BackendsTest(TestCase):
    """
    backends.pyに対するテストコード。
    """

    @patch('twingo2.backends.API')
    @patch('twingo2.backends.OAuthHandler')
    def test_authenticate_01(self, oauth_handler, api):
        """
        [対象] TwitterBackend.authenticate()
        [条件] 新規ユーザーでログインする。
        [結果] ユーザーの情報がデータベースに登録され、該当ユーザーのUserオブジェクトが返される。
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

        twitter_backend = TwitterBackend()
        actual = twitter_backend.authenticate(('key', 'secret'))

        user = User.objects.get(twitter_id=1402804142)
        assert_equal('7pairs', user.screen_name)
        assert_equal('Jun-ya HASEBA', user.name)
        assert_equal('This video has been deleted.', user.description)
        assert_equal('Seibu Prince Dome', user.location)
        assert_equal('http://seven-pairs.hatenablog.jp/', user.url)
        assert_equal('https://pbs.twimg.com/profile_images/1402804142/icon_400x400.jpg', user.profile_image_url)
        assert_equal(True, user.is_active)
        assert_equal(False, user.is_superuser)
        assert_equal(False, user.is_staff)
        assert_equal(user, actual)

    @override_settings(ADMIN_TWITTER_ID=(1402804142,))
    @patch('twingo2.backends.API')
    @patch('twingo2.backends.OAuthHandler')
    def test_authenticate_02(self, oauth_handler, api):
        """
        [対象] TwitterBackend.authenticate()
        [条件] 新規管理者ユーザーでログインする。
        [結果] ユーザーの情報がデータベースに登録され、該当ユーザーのUserオブジェクトが返される。
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

        twitter_backend = TwitterBackend()
        actual = twitter_backend.authenticate(('key', 'secret'))

        user = User.objects.get(twitter_id=1402804142)
        assert_equal('7pairs', user.screen_name)
        assert_equal('Jun-ya HASEBA', user.name)
        assert_equal('This video has been deleted.', user.description)
        assert_equal('Seibu Prince Dome', user.location)
        assert_equal('http://seven-pairs.hatenablog.jp/', user.url)
        assert_equal('https://pbs.twimg.com/profile_images/1402804142/icon_400x400.jpg', user.profile_image_url)
        assert_equal(True, user.is_active)
        assert_equal(True, user.is_superuser)
        assert_equal(True, user.is_staff)
        assert_equal(user, actual)

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

        twitter_backend = TwitterBackend()
        actual = twitter_backend.authenticate(('key', 'secret'))

        assert_equal(user, actual)

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

        twitter_backend = TwitterBackend()
        actual = twitter_backend.authenticate(('key', 'secret'))

        assert_equal(None, actual)

    @patch('twingo2.backends.API')
    @patch('twingo2.backends.OAuthHandler')
    def test_authenticate_05(self, oauth_handler, api):
        """
        [対象] TwitterBackend.authenticate()
        [条件] Twitterからエラーが返る。
        [結果] Noneが返される。
        """
        api.return_value.me.side_effect = TweepError('reason')

        twitter_backend = TwitterBackend()
        actual = twitter_backend.authenticate(('key', 'secret'))

        assert_equal(None, actual)

    def test_get_user_01(self):
        """
        [対象] TwitterBackend.get_user()
        [条件] 存在するユーザーのIDを指定する。
        [結果] 該当ユーザーのUserオブジェクトが返される。
        """
        user = UserFactory()

        twitter_backend = TwitterBackend()
        actual = twitter_backend.get_user(user.id)

        assert_equal(user, actual)

    def test_get_user_02(self):
        """
        [対象] TwitterBackend.get_user()
        [条件] 存在しないユーザーのIDを指定する。
        [結果] Noneが返される。
        """
        user = UserFactory()

        twitter_backend = TwitterBackend()
        actual = twitter_backend.get_user(user.id + 1)

        assert_equal(None, actual)

    def test_get_user_03(self):
        """
        [対象] TwitterBackend.get_user()
        [条件] 無効なユーザーのIDを指定する。
        [結果] Noneが返される。
        """
        user = DisableUserFactory()

        twitter_backend = TwitterBackend()
        actual = twitter_backend.get_user(user.id)

        assert_equal(None, actual)
