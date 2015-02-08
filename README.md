# twingo2

## 概要

"twingo2" は、TwitterのOAuthを利用したDjangoの認証バックエンドです。
Twitterのユーザー情報を利用したログインの仕組みを、簡単な記述でアプリケーションに組み込むことができます。

## バージョン

Python3.4 + Django1.7での動作を確認しております。

## インストール

同梱の `setup.py` を実行してください。

```
python setup.py install
```

pipを利用して、GitHubから直接インストールすることもできます。

```
pip install git+https://github.com/7pairs/twingo2.git
```

## 設定

twingo2をDjangoから呼び出すための設定を行います。
`settings.py` の `INSTALLED_APPS` に `twingo2` の記述を追加してください。

```python
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'yourproject.yourapplication',
    'twingo2',  # ←追加
)
```

続いて、twingo2を認証バックエンドとするための設定を行います。
同じく `settings.py` に以下の記述を追加してください。

```python
AUTHENTICATION_BACKENDS = (
    'twingo2.backends.TwitterBackend',
)
```

さらに、twingo2のユーザーモデルをDjangoのモデルから置き換えるための設定を行います。
同じく `settings.py` に以下の記述を追加してください。

```python
AUTH_USER_MODEL = 'twingo2.User'
```

また、あわせて `settings.py` に以下の定数を定義してください。

* `CONSUMER_KEY` : Twitter APIのConsumer Key。
* `CONSUMER_SECRET` : Twitter APIのConsumer Secret。

なお、以下の定数を定義することで、twingo2のデフォルトの動作を変更することができます（任意）。

* `ADMIN_TWITTER_ID` : 管理者のTwitter ID（Screen Nameではありません）を格納したタプル。複数人指定可能。
* `AFTER_LOGIN_URL` : ログイン成功後のリダイレクト先URL。デフォルトは `/` 。
* `AFTER_LOGOUT_URL` : ログアウト後のリダイレクト先URL。デフォルトは `/` 。

## URLディスパッチャー

最後に、`urls.py` に以下の設定を追加してください。

```python
urlpatterns = patterns('',
    # 中略
    (r'^authentication_url/', include('twingo2.urls'))  # ←追加
)
```

`r'^authentication_url/'` は任意のURLで構いません。その配下のURLでtwingo2が動作します。
