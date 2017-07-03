ナナコギフト入力で日曜日の午前が溶かすのは、もうおしまいにしよう

# 使い方(TBD）
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
