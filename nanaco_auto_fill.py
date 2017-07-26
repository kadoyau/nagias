"""
nanacoギフトカードの登録をするプログラム
"""
import sys
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

class NanacoAutoFiller:
    __results = {'success':[], 'fairule':[]}

    def __init__(self, use_canary = False):
        self.__use_canary = use_canary
        self.__driver = self.__init_driver()
        # タイムアウトまでのデフォルト秒数を指定する
        self.__driver.implicitly_wait(3)
        # ログインに必要な情報を読み込む
        with open('.secret') as f:
            self.__CREDENTIALS = f.read().strip().split('\t')
    
    def __init_driver(self):
        '''Chrome起動時のオプションの設定をしてドライバを返す'''
        options = webdriver.ChromeOptions()
        if self.__use_canary:
            options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
        else:
            options.binary_location ='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        # options.add_argument('headless')
        options.add_argument('window-size=1200x600')
        return webdriver.Chrome(chrome_options=options)

    def __input_codes(self,code):
        '''ギフトコードを入力する'''
        SPLIT_LENGTH = 4
        SPLITED_CODES = [code[i: i + SPLIT_LENGTH] for i in range(0, len(code), SPLIT_LENGTH)]
        # コードを入力する
        for i in range(SPLIT_LENGTH):
            ID = 'gift0' + str(i+1) # gift01 to gift04
            self.__driver.find_element_by_id(ID).send_keys(SPLITED_CODES[i])
    
    def __login(self):
        '''nanacoのサイトにログインする'''
        EMAIL = self.__driver.find_element_by_css_selector('#loginByPassword input[type=text]')
        PASSWORD = self.__driver.find_element_by_css_selector('#loginByPassword input[type=password]')

        EMAIL.send_keys(self.__CREDENTIALS[0])
        PASSWORD.send_keys(self.__CREDENTIALS[1])
        # @see http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.common.keys

        # TODO: このページ遷移を切り出す
        PASSWORD.send_keys(Keys.RETURN)
    
    def __register(self):
        '''登録するボタンを押す'''
        try:
            self.__driver.find_element_by_css_selector('#nav2Next input[type=image]').click()
            return True
        except NoSuchElementException:
            return False

    def __go_to_login_page(self):
        '''
        nanacoのログインページへアクセス
        https://gyazo.com/7f85b3bc21371319533afe7a30f52da2
        '''
        self.__driver.get('https://www.nanaco-net.jp/pc/emServlet')

    def __go_to_agreement_page(self):
        '''ギフト登録約款ページへアクセス'''
        self.__driver.find_element_by_css_selector('#memberNavi02').click()


    def main(self):
        # TODO: usageを書く
        self.__go_to_login_page()
        self.__login()
        self.__go_to_agreement_page()

        # コードの数だけ入力を繰り返す
        # コードを全て取得する
        with open('.giftcodes') as f:
            CODES = f.read().splitlines()

        for code in CODES:
            # ギフト登録ページにジャンプする
            self.__driver.find_element_by_css_selector('#register input[type=image]').click()
            # ギフト登録ページのウィンドウに制御を移す
            # @see http://qiita.com/QUANON/items/285ad7157619b0da5c67
            main_page =  self.__driver.window_handles[0]

            # 別ウィンドウのハンドラを取得する
            WebDriverWait(self.__driver, 3).until(lambda d: len(d.window_handles) > 1)
            gift_page_handle =  self.__driver.window_handles[1]
            self.__driver.switch_to.window(gift_page_handle)

            self.__input_codes(code)
            self.__driver.find_element_by_id('submit-button').click()

            if self.__register():
                self.__results["success"].append(code)
            else:
                self.__results["fairule"].append(code)
            # 当該ウィンドウを終了する
            # @see https://stackoverflow.com/questions/35286094/how-to-close-the-whole-browser-window-by-keeping-the-webdriver-active
            self.__driver.close()

            # はじめのウィンドウに戻る
            self.__driver.switch_to.window(main_page)
        self.__driver.quit()

    def output(self):
        """結果を表示する"""
        print('SUCCESS: ' + str(len(self.__results["success"])))
        print('FAIRULE: ' + str(len(self.__results["fairule"])))
        pprint(self.__results["fairule"])

if __name__ == '__main__':
    arg_names = ['command', 'use_canary']
    args = dict(zip(arg_names, sys.argv))
    use_canary = args.get('use_canary', False)

    nanaco = NanacoAutoFiller(use_canary)
    nanaco.main()
    nanaco.output()
