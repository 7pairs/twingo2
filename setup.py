#!/usr/bin/env python
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

from setuptools import find_packages, setup

from twingo2 import __version__


setup(
    name='twingo2',
    version=__version__,
    description='Authentication application for Django on Python 3.x',
    author='Jun-ya HASEBA',
    author_email='7pairs@gmail.com',
    url='https://github.com/7pairs/twingo2',
    packages=find_packages(exclude=['tests']),
    install_requires=['tweepy>=3.0'],
)
