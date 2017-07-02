from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

# Chrome起動時のオプションの設定
options = webdriver.ChromeOptions()
#options.binary_location ='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
# 自分の環境だとCanaryでないと動かなかった
options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
options.add_argument('headless')
options.add_argument('window-size=1200x600')
driver = webdriver.Chrome(chrome_options=options)

# nanacoのログインページへアクセス
driver.get('https://www.nanaco-net.jp/pc/emServlet')

# 次の行動にうつるまでの秒数を指定する
driver.implicitly_wait(5)

# nanacoのサイトにログインする
email = driver.find_element_by_css_selector('#loginByPassword input[type=text]')
password = driver.find_element_by_css_selector('#loginByPassword input[type=password]')
with open('.secret') as f:
    credentials = f.read().strip().split('\t')

email.send_keys(credentials[0])
password.send_keys(credentials[1])
# @see http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.common.keys
password.send_keys(Keys.RETURN)

# ギフト登録約款ページに飛ぶ
driver.get_screenshot_as_file('yakkan.png')
driver.find_element_by_css_selector('#memberNavi02').click()

