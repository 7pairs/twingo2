# -*- coding: utf-8 -*-

"""
Twingoで利用するビューを提供します。

@author: Jun-ya HASEBA
"""

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect

from twython import Twython


def twitter_login(request):
    """
    ログインURLへのアクセス時に呼び出されます。

    @param request: リクエストオブジェクト
    @type request: django.http.HttpRequest
    @return: 遷移先を示すレスポンスオブジェクト
    @rtype: django.http.HttpResponse
    """
    # TwitterからのコールバックURLを取得
    callback_url = getattr(settings, 'TWITTER_CALLBACK_URL', None)
    if not callback_url:
        callback_url = 'http://%s/callback/' % request.META.get('HTTP_HOST', 'localhost')

    # 認証トークンを取得
    twython = Twython(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET)
    tokens = twython.get_authentication_tokens(callback_url=callback_url)

    # 認証トークンをセッションに保存
    request.session['oauth_token'] = tokens['oauth_token']
    request.session['oauth_token_secret'] = tokens['oauth_token_secret']

    # ログイン後のリダイレクト先URLをセッションに保存
    if 'next' in request.GET:
        request.session['next'] = request.GET['next']

    # 認証URLにリダイレクト
    return HttpResponseRedirect(tokens['auth_url'])


def twitter_logout(request):
    """
    ログアウトURLへのアクセス時に呼び出されます。

    @param request: リクエストオブジェクト
    @type request: django.http.HttpRequest
    @return: 遷移先を示すレスポンスオブジェクト
    @rtype: django.http.HttpResponse
    """
    # ログアウト処理
    logout(request)

    # トップページにリダイレクト
    top_url = getattr(settings, 'TOP_URL', '/')
    return HttpResponseRedirect(top_url)


def twitter_callback(request):
    """
    Twitterからのコールバック時に呼び出されます。

    @param request: リクエストオブジェクト
    @type request: django.http.HttpRequest
    @return: 遷移先を示すレスポンスオブジェクト
    @rtype: django.http.HttpResponse
    """
    # セッションからトークンを取得
    oauth_token = request.session.get('oauth_token')
    oauth_token_secret = request.session.get('oauth_token_secret')
    if not oauth_token or not oauth_token_secret:
        request.session.clear()
        raise PermissionDenied

    # セッションの値とTwitterからの返却値が一致しない場合は処理続行不可能
    if oauth_token != request.GET.get('oauth_token'):
        request.session.clear()
        raise PermissionDenied

    # 認証トークンを取得
    twython = Twython(
        settings.TWITTER_API_KEY,
        settings.TWITTER_API_SECRET,
        oauth_token,
        oauth_token_secret
    )
    oauth_verifier = request.GET.get('oauth_verifier')
    tokens = twython.get_authorized_tokens(oauth_verifier)

    # 認証処理
    authenticated_user = authenticate(tokens=tokens)

    # ログイン処理
    if authenticated_user:
        login(request, authenticated_user)
    else:
        request.session.clear()
        raise PermissionDenied

    # 認証成功
    if 'next' in request.session:
        next_url = request.session.pop('next')
    else:
        next_url = getattr(settings, 'TOP_URL', '/')
    return HttpResponseRedirect(next_url)
