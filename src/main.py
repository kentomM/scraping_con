import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from modules import const, search_setting, vendor_info, export_csv, error

options = webdriver.ChromeOptions()
driver = webdriver.Remote(
    command_executor = 'http://selenium:4444/wd/hub',
    options = options
)


def move_page(target_page: int) -> None:
    # リストのページを移動
    driver.implicitly_wait(10)
    dropdown = driver.find_element(By.ID, 'pageListNo1')
    time.sleep(2)
    pager = Select(dropdown)
    pager.select_by_value(target_page)
    
    time.sleep(1)
    if error.is_confirm_page(driver.page_source):
        print("Please press enter after confirm page.")
        input()
        time.sleep(3)
    if error.is_error_page(driver.page_source):
        print("Error displayed. Retry after 10 seconds.")
        time.sleep(1)
        driver.back()
        time.sleep(10)
        move_page(target_page)
    
    return

def open_detail_page(target: int) -> None:
    driver.implicitly_wait(10)
    el = driver.find_element(By.XPATH, f'//*[@id="container_cont"]/table/tbody/tr[{target}]/td[4]/a')
    el.click()
    
    time.sleep(1)
    if error.is_confirm_page(driver.page_source):
        print("Please press enter after confirm page.")
        input()
        time.sleep(3)
    if error.is_error_page(driver.page_source):
        driver.back()
        time.sleep(20)
        open_detail_page(target)
    return

def return_vendor_list() -> None:
    pancuz = driver.find_element(By.XPATH, '//*[@id="pancuz"]/p[1]/a[2]')
    pancuz.click()
    
    time.sleep(3)
    if error.is_confirm_page(driver.page_source):
        print("Please press enter after confirm page.")
        input()
    if error.is_error_page(driver.page_source):
        driver.back()
        time.sleep(20)
        return_vendor_list()
    return 

try:
    driver.implicitly_wait(10)

    url = 'https://etsuran2.mlit.go.jp/TAKKEN/kensetuKensaku.do?outPutKbn=1'
    driver.get(url)
    
    time.sleep(1)
    if error.is_confirm_page(driver.page_source):
        print("Please press enter after confirm page.")
        input()
    # 検索条件を指定
    search_setting.set_condition(driver)

    # 「検索」ボタンを押す
    el = driver.find_element(By.XPATH, '//*[@id="input"]/div[6]/div[5]/img')
    el.click()
    
    time.sleep(1)
    if error.is_confirm_page(driver.page_source):
        print("Please press enter after confirm page.")
        input()


    # 書き込み先CSVを用意
    path = f'./tmp/vendors_{const.CONDITION_PREFECTURE}.csv'
    if const.CONDITION_MIDDLE_PAGE == '1':
        export_csv.create_file(path, const.CSV_HEADER)

    # 次のページがある限り繰り返し
    dropdown = driver.find_element(By.ID, 'pageListNo1')
    pager = Select(dropdown)
    middle_page = int(const.CONDITION_MIDDLE_PAGE) - 1
    page_values = [option.get_attribute("value") for option in pager.options][middle_page:]

    for value in page_values[:const.NUM_PAGE_TO_PROCESS]:
        # リストのページを移動
        move_page(value)
        
        # 業者情報をCSVに追記
        for i in range(const.CONDITION_DISPLAY_COUNT):
            print("-"*20)
            print(f"Processing to {value}/{page_values[-1]}:{i+1}件目, Count {(int(value)-1)*const.CONDITION_DISPLAY_COUNT+i+1}")
            # 詳細ページを開く
            open_detail_page(i+2)
            # 必要な情報を取得
            driver.implicitly_wait(10)
            html = driver.page_source
            vendor = vendor_info.parse(html)
            # CSVに書き込み
            export_csv.write_row(path, vendor)
            # サーバー負荷を考え待機
            time.sleep(2)
            return_vendor_list()
            time.sleep(2)
except Exception as e:
    print(e)
finally:        
    driver.quit()
