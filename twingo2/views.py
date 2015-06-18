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

from tweepy import OAuthHandler

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect


def twitter_login(request):
    """
    ログインを行う。

    :param request: リクエストオブジェクト
    :type request: django.http.HttpRequest
    :return: 遷移先を示すレスポンスオブジェクト
    :rtype: django.http.HttpResponse
    """
    # 認証URLを取得する
    oauth_handler = OAuthHandler(
        settings.CONSUMER_KEY,
        settings.CONSUMER_SECRET,
        request.build_absolute_uri(reverse(twitter_callback))
    )
    authorization_url = oauth_handler.get_authorization_url()

    # リクエストトークンをセッションに保存する
    request.session['request_token'] = oauth_handler.request_token

    # ログイン完了後のリダイレクト先URLをセッションに保存する
    if 'next' in request.GET:
        request.session['next'] = request.GET['next']

    # 認証URLにリダイレクトする
    return HttpResponseRedirect(authorization_url)


def twitter_callback(request):
    """
    Twitterからのコールバック時に呼び出される。

    :param request: リクエストオブジェクト
    :type request: django.http.HttpRequest
    :return: 遷移先を示すレスポンスオブジェクト
    :rtype: django.http.HttpResponse
    """
    # セッションからリクエストトークンを取得する
    request_token = request.session.get('request_token')
    if not request_token:
        request.session.clear()
        return HttpResponse('Unauthorized', status=401)

    # Twitterからの返却値を取得する
    oauth_token = request.GET.get('oauth_token')
    oauth_verifier = request.GET.get('oauth_verifier')

    # セッションの値とTwitterからの返却値が一致しない場合は処理を中断する
    if request_token.get('oauth_token') != oauth_token:
        request.session.clear()
        return HttpResponse('Unauthorized', status=401)

    # アクセストークンを取得する
    oauth_handler = OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    oauth_handler.request_token = request_token
    access_token = oauth_handler.get_access_token(oauth_verifier)

    # 認証処理を実行する
    authenticated_user = authenticate(access_token=access_token)
    if authenticated_user:
        login(request, authenticated_user)
    else:
        request.session.clear()
        return HttpResponse('Unauthorized', status=401)

    # ログイン後に遷移すべき画面にリダイレクトする
    url = request.session.get('next', getattr(settings, 'AFTER_LOGIN_URL', '/'))
    return HttpResponseRedirect(url)


def twitter_logout(request):
    """
    ログアウトを行う。

    :param request: リクエストオブジェクト
    :type request: django.http.HttpRequest
    :return: 遷移先を示すレスポンスオブジェクト
    :rtype: django.http.HttpResponse
    """
    # ログアウト処理を実行する
    logout(request)

    # ログアウト後に遷移すべき画面にリダイレクトする
    url = getattr(settings, 'AFTER_LOGOUT_URL', '/')
    return HttpResponseRedirect(url)
