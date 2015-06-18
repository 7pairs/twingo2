# twingo2

[![Build Status](https://travis-ci.org/7pairs/twingo2.svg?branch=master)](https://travis-ci.org/7pairs/twingo2)
[![Coverage Status](https://coveralls.io/repos/7pairs/twingo2/badge.svg?branch=master)](https://coveralls.io/r/7pairs/twingo2?branch=master)

## 概要

"twingo2"は、TwitterのOAuthを利用したDjangoの認証バックエンドです。
Twitterのユーザー情報による認証の仕組みを簡単な記述でDjangoアプリケーションに組み込むことができます。

## バージョン

Python3.4 + Django1.8での動作を確認しています。
また、Python3.3およびDjango1.7でもユニットテストを実施しています。

## インストール

同梱の `setup.py` を実行してください。

```console
$ python setup.py install
```

pipを利用し、GitHubから直接インストールすることもできます。

```console
$ pip install git+https://github.com/7pairs/twingo2.git
```

## 設定

Djangoからtwingo2を呼び出すための設定を行います。
まず、 `settings.py` の `INSTALLED_APPS` に `twingo2` を追加してください。

```python
INSTALLED_APPS = (
    # (中略)
    'twingo2',  # ←追加
)
```

さらに、twingo2を認証バックエンドとするための設定を行います。
同じく `settings.py` に以下の記述を追加してください。

```python
AUTHENTICATION_BACKENDS = (
    'twingo2.backends.TwitterBackend',
)
```

加えて、twingo2のモデルをシステムのユーザーモデルとするための設定を行います。
同じく `settings.py` に以下の記述を追加してください。

```python
AUTH_USER_MODEL = 'twingo2.User'
```

また、あわせて `settings.py` に以下の定数を定義してください。

|定数名           |設定する値                  |
|-----------------|----------------------------|
|`CONSUMER_KEY`   |Twitter APIのConsumer Key   |
|`CONSUMER_SECRET`|Twitter APIのConsumer Secret|

なお、以下の定数を定義することで、twingo2のデフォルトの動作を上書きすることができます（任意）。

|定数名            |設定する値                                                                     |デフォルト値|
|------------------|-------------------------------------------------------------------------------|------------|
|`ADMIN_TWITTER_ID`|管理者のTwitter ID（Screen Nameではありません）を格納したタプル（複数指定可能）|`None`      |
|`AFTER_LOGIN_URL` |ログイン成功後のリダイレクト先URL                                              |`/`         |
|`AFTER_LOGOUT_URL`|ログアウト後のリダイレクト先URL                                                |`/`         |

## URLディスパッチャー

`urls.py` に以下の記述を追加してください。

```python
urlpatterns = patterns('',
    # (中略)
    (r'^authentication_url/', include('twingo2.urls'))  # ←追加
)
```

`r'^authentication_url/'` は任意のURLで構いません。
その配下のURLでtwingo2が動作します。

また、 `@login_required` デコレータを使用する場合、 `settings.py` に以下の記述を追加してください。

```python
LOGIN_URL = 'authentication_url/login/'
```

`authentication_url` の部分は `urls.py` にて設定した値と同一のものにしてください。

## ライセンス

twingo2は [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0) にて提供します。
ただし、twingo2が依存している [Tweepy](https://github.com/tweepy/tweepy) は [The MIT License](http://opensource.org/licenses/mit-license.php) により提供されていますのでご注意ください。
