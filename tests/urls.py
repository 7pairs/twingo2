# -*- coding: utf-8 -*-

from django.conf.urls import include, patterns, url
from django.http import HttpResponse


urlpatterns = patterns('',
   (r'^twingo2/', include('twingo2.urls')),
   url(r'^$', 'tests.urls.top_page', name='top'),
   url(r'^redirect/$', 'tests.urls.redirect_page', name='redirect'),
   url(r'^next/$', 'tests.urls.next_page', name='next'),
   url(r'^after/$', 'tests.urls.after_page', name='after'),
)


def top_page(request):
    """
    ダミーのトップページ。
    """
    return HttpResponse('')


def redirect_page(request):
    """
    ダミーのリダイレクト先。
    """
    return HttpResponse('')


def next_page(request):
    """
    ダミーの次画面。
    """
    return HttpResponse('')


def after_page(request):
    """
    ダミーの処理後画面。
    """
    return HttpResponse('')
