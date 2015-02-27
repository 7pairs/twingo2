# -*- coding: utf-8 -*-

from nose.tools import *
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
        [対象] twitter_login()
        [条件] 次ページを指定せずにアクセスする。
        [結果] セッションにリクエストトークンが保管され、認証ページにリダイレクトされる。
        """
        oauth_handler.return_value.get_authorization_url.return_value = '/redirect/'
        oauth_handler.return_value.request_token = 'Request Token'

        response = self.client.get(reverse('twingo2_login'))
        session = self.client.session
        self.assertRedirects(response, '/redirect/')
        assert_equal('Request Token', session['request_token'])
        assert_equal(None, session.get('next'))

    @patch('twingo2.views.OAuthHandler')
    def test_twitter_login_02(self, oauth_handler):
        """
        [対象] twitter_login()
        [条件] 次ページを指定してアクセスする。
        [結果] セッションにリクエストトークン、次ページのURLが保管され、認証ページにリダイレクトされる。
        """
        oauth_handler.return_value.get_authorization_url.return_value = '/redirect/'
        oauth_handler.return_value.request_token = 'Request Token'

        response = self.client.get(reverse('twingo2_login'), {'next': '/next_page/'})
        session = self.client.session
        self.assertRedirects(response, '/redirect/')
        assert_equal('Request Token', session['request_token'])
        assert_equal('/next_page/', session.get('next'))

    @patch('twingo2.views.login')
    @patch('twingo2.views.authenticate')
    @patch('twingo2.views.OAuthHandler')
    def test_twitter_callback_01(self, oauth_handler, authenticate, login):
        """
        [対象] twitter_callback()
        [条件] ログイン後に遷移する画面を指定する。
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
        [対象] twitter_callback()
        [条件] ログイン後に遷移する画面を指定しない(settings.pyでは指定する)。
        [結果] settings.pyで指定された画面にリダイレクトされる。
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
        [対象] twitter_callback()
        [条件] ログイン後に遷移する画面を指定しない(settings.pyでも指定しない)。
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
        [対象] twitter_callback()
        [条件] リクエストトークンをセッションに設定しない。
        [結果] 401エラーが発生する。
        """
        response = self.client.get(reverse('twingo2_callback'), {'oauth_token': 'token', 'oauth_verifier': 'verifier'})
        assert_equal(401, response.status_code)

    def test_twitter_callback_05(self):
        """
        [対象] twitter_callback()
        [条件] セッション内のリクエストトークンとGETパラメータのリクエストトークンが異なる。
        [結果] 401エラーが発生する。
        """
        session = self.client.session
        session['request_token'] = {'oauth_token': 'error_token'}
        session.save()

        response = self.client.get(reverse('twingo2_callback'), {'oauth_token': 'token', 'oauth_verifier': 'verifier'})
        assert_equal(401, response.status_code)

    @patch('twingo2.views.authenticate')
    @patch('twingo2.views.OAuthHandler')
    def test_twitter_callback_06(self, oauth_handler, authenticate):
        """
        [対象] twitter_callback()
        [条件] 認証処理に失敗する。
        [結果] 401エラーが発生する。
        """
        authenticate.return_value = None

        session = self.client.session
        session['request_token'] = {'oauth_token': 'token'}
        session.save()

        response = self.client.get(reverse('twingo2_callback'), {'oauth_token': 'token', 'oauth_verifier': 'verifier'})
        assert_equal(401, response.status_code)

    @override_settings(AFTER_LOGOUT_URL='/after/')
    @patch('twingo2.views.logout')
    def test_twitter_logout_01(self, logout):
        """
        [対象] twitter_logout()
        [条件] ログイン後に遷移する画面をsettings.pyで指定する。
        [結果] settings.pyで指定された画面にリダイレクトされる。
        """
        response = self.client.get(reverse('twingo2_logout'))
        self.assertRedirects(response, '/after/')

    @patch('twingo2.views.logout')
    def test_twitter_logout_02(self, logout):
        """
        [対象] twitter_logout()
        [条件] ログイン後に遷移する画面をsettings.pyで指定しない。
        [結果] トップ画面にリダイレクトされる。
        """
        response = self.client.get(reverse('twingo2_logout'))
        self.assertRedirects(response, '/')
