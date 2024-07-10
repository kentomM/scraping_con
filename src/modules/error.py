from bs4 import BeautifulSoup

def is_error_page(html):
    soup = BeautifulSoup(html, features='html.parser')
    el = soup.find('img', {'alt': '警告'})
    return True if el else False

def is_confirm_page(html):
    soup = BeautifulSoup(html, features='html.parser')
    h1_text = soup.find('h1').text if soup.find('h1') else ''
    text = "Let's confirm you are human"
    return True if h1_text == text else False
