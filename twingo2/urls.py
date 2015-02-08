# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('twingo2.views',
    # ログイン
    url(r'^login/$', 'twitter_login', name='twingo2_login'),

    # Twitterからのコールバック
    url(r'^callback/$', 'twitter_callback', name='twingo2_callback'),

    # ログアウト
    url(r'^logout/$', 'twitter_logout', name='twingo2_logout'),
)
