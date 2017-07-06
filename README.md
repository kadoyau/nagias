ナナコギフト入力で日曜日を溶かすのは、もうおしまいにしよう

# 使い方(macOS）
## 事前準備
- [Chrome Canary](https://www.google.co.jp/chrome/browser/canary.html)をインストールする  
  - `/Applications` 直下におく
- 以下の手順に従ってselenium等を導入
```
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

# 実行確認
chromedriver
Starting ChromeDriver 2.30.477690 (c53f4ad87510ee97b5c3425a14c0e79780cdf262) on port 9515
Only local connections are allowed.
# Ctrl-Cなどで一旦切断する

# IDとpasswordの設定を記述
vim .secret
# ギフトコードを入力する
vim .giftcodes 
```
## 実行
```
python nanaco_auto_fill.py
```

## 設定ファイルの作り方
### .secretの中身
タブ区切りでID/Passをかきます
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
