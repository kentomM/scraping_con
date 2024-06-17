from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

options = webdriver.ChromeOptions()
driver = webdriver.Remote(
    command_executor = 'http://selenium:4444/wd/hub',
    options = options
)

driver.implicitly_wait(10)

url = 'https://etsuran2.mlit.go.jp/TAKKEN/kensetuKensaku.do?outPutKbn=1' # テストでアクセスするURLを指定
driver.get(url)

# 検索条件: 本店
dropdown = driver.find_element(By.ID, 'choice')
select = Select(dropdown)
select.select_by_value('1')

# 検索条件: 都道府県
dropdown = driver.find_element(By.ID, 'kenCode')
select = Select(dropdown)
select.select_by_value('13')

# 「検索」ボタンを押す
el = driver.find_element(By.XPATH, '//*[@id="input"]/div[6]/div[5]/img')
el.click()

driver.save_screenshot('test.png') # アクセスした先でスクリーンショットを取得
driver.quit()
