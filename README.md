ナナコギフト入力で日曜日の午前が溶かすのは、もうおしまいにしよう

# 使い方(macOS）
## 事前準備
- [Chrome Canary](https://www.google.co.jp/chrome/browser/canary.html)をインストールする
- 以下の手順に従ってselenium等を導入
```
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

# 実行確認
chromedriver
Starting ChromeDriver 2.30.477690 (c53f4ad87510ee97b5c3425a14c0e79780cdf262) on port 9515
Only local connections are allowed.
# Ctrl-Cなどで一旦切断する
```

## 実行
```
git clone git@github.com:kadoyau/nagias.git
cd nagias
# IDとpasswordの設定を記述
vim .secret
# 16桁のギフトコードを入力する
vim .giftcodes 
# 実行
python nanaco_auto_fill.py
```

## .secretの中身
タブ区切りでID/Passをかきます
```
YOUR_LOGIN_ID  YOUR_PASSWORD
```

## .giftcodesの中身
```
abcdefghijklmnop
bcdefghijklmnopq
...
```
