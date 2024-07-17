import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from . import error, const

class Crawler():
    def __init__(self):
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Remote(
            command_executor = 'http://selenium:4444/wd/hub',
            options = options
        )

    def arrow_top_page(self) -> None:
        """
        TOPページを表示
        """
        self.driver.implicitly_wait(10)
        # 検索ページを表示
        url = 'https://etsuran2.mlit.go.jp/TAKKEN/kensetuKensaku.do?outPutKbn=1'
        self.driver.get(url)

        if error.has_error(self.driver.page_source):
            self.allow_top_page()
        return

    def search(self) -> None:
        """
        検索条件をセットして検索ボタンを押す
        """
        self.driver.implicitly_wait(10)
        # 検索条件: 本店
        dropdown = self.driver.find_element(By.ID, 'choice')
        select = Select(dropdown)
        select.select_by_value('1')

        # 検索条件: 都道府県
        dropdown = self.driver.find_element(By.ID, 'kenCode')
        select = Select(dropdown)
        select.select_by_value(const.CONDITION_PREFECTURE)

        # 検索条件: 結果表示件数
        dropdown = self.driver.find_element(By.ID, 'dispCount')
        select = Select(dropdown)
        select.select_by_value(str(const.CONDITION_DISPLAY_COUNT))
        
        # 「検索」ボタンを押す
        el = self.driver.find_element(By.XPATH, '//*[@id="input"]/div[6]/div[5]/img')
        el.click()
        
        if error.has_error(self.driver.page_source):
            self.deriver.back()
            self.search()
        return
    
    def get_page_values(self) -> list:
        """
        プルダウンの件数を取得して返す
        """
        dropdown = self.driver.find_element(By.ID, 'pageListNo1')
        pager = Select(dropdown)
        page_values = [option.get_attribute("value") for option in pager.options]
        return page_values
        
    def move_page(self, target_page: int) -> None:
        """
        ページを切り替える
        """
        self.driver.implicitly_wait(10)
        dropdown = self.driver.find_element(By.ID, 'pageListNo1')
        pager = Select(dropdown)
        pager.select_by_value(target_page)
        
        if error.has_error(self.driver.page_source):
            self.driver.back()
            self.move_page(target_page)        
        return

    def open_detail_page(self, target: int) -> None:
        self.driver.implicitly_wait(10)
        el = self.driver.find_element(By.XPATH, f'//*[@id="container_cont"]/table/tbody/tr[{target}]/td[4]/a')
        el.click()
        
        time.sleep(2)
        if error.has_error(self.driver.page_source):
            self.driver.back()
            self.open_detail_page(target)
        return

    def get_html(self) -> str:
        self.driver.implicitly_wait(10)
        return self.driver.page_source

    def return_vendor_list(self) -> None:
        time.sleep(2)
        pancuz = self.driver.find_element(By.XPATH, '//*[@id="pancuz"]/p[1]/a[2]')
        pancuz.click()
        
        time.sleep(3)
        if error.has_error(self.driver.page_source):
            self.driver.back()
            self.return_vendor_list()
        return 
    
    def quit(self):
        self.driver.quit()
        return
