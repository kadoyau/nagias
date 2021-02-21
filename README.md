ナナコギフト入力で日曜日を溶かすのは、もうおしまいにしよう

# 使い方(macOS）
## 事前準備
- [Chrome](https://www.google.co.jp/chrome/browser/desktop/index.html)および[Chrome Canary](https://www.google.co.jp/chrome/browser/canary.html)をインストールする
  - `/Applications` 直下におく
  - 使いたい方だけ入れれば問題ない（デフォルトはChromeを利用する）
- 以下の手順に従ってselenium等を導入
```zsh
git clone git@github.com:kadoyau/nagias.git
cd nagias

# virtualenvのインストール
pip install virtualenv
# virtualenvをアクティベート（ここで/env/binが生成される）
virtualenv env
source env/bin/activate

# Seleniumのインストール
pip install selenium

# Chrome Driverのインストール
PLATFORM=mac64
VERSION=$(curl http://chromedriver.storage.googleapis.com/LATEST_RELEASE)
curl http://chromedriver.storage.googleapis.com/$VERSION/chromedriver_$PLATFORM.zip \
| bsdtar -xvf - -C env/bin/
chmod u+x env/bin/chromedriver

# 実行確認
chromedriver
Starting ChromeDriver 2.30.477690 (c53f4ad87510ee97b5c3425a14c0e79780cdf262) on port 9515
Only local connections are allowed.
# Ctrl-Cなどで一旦切断する

# IDとpasswordの設定を記述
$EDITOR .secret
# ギフトコードを入力する
$EDITOR .giftcodes 
```
## 使い方

### 実行方法
モバイル会員・ネット会員
```
python nanaco_auto_fill.py
```

カード会員

```
python nanaco_auto_fill.py -t 2
```
### 詳細な使い方
以下のコマンドでヘルプを表示できます。
```
python nanaco_auto_fill.py -h
```
#### 注意
`-q`オプションを使う際には、`-c`と組み合わせて利用しないとエラーが発生します。

再現環境
 - headless chrome=60.0.3112.78
 - chromedriver=2.30.477690
 - Mac OS X 10.12.5

Chrome 62.0.3168.0では問題ありませんでした。

# Docker
## 動作環境
- OS
  - macOS
  - Linux(Ubuntu, etc.)

- Programs
  - [Docker](https://www.docker.com/)
  
    [Installation guide in English](https://docs.docker.com/get-docker/)
    
    [インストール方法（日本語版）](https://docs.docker.jp/get-docker.html)
  
  - [Git](https://git-scm.com/) (任意)
  
    このリポジトリ取得用

## 使い方
### 1. このリポジトリをダウンロード
```
git clone https://github.com/kadoyau/nagias.git
cd nagias
```

### 2. IDとpasswordの設定を記述・ギフトコードを入力（[設定ファイルの作り方](#設定ファイルの作り方)を参照）
```
$EDITOR .secret
$EDITOR .giftcodes
```

### 3. Dockerイメージを構築
```
docker build -t nagias .
```

### 4. コンテナとしてイメージを実行
モバイル会員・ネット会員
```
docker run --rm --name nagias \
           -v $PWD/.secret:/home/nagias/.secret \
           -v $PWD/.giftcodes:/home/nagias/.giftcodes \
           --security-opt seccomp=$PWD/chrome.json \
           nagias python nanaco_auto_fill.py -d
```

カード会員
```
docker run --rm --name nagias \
           -v $PWD/.secret:/home/nagias/.secret \
           -v $PWD/.giftcodes:/home/nagias/.giftcodes \
           --security-opt seccomp=$PWD/chrome.json \
           nagias python nanaco_auto_fill.py -t 2 -d
```

## Dockerのセキュリティ
- [Seccomp security profilesのDocker公式解説](https://docs.docker.com/engine/security/seccomp/)
- [Chrome Headlessを安全に使うために](https://github.com/Zenika/alpine-chrome#-the-best-with-seccomp)

Docker用のSeccomp Profileは[jessfraz](https://github.com/jessfraz)の[chrome.json](https://github.com/jessfraz/dotfiles/blob/master/etc/docker/seccomp/chrome.json)を使っています。

## 検証環境
- Ubuntu 20.04.2 LTS
  - Docker 20.10.3
  - git 2.25.1
- Docker Image: python:3.9.2-alpine3.13
  - Chromium 86.0.4240.111
  - ChromeDriver 86.0.4240.111
  - Selenium 3.141.0

# 設定ファイルの作り方
### .secretの中身
**タブ区切り**でID/Passをかきます
```
YOUR_LOGIN_ID  YOUR_PASSWORD
```

### .giftcodesの中身
16桁のギフトコードを入力する。1つのコードごとに改行する。
```
abcdefghijklmnop
bcdefghijklmnopq
...
```

# `.giftcodes`を作成しやすくする補助ツール
![image](https://i.gyazo.com/a77e64e6781ef77aabc673cfc37e7997.png)

## 使い方
1. [Tampermonkey](http://tampermonkey.net/)をインストールする
2. https://github.com/kadoyau/nagias/raw/master/code_extractor.user.js をひらいてユーザスクリプトをインストールする
3. ギフトコードが送られてくるページへアクセスするとコピペ用のテキストエリアにコードが出現
4. `.giftcodes`にペーストする

## よくある質問
https://scrapbox.io/kadoyau/nagias_FAQ
