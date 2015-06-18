#!/bin/bash

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

# インストール対象のライブラリ
INSTALL_LIBRARIES=('Django' 'tweepy' 'nose' 'django-nose' 'factory-boy' 'mock')

# requirements.txtに記載しないライブラリ
EXCLUDE_LIBRARIES=('Django')

# インストール済みのライブラリをいったんアンインストールする
echo '*****  Uninstall START ' `date +'%Y-%m-%d %H:%M:%S'` ' *****'
pip freeze | awk -F '==' '{print $1}' | while read library; do
    pip uninstall -y ${library}
done
echo '*****  Uninstall END   ' `date +'%Y-%m-%d %H:%M:%S'` ' *****'

# 対象のライブラリをインストールする
echo '*****  Install   START ' `date +'%Y-%m-%d %H:%M:%S'` ' *****'
for library in ${INSTALL_LIBRARIES[@]}; do
    pip install $library
done
echo '*****  Install   END   ' `date +'%Y-%m-%d %H:%M:%S'` ' *****'

# requirements.txtを更新する
echo '*****  Update    START ' `date +'%Y-%m-%d %H:%M:%S'` ' *****'
: > ./requirements.txt
pip freeze | while read line; do
    for exclude in ${EXCLUDE_LIBRARIES[@]}; do
        if [[ ${line} =~ "${exclude}==" ]]; then
            continue 2
        fi
    done
    echo ${line} >> ./requirements.txt
done
echo '*****  Update    END   ' `date +'%Y-%m-%d %H:%M:%S'` ' *****'
