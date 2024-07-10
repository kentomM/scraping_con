from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from modules import const

def set_condition(driver):
    driver.implicitly_wait(10)
    # 検索条件: 本店
    dropdown = driver.find_element(By.ID, 'choice')
    select = Select(dropdown)
    select.select_by_value('1')

    # 検索条件: 都道府県
    dropdown = driver.find_element(By.ID, 'kenCode')
    select = Select(dropdown)
    select.select_by_value(const.CONDITION_PREFECTURE)

    # 検索条件: 結果表示件数
    dropdown = driver.find_element(By.ID, 'dispCount')
    select = Select(dropdown)
    select.select_by_value(str(const.CONDITION_DISPLAY_COUNT))
    
    return driver
