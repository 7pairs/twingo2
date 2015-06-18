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

from mock import patch

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings
from django.utils.importlib import import_module


class ViewsTest(TestCase):
    """
    views.pyに対するテストコード。
    """

    def setUp(self):
        """
        初期処理を実行する。
        """
        # クライアントを生成する
        self.client = Client()

        # クッキーを生成する
        engine = import_module(settings.SESSION_ENGINE)
        session = engine.SessionStore()
        session.save()
        session_cookie = settings.SESSION_COOKIE_NAME
        self.client.cookies[session_cookie] = session.session_key
        cookie_data = {
            'max-age': None,
            'path': '/',
            'domain': settings.SESSION_COOKIE_DOMAIN,
            'secure': settings.SESSION_COOKIE_SECURE or None,
            'expires': None,
        }
        self.client.cookies[session_cookie].update(cookie_data)

    @patch('twingo2.views.OAuthHandler')
    def test_twitter_login_01(self, oauth_handler):
        """
        [対象] twitter_login() : No.01
        [条件] 次ページを指定せずにアクセスする。
        [結果] セッションにリクエストトークンが保管され、認証ページにリダイレクトされる。
        """
        oauth_handler.return_value.get_authorization_url.return_value = '/redirect/'
        oauth_handler.return_value.request_token = 'Request Token'

        response = self.client.get(reverse('twingo2_login'))
        session = self.client.session
        self.assertRedirects(response, '/redirect/')
        self.assertEqual('Request Token', session['request_token'])
        self.assertIsNone(session.get('next'))

    @patch('twingo2.views.OAuthHandler')
    def test_twitter_login_02(self, oauth_handler):
        """
        [対象] twitter_login() : No.02
        [条件] 次ページを指定してアクセスする。
        [結果] セッションにリクエストトークンと次ページのURLが保管され、認証ページにリダイレクトされる。
        """
        oauth_handler.return_value.get_authorization_url.return_value = '/redirect/'
        oauth_handler.return_value.request_token = 'Request Token'

        response = self.client.get(reverse('twingo2_login'), {'next': '/next_page/'})
        session = self.client.session
        self.assertRedirects(response, '/redirect/')
        self.assertEqual('Request Token', session['request_token'])
        self.assertEqual('/next_page/', session['next'])

    @patch('twingo2.views.login')
    @patch('twingo2.views.authenticate')
    @patch('twingo2.views.OAuthHandler')
    def test_twitter_callback_01(self, oauth_handler, authenticate, login):
        """
        [対象] twitter_callback() : No.01
        [条件] ログイン後に遷移する画面をセッションで指定する。
        [結果] 指定された画面にリダイレクトされる。
        """
        authenticate.return_value = 'user'

        session = self.client.session
        session['request_token'] = {'oauth_token': 'token'}
        session['next'] = '/next/'
        session.save()

        response = self.client.get(reverse('twingo2_callback'), {'oauth_token': 'token', 'oauth_verifier': 'verifier'})
        self.assertRedirects(response, '/next/')

    @override_settings(AFTER_LOGIN_URL='/after/')
    @patch('twingo2.views.login')
    @patch('twingo2.views.authenticate')
    @patch('twingo2.views.OAuthHandler')
    def test_twitter_callback_02(self, oauth_handler, authenticate, login):
        """
        [対象] twitter_callback() : No.02
        [条件] ログイン後に遷移する画面をsettings.pyで指定する。
        [結果] 指定された画面にリダイレクトされる。
        """
        authenticate.return_value = 'user'

        session = self.client.session
        session['request_token'] = {'oauth_token': 'token'}
        session.save()

        response = self.client.get(reverse('twingo2_callback'), {'oauth_token': 'token', 'oauth_verifier': 'verifier'})
        self.assertRedirects(response, '/after/')

    @patch('twingo2.views.login')
    @patch('twingo2.views.authenticate')
    @patch('twingo2.views.OAuthHandler')
    def test_twitter_callback_03(self, oauth_handler, authenticate, login):
        """
        [対象] twitter_callback() : No.03
        [条件] ログイン後に遷移する画面を指定しない。
        [結果] トップ画面にリダイレクトされる。
        """
        authenticate.return_value = 'user'

        session = self.client.session
        session['request_token'] = {'oauth_token': 'token'}
        session.save()

        response = self.client.get(reverse('twingo2_callback'), {'oauth_token': 'token', 'oauth_verifier': 'verifier'})
        self.assertRedirects(response, '/')

    def test_twitter_callback_04(self):
        """
        [対象] twitter_callback() : No.04
        [条件] リクエストトークンをセッションに設定しない。
        [結果] 401エラーが発生する。
        """
        response = self.client.get(reverse('twingo2_callback'), {'oauth_token': 'token', 'oauth_verifier': 'verifier'})
        self.assertEqual(401, response.status_code)

    def test_twitter_callback_05(self):
        """
        [対象] twitter_callback() : No.05
        [条件] セッションに格納されたリクエストトークンとGETパラメータのリクエストトークンが異なる。
        [結果] 401エラーが発生する。
        """
        session = self.client.session
        session['request_token'] = {'oauth_token': 'error_token'}
        session.save()

        response = self.client.get(reverse('twingo2_callback'), {'oauth_token': 'token', 'oauth_verifier': 'verifier'})
        self.assertEqual(401, response.status_code)

    @patch('twingo2.views.authenticate')
    @patch('twingo2.views.OAuthHandler')
    def test_twitter_callback_06(self, oauth_handler, authenticate):
        """
        [対象] twitter_callback() : No.06
        [条件] 認証処理に失敗する。
        [結果] 401エラーが発生する。
        """
        authenticate.return_value = None

        session = self.client.session
        session['request_token'] = {'oauth_token': 'token'}
        session.save()

        response = self.client.get(reverse('twingo2_callback'), {'oauth_token': 'token', 'oauth_verifier': 'verifier'})
        self.assertEqual(401, response.status_code)

    @override_settings(AFTER_LOGOUT_URL='/after/')
    @patch('twingo2.views.logout')
    def test_twitter_logout_01(self, logout):
        """
        [対象] twitter_logout() : No.01
        [条件] ログイン後に遷移する画面をsettings.pyで指定する。
        [結果] 指定された画面にリダイレクトされる。
        """
        response = self.client.get(reverse('twingo2_logout'))
        self.assertRedirects(response, '/after/')

    @patch('twingo2.views.logout')
    def test_twitter_logout_02(self, logout):
        """
        [対象] twitter_logout() : No.02
        [条件] ログイン後に遷移する画面をsettings.pyで指定しない。
        [結果] トップ画面にリダイレクトされる。
        """
        response = self.client.get(reverse('twingo2_logout'))
        self.assertRedirects(response, '/')
