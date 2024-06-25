from bs4 import BeautifulSoup

def is_error_page(html):
    soup = BeautifulSoup(html, features='html.parser')
    el = soup.find('img', {'alt': '警告'})
    return True if el else False
