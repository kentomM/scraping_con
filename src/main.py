import time
from modules import const, vendor_info, export_csv
from modules.crawler import Crawler

se = Crawler()

try:
    se.arrow_top_page()
    
    se.search()

    # 書き込み先CSVを用意
    middle_page = int(const.CONDITION_START_NO / const.CONDITION_DISPLAY_COUNT) + 1
    path = f'./tmp/vendors_{const.CONDITION_PREFECTURE}.csv'
    if middle_page == '1':
        export_csv.create_file(path, const.CSV_HEADER)

    page_values = se.get_page_values()
    offset_of_page = const.CONDITION_START_NO - (middle_page -1) * const.CONDITION_DISPLAY_COUNT
    for page_num in page_values[middle_page-1:][:const.NUM_PAGE_TO_PROCESS]:
        # リストのページを移動
        se.move_page(page_num)
        
        # 業者情報をCSVに追記
        for i in range(const.CONDITION_DISPLAY_COUNT - offset_of_page):
            print("-"*20)
            count_of_page = i + 1 + offset_of_page
            count_total = (int(page_num)-1) * const.CONDITION_DISPLAY_COUNT + count_of_page
            print(f"Processing to {page_num}/{page_values[-1]}:{count_of_page}件目, Count {count_total}")
            # 詳細ページを開く
            se.open_detail_page(offset_of_page+i+2)
            # 必要な情報を取得
            vendor = vendor_info.parse(se.get_html())
            # CSVに書き込み
            export_csv.write_row(path, vendor)
            # サーバー負荷を考え待機
            se.return_vendor_list()
            time.sleep(2)
        offset_of_page = 0
except Exception as e:
    print(e)
finally:        
    se.quit()
