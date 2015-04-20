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
