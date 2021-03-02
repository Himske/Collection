import bs4 as bs
import pandas as pd
from requests_html import HTMLSession
from urllib3.exceptions import ProtocolError
from typing import Optional

BASE_URL = 'https://us.nicebooks.com'
SEARCH_URL = f'{BASE_URL}/search'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 '\
    'Safari/537.36 Edg/88.0.705.74'

HEADERS = {
    'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'sv-SE, sv; q=0.8, en-US; q=0.5, en; q=0.3',
    # 'Cache-Control': 'max-age=0',
    # 'Connection': 'Keep-Alive',
    'Host': 'us.nicebooks.com',
    'Referer': f'{SEARCH_URL}/isbn',
    'User-Agent': USER_AGENT
}


def get_book_url(search_isbn: str):
    '''
    Gets a beautifulsoup object based on the request to the ISBN search page
    '''
    session = HTMLSession()
    book_url: str = None
    with session.get(SEARCH_URL, params={'q': search_isbn}, headers=HEADERS) as response:
        response.html.render()
        # soup = bs.BeautifulSoup(RESPONSE.text, 'lxml')
        search_result = bs.BeautifulSoup(response.html.html, 'html5lib')

    try:
        book_url = f"{BASE_URL}{search_result.find('a', attrs={'class': 'title'}).get('href')}"
    except AttributeError:
        return None
    except ConnectionError:
        return None
    except ProtocolError:
        return None

    return book_url


def get_book_html(search_isbn: str) -> Optional[bs.BeautifulSoup]:
    '''
    Gets a beautifulsoup object for a book
    '''
    book_url = get_book_url(search_isbn)
    if book_url:
        session = HTMLSession()
        response = session.get(book_url, headers=HEADERS)
        book = bs.BeautifulSoup(response.text, 'html5lib')
        return book
    return None


def get_book_info(isbn: str) -> Optional[bs.BeautifulSoup]:
    '''Gets html for a book from us.nicebooks.com'''
    retries = 0
    book = get_book_html(isbn)
    while book is None and retries < 3:
        book = get_book_html(isbn)
        retries += 1
    return book


if __name__ == '__main__':
    # isbn = input('ISBN-13: ')
    isbn = '9781943591091'
    book = get_book_info(isbn)
    if book:
        print(book.prettify())
    else:
        print("Didn't find anything")
