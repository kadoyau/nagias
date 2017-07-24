"""
nanacoギフトカードの登録をするプログラム
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

# TODO: usageを書く

# Chrome起動時のオプションの設定
options = webdriver.ChromeOptions()
#options.binary_location ='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
# 自分の環境だとCanaryでないと動かなかった
options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
# options.add_argument('headless')
options.add_argument('window-size=1200x600')
driver = webdriver.Chrome(chrome_options=options)

# nanacoのログインページへアクセス
driver.get('https://www.nanaco-net.jp/pc/emServlet')

# タイムアウトまでのデフォルト秒数を指定する
driver.implicitly_wait(3)

# nanacoのサイトにログインする
EMAIL = driver.find_element_by_css_selector('#loginByPassword input[type=text]')
PASSWORD = driver.find_element_by_css_selector('#loginByPassword input[type=password]')
with open('.secret') as f:
    credentials = f.read().strip().split('\t')

EMAIL.send_keys(credentials[0])
PASSWORD.send_keys(credentials[1])
# @see http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.common.keys
PASSWORD.send_keys(Keys.RETURN)

# ギフト登録約款ページに飛ぶ
driver.find_element_by_css_selector('#memberNavi02').click()


# コードの数だけ入力を繰り返す
# コードを全て取得する
with open('.giftcodes') as f:
    codes = f.read().splitlines()

for code in codes:
    # ギフト登録ページにジャンプする
    driver.find_element_by_css_selector('#register input[type=image]').click()

    # ギフト登録ページのウィンドウに制御を移す
    # @see http://qiita.com/QUANON/items/285ad7157619b0da5c67
    main_page =  driver.window_handles[0]

    # 別ウィンドウのハンドラを取得する
    WebDriverWait(driver, 3).until(lambda d: len(d.window_handles) > 1)
    gift_page_handle =  driver.window_handles[1]
    driver.switch_to.window(gift_page_handle)

    SPLIT_LENGTH = 4
    splited_code = [code[i: i + SPLIT_LENGTH] for i in range(0, len(code), SPLIT_LENGTH)]
    # コードを入力する
    driver.find_element_by_id('gift01').send_keys(splited_code[0])
    driver.find_element_by_id('gift02').send_keys(splited_code[1])
    driver.find_element_by_id('gift03').send_keys(splited_code[2])
    driver.find_element_by_id('gift04').send_keys(splited_code[3])

    driver.find_element_by_id('submit-button').click()

    # 登録するボタンを押す
    driver.find_element_by_css_selector('#nav2Next input[type=image]').click()

    # 当該ウィンドウを終了する
    # @see https://stackoverflow.com/questions/35286094/how-to-close-the-whole-browser-window-by-keeping-the-webdriver-active
    driver.close()

    # はじめのウィンドウに戻る
    driver.switch_to.window(main_page)
    driver.get_screenshot_as_file('main-page.png')

driver.quit()
