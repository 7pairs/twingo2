# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('twitter_id', models.IntegerField(unique=True, verbose_name='Twitter ID')),
                ('screen_name', models.CharField(max_length=15, verbose_name='ユーザー名')),
                ('name', models.CharField(max_length=20, verbose_name='名前')),
                ('description', models.CharField(blank=True, max_length=160, verbose_name='自己紹介')),
                ('location', models.CharField(blank=True, max_length=30, verbose_name='場所')),
                ('url', models.URLField(blank=True, verbose_name='ホームページ')),
                ('profile_image_url', models.URLField(blank=True, verbose_name='プロフィール画像')),
                ('is_active', models.BooleanField(verbose_name='有効フラグ', default=False)),
                ('is_superuser', models.BooleanField(verbose_name='管理者権限', default=False)),
                ('is_staff', models.BooleanField(verbose_name='管理画面操作権限', default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='登録日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
