"""
複数行のnanacoギフトカードの登録を自動化する
"""
import os
import argparse
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from logintype import LoginType
import time

class NanacoAutoFiller:
    __results = {'success':[], 'failure':[]}

    def __init__(self, login_type, use_canary, is_quiet, is_docker, is_ubuntu):
        self.__use_canary = use_canary
        self.__login_type = login_type
        self.__is_quiet = is_quiet
        self.__is_docker = is_docker
        self.__is_ubuntu = is_ubuntu

        self.__driver = self.__init_driver()
        # ログインに必要な情報を読み込む
        with open('.secret') as f:
            self.__CREDENTIALS = f.read().strip().split('\t')
        # コードを全て取得する
        with open('.giftcodes') as f:
            self.__codes = f.read().splitlines()

    def __init_driver(self):
        '''Chrome起動時のオプションの設定をしてドライバを返す'''
        if self.__is_docker:
            options = webdriver.firefox.options.Options()
            options.headless = True
            return webdriver.Firefox(options=options)
        if self.__is_ubuntu:
            options = webdriver.firefox.options.Options()
            return webdriver.Firefox(options=options)
        options = webdriver.ChromeOptions()
        if self.__use_canary:
            options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
        else:
            options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        if self.__is_quiet:
            options.add_argument('headless')
        options.add_argument('window-size=1200x600')
        return webdriver.Chrome(options=options)

    def __input_codes(self,code):
        '''ギフトコードを入力する'''
        SPLIT_LENGTH = 4
        SPLITED_CODES = [code[i: i + SPLIT_LENGTH] for i in range(0, len(code), SPLIT_LENGTH)]
        # コードを入力する
        for i in range(SPLIT_LENGTH):
            ID = 'gift0' + str(i+1) # gift01 to gift04
            WebDriverWait(self.__driver, 3).until(EC.presence_of_element_located((By.ID, ID))).send_keys(SPLITED_CODES[i])

    def __login(self):
        '''nanacoのサイトにログインする'''
        if self.__login_type is LoginType.NET:
            EMAIL = WebDriverWait(self.__driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#loginByPassword input[type=text]')))
            PASSWORD = WebDriverWait(self.__driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#loginByPassword input[type=password]')))
        elif self.__login_type is LoginType.CARD:
            EMAIL = WebDriverWait(self.__driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#loginByCard input[name=XCID]')))
            PASSWORD = WebDriverWait(self.__driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#loginByCard input[name=SECURITY_CD]')))

        EMAIL.send_keys(self.__CREDENTIALS[0])
        PASSWORD.send_keys(self.__CREDENTIALS[1])
        # @see http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.common.keys

        # TODO: このページ遷移を切り出す
        PASSWORD.send_keys(Keys.RETURN)

    def __register(self):
        '''登録するボタンを押す'''
        try:
            WebDriverWait(self.__driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#nav2Next input[type=image]'))).click()
            return True
        except TimeoutException:
            return False

    def __go_to_login_page(self):
        '''
        nanacoのログインページへアクセス
        https://gyazo.com/7f85b3bc21371319533afe7a30f52da2
        '''
        self.__driver.get('https://www.nanaco-net.jp/pc/emServlet')

    def __go_to_agreement_page(self):
        '''ギフト登録約款ページへアクセス'''
        WebDriverWait(self.__driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#memberNavi02'))).click()

    def __go_to_register_page(self):
        '''ギフトコード入力ページへアクセス'''
        WebDriverWait(self.__driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#register input[type=image]'))).click()

    def __get_register_page_handle(self):
        '''ギフトコード入力ページ（別ウィンドウ）のハンドラを取得する'''
        WebDriverWait(self.__driver, 3).until(lambda d: len(d.window_handles) > 1)
        gift_page_handle = self.__driver.window_handles[1]
        return gift_page_handle

    def __go_to_register_confirm_page(self):
        '''ギフトID内容登録確認ページへアクセス
        http://qiita.com/QUANON/items/285ad7157619b0da5c67
        '''
        WebDriverWait(self.__driver, 3).until(EC.element_to_be_clickable((By.ID, 'submit-button'))).click()

    def main(self):
        self.__go_to_login_page()
        self.__login()
        self.__go_to_agreement_page()

        for code in self.__codes:
            self.__go_to_register_page()

            # ギフト登録ページのウィンドウに制御を移す
            main_page =  self.__driver.window_handles[0]

            register_page_handle = self.__get_register_page_handle()
            self.__driver.switch_to.window(register_page_handle)

            self.__input_codes(code)
            self.__go_to_register_confirm_page()

            if self.__register():
                self.__results["success"].append(code)
            else:
                self.__results["failure"].append(code)
            # 当該ウィンドウを終了する
            # @see https://stackoverflow.com/questions/35286094/how-to-close-the-whole-browser-window-by-keeping-the-webdriver-active
            self.__driver.close()

            # はじめのウィンドウに戻る
            self.__driver.switch_to.window(main_page)
            time.sleep(1)
        self.__driver.quit()

        # Delete geckodriver's log when using Firefox
        if self.__is_docker or self.__is_ubuntu:
            os.remove('geckodriver.log')

    def output(self):
        """結果を表示する"""
        print('SUCCESS: ' + str(len(self.__results["success"])))
        print('FAILURE: ' + str(len(self.__results["failure"])))
        pprint(self.__results["failure"])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t", "--login_type",
        help="1：会員メニュー用パスワードでログイン, 2：カード記載の番号でログイン",
        type=int,
        choices=[1, 2],
        default=1
    )
    parser.add_argument(
        "-c", "--use_canary",
        help="ブラウザとしてChrome Canaryを使う（デフォルトはChrome）",
        action="store_true"
    )
    parser.add_argument(
        "-q", "--quiet",
       help="Chromeのheadless modeを利用する",
       action="store_true"
    )
    parser.add_argument(
        "-d", "--docker",
       help="Option used for dockerized nagias",
       action="store_true"
    )
    parser.add_argument(
        "-u", "--ubuntu",
       help="Run nagias on a Ubuntu machine with Firefox",
       action="store_true"
    )
    args = parser.parse_args()

    nanaco = NanacoAutoFiller(LoginType(args.login_type), args.use_canary, args.quiet, args.docker, args.ubuntu)
    nanaco.main()
    nanaco.output()
