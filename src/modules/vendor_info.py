import re
from bs4 import BeautifulSoup

def parse(html):
    soup = BeautifulSoup(html, features='html.parser')
    vendor = {}
    
    # 許可番号
    elements = soup.select('th:-soup-contains("許可番号") ~ td')
    vendor["license_number"] = elements[0].get_text().strip() if elements else ""

    # 許可の有効期間
    elements = soup.select('th:-soup-contains("許可の有効期間") ~ td')
    vendor["license_validity_period"] = elements[0].get_text().strip() if elements else ""

    # 法人・個人区分
    elements = soup.select('th:-soup-contains("法人・個人区分") ~ td')
    vendor["corporate_individual_classification"] = elements[0].get_text().strip() if elements else ""

    # 商号又は名称
    elements = soup.select('th:-soup-contains("商号又は名称") ~ td')
    if elements:
        kana = elements[0].find("p").get_text().strip()
        vendor["business_name_kana"] = kana
        vendor["business_name"] = elements[0].get_text().strip().replace(kana, "", 1)
    else:
        vendor["business_name_kana"] = ""
        vendor["business_name"] = ""

    # 代表者の氏名
    elements = soup.select('th:-soup-contains("代表者の氏名") ~ td')
    if elements:
        kana = elements[0].find("p").get_text().strip()
        vendor["representative_name_kana"] = kana
        vendor["representative_name"] = elements[0].get_text().strip().replace(kana, "", 1)
    else:
        vendor["representative_name_kana"] = ""
        vendor["representative_name"] = ""

    # 主たる営業所の所在地
    elements = soup.select('th:-soup-contains("主たる営業所の所在地") ~ td')
    if elements:
        parse_address = [el for el in elements[0].contents if el.get_text() != '']
        vendor["postal"] = parse_address[0].replace("〒", "")
        vendor["prefecture"] = re.match('東京都|北海道|(?:京都|大阪)府|.{2,3}県' , parse_address[1]).group()
        vendor["city"] = parse_address[1].replace(vendor["prefecture"], "")
        vendor["address"] = parse_address[2]

    # 電話番号
    elements = soup.select('th:-soup-contains("電話番号") ~ td')
    vendor["phone_number"] = elements[0].get_text().strip() if elements else ""

    # 資本金額
    elements = soup.select('th:-soup-contains("資本金額") ~ td')
    capital_amount = elements[0].get_text().strip() if elements else ""
    if capital_amount:
        vendor["capital_amount"] = capital_amount
        vendor["capital_amount_yen"] = re.search(r'[\d,]+', capital_amount).group().replace(",", "") + "000"
    else:
        vendor["capital_amount"] = ""
        vendor["capital_amount_yen"] = ""

    # 建設業以外の兼業の有無
    elements = soup.select('th:-soup-contains("建設業以外の兼業の有無") ~ td')
    vendor["other_business_involvement"] = elements[0].get_text().strip() if elements else ""

    # 許可を受けた建設業の種類の値
    elements = soup.select('.re_summ_odd > td')
    elements = elements[:29]
    for i, el in enumerate(elements):
        vendor[f"construction_type_{i}"] = el.get_text().strip()

    
    return vendor
