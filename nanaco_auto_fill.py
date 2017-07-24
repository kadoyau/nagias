"""
nanacoギフトカードの登録をするプログラム
"""
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


def main():
    # TODO: usageを書く
    # Chrome起動時のオプションの設定
    options = webdriver.ChromeOptions()
    #options.binary_location ='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    # 自分の環境だとCanaryでないと動かなかった
    options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
    # options.add_argument('headless')
    options.add_argument('window-size=1200x600')
    DRIVER = webdriver.Chrome(chrome_options=options)

    # nanacoのログインページへアクセス
    DRIVER.get('https://www.nanaco-net.jp/pc/emServlet')

    # タイムアウトまでのデフォルト秒数を指定する
    DRIVER.implicitly_wait(3)

    # nanacoのサイトにログインする
    EMAIL = DRIVER.find_element_by_css_selector('#loginByPassword input[type=text]')
    PASSWORD = DRIVER.find_element_by_css_selector('#loginByPassword input[type=password]')
    with open('.secret') as f:
        CREDENTIALS = f.read().strip().split('\t')

    EMAIL.send_keys(CREDENTIALS[0])
    PASSWORD.send_keys(CREDENTIALS[1])
    # @see http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.common.keys
    PASSWORD.send_keys(Keys.RETURN)

    # ギフト登録約款ページに飛ぶ
    DRIVER.find_element_by_css_selector('#memberNavi02').click()


    # コードの数だけ入力を繰り返す
    # コードを全て取得する
    with open('.giftcodes') as f:
        CODES = f.read().splitlines()

    results = {'success':[], 'fairule':[]}
    for code in CODES:
        # ギフト登録ページにジャンプする
        DRIVER.find_element_by_css_selector('#register input[type=image]').click()

        # ギフト登録ページのウィンドウに制御を移す
        # @see http://qiita.com/QUANON/items/285ad7157619b0da5c67
        main_page =  DRIVER.window_handles[0]

        # 別ウィンドウのハンドラを取得する
        WebDriverWait(DRIVER, 3).until(lambda d: len(d.window_handles) > 1)
        gift_page_handle =  DRIVER.window_handles[1]
        DRIVER.switch_to.window(gift_page_handle)

        SPLIT_LENGTH = 4
        splited_code = [code[i: i + SPLIT_LENGTH] for i in range(0, len(code), SPLIT_LENGTH)]
        # コードを入力する
        DRIVER.find_element_by_id('gift01').send_keys(splited_code[0])
        DRIVER.find_element_by_id('gift02').send_keys(splited_code[1])
        DRIVER.find_element_by_id('gift03').send_keys(splited_code[2])
        DRIVER.find_element_by_id('gift04').send_keys(splited_code[3])

        DRIVER.find_element_by_id('submit-button').click()

        # 登録するボタンを押す
        try:
            DRIVER.find_element_by_css_selector('#nav2Next input[type=image]').click()
            results["success"].append(code)
        except NoSuchElementException:
            results["fairule"].append(code)

        # 当該ウィンドウを終了する
        # @see https://stackoverflow.com/questions/35286094/how-to-close-the-whole-browser-window-by-keeping-the-webdriver-active
        DRIVER.close()

        # はじめのウィンドウに戻る
        DRIVER.switch_to.window(main_page)

    DRIVER.quit()
    return results


def show_results(results):
    """結果を表示する"""
    print('SUCCESS: ' + str(len(results["success"])))
    print('FAIRULE: ' + str(len(results["fairule"])))
    pprint(results["fairule"])

if __name__ == '__main__':
    RESULTS = main()
    show_results(RESULTS)
