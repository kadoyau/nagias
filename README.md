ナナコギフト入力で日曜日を溶かすのは、もうおしまいにしよう

- [Dockerを使った実行 (recommended)](#dockerを使った実行-recommended)
- [macOSでの実行](#macosでの実行)
- [Ubuntuでの実行](#ubuntuでの実行)
- [設定ファイルの作り方](#設定ファイルの作り方)
- [`.giftcodes`を作成しやすくする補助ツール](#giftcodesを作成しやすくする補助ツール)
- [よくある質問](#よくある質問)

# Dockerを使った実行 (recommended)
## 動作環境
- OS
  - macOS
  - Linux(Ubuntu, etc.)
  - Windows

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

### 2. 必要なファイルを用意
IDとpasswordの設定を記述・ギフトコードを入力（[設定ファイルの作り方](#設定ファイルの作り方)を参照）
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
           -v $PWD:/root/nagias \
           nagias python nanaco_auto_fill.py -d
```

カード会員
```
docker run --rm --name nagias \
           -v $PWD:/root/nagias \
           nagias python nanaco_auto_fill.py -t 2 -d
```

## 検証環境
- Ubuntu 22.04 LTS
  - Docker 20.10.17
  - git 2.34.1
- Docker Image python:3.10.5-slim-bullseye
  - Firefox 91.10.0esr
  - geckodriver 0.31.0
  - Selenium 4.2.0

# macOSでの実行
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

# Ubuntuでの実行
macOSとほぼ同じなので、詳細を省く。デフォルトで入っているFirefoxを使う。
## 事前準備
```
sudo apt update
sudo apt install python3-pip firefox-geckodriver

git clone https://github.com/kadoyau/nagias.git
cd nagias

pip install virtualenv

virtualenv env
source env/bin/activate

pip install selenium
```

IDとpasswordの設定を記述・ギフトコードを入力（[設定ファイルの作り方](#設定ファイルの作り方)を参照）
```
$EDITOR .secret
$EDITOR .giftcodes
```

## 実行方法
モバイル会員・ネット会員
```
python nanaco_auto_fill.py -u
```

カード会員

```
python nanaco_auto_fill.py -t 2 -u
```

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

# よくある質問
https://scrapbox.io/kadoyau/nagias_FAQ
