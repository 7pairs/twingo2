# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

from twingo2 import __version__


setup(
    name='twingo2',
    version=__version__,
    description='Authentication application for Django on Python 3.x',
    author='Jun-ya HASEBA',
    author_email='7pairs@gmail.com',
    url='http://seven-pairs.hatenablog.jp/',
    packages=find_packages(exclude=['tests']),
    install_requires=['tweepy'],
)
