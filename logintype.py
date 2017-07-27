from enum import Enum

class LoginType(Enum):
    '''ナナコのログイン種別
    
    CARD: カード記載の番号でログイン
    NET: 会員メニュー用パスワードでログイン
    '''
    NET = 1
    CARD = 2
