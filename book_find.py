'''
Find a book based on ISBN and adding it to the csv file.
'''

import bs4 as bs
import math
import pandas as pd

from requests_html import HTMLSession
from urllib3.exceptions import ProtocolError

SEARCH_URL = 'https://us.nicebooks.com/search'

HEADERS = {
    'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'sv-SE, sv; q=0.8, en-US; q=0.5, en; q=0.3',
    # 'Cache-Control': 'max-age=0',
    # 'Connection': 'Keep-Alive',
    'Host': 'us.nicebooks.com',
    'Referer': 'https://us.nicebooks.com/search/isbn',
    # 'User-Agent': 'my-app/0.0.1'
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '\
    '(KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
}


def get_soup(search_isbn: str):
    '''
    Gets a beautifulsoup object based on the result of the second url request\n
    The first request is to the ISBN search page and the second is to the actual result page
    '''
    with HTMLSession() as session:
        with session.get(SEARCH_URL, params={'q': search_isbn}, headers=HEADERS) as response:
            try:
                response.html.render(timeout=32, wait=0.5)
            except TimeoutError:
                return None
            except ConnectionResetError:
                return None
            # soup = bs.BeautifulSoup(RESPONSE.text, 'lxml')
            soup = bs.BeautifulSoup(response.html.html, 'html5lib')
            try:
                book_url = 'https://us.nicebooks.com' + \
                    soup.find('a', attrs={'class': 'title'}).get('href')
                response = session.get(book_url, headers=HEADERS)
                soup = bs.BeautifulSoup(response.text, 'html5lib')
            except AttributeError:
                soup = None
            except ConnectionError:
                soup = None
            except ProtocolError:
                soup = None
    return soup


def get_element_text(soup: bs.BeautifulSoup, tag, itemprop):
    '''Gets the text from a beautifulsoup element based on the tag and itemprop'''
    element = soup.find(tag, attrs={'itemprop': itemprop})
    if element:
        return element.text
    return None


def get_element_content(soup: bs.BeautifulSoup, tag, itemprop):
    '''Gets the content from a beautifulsoup element based on the tag and itemprop'''
    try:
        element = soup.find(tag, attrs={'itemprop': itemprop}).get('content')
    except AttributeError:
        element = None
    return element


def get_author(soup: bs.BeautifulSoup):
    '''Gets the author text from a beautifulsoup object'''
    author = soup.find(itemprop='author')
    if author:
        return author.span.text
    return None


def get_book_format(soup: bs.BeautifulSoup):
    '''Gets the book format from a beautifulsoup object'''
    print_format = soup.find('link', attrs={'itemprop': 'bookFormat'})
    if print_format:
        print_format = str(print_format.find_parent("div").text.strip())
        return print_format.replace('Format:', '')
    return None


def get_isbn_dict(soup: bs.BeautifulSoup):
    '''Gets ISBN-10 and ISBN-13 from a beautifulsoup object'''
    result = dict()
    isbn_list = soup.find_all('div', attrs={'itemprop': 'isbn'})
    if isbn_list:
        for isbn in isbn_list:
            if isbn.find_previous_sibling('div').text == 'ISBN-10':
                isbn_10 = isbn.text
                # print(f'ISBN 10: {isbn_10}')
                result.update({'isbn-10': isbn_10})
            else:
                isbn_13 = isbn.text
                # print(f'ISBN 13: {isbn_13}')
                result.update({'isbn-13': isbn_13})
    return result


def get_image(soup: bs.BeautifulSoup, isbn_13: str):
    '''
    Get cover image files and stores them in the cover_images folder\n
    Stores two sizes, one thumbnail and one large with isbn_13 as a name standard\n
    Returns the filename for the thumbnail version
    '''
    with HTMLSession() as session:
        image_name = None
        try:
            image_url = soup.find('img', attrs={'itemprop': 'image'}).get('src')
        except AttributeError:
            image_url = None
        if image_url:
            remote_image = session.get(image_url)
            with open(f'flask_collection/static/cover_images/{isbn_13}.jpg', 'wb') as local_image:
                local_image.write(remote_image.content)
            image_name = local_image.name[42:]
            image_url = image_url[:image_url.rfind('?')]
            remote_image = session.get(image_url)
            with open(f'flask_collection/static/cover_images/{isbn_13}_large.jpg', 'wb') as large_image:
                large_image.write(remote_image.content)
    return image_name


def get_book_info(isbn: str):
    '''Gets all the information on a book from us.nicebooks.com'''
    retries = 0
    book_soup = get_soup(isbn)
    while book_soup is None and retries < 3:
        book_soup = get_soup(isbn)
        retries += 1

    if book_soup:
        # book_title = get_title(book_soup)
        book_title = get_element_text(book_soup, 'span', 'name')
        book_sub_title = get_element_text(book_soup, 'small', 'alternativeHeadline')
        book_author = get_author(book_soup)
        book_publisher = get_element_text(book_soup, 'a', 'publisher')
        book_publication_date = get_element_content(book_soup, 'div', 'datePublished')
        book_language_iso = get_element_content(book_soup, 'div', 'inLanguage')
        book_language = get_element_text(book_soup, 'div', 'inLanguage')
        book_format = get_book_format(book_soup)
        book_nof_pages = get_element_text(book_soup, 'div', 'numberOfPages')
        isbn_dict = get_isbn_dict(book_soup)
        book_description = get_element_text(book_soup, 'p', 'description')
        if 'isbn-13' in isbn_dict.keys():
            book_image_name = get_image(book_soup, isbn_dict['isbn-13'])

        return {
            'author': book_author,
            'title': book_title,
            'sub_title': book_sub_title,
            'publisher': book_publisher,
            'publication_date': book_publication_date,
            'language': book_language,
            'language_iso': book_language_iso,
            'nof_pages': book_nof_pages,
            'format': book_format,
            'image_name': book_image_name,
            'isbn-13': isbn_dict['isbn-13'],
            'isbn-10': isbn_dict['isbn-10'],
            'description': book_description
        }

    return {
        'author': None,
        'title': None,
        'sub_title': None,
        'publisher': None,
        'publication_date': None,
        'language': None,
        'language_iso': None,
        'nof_pages': None,
        'format': None,
        'image_name': None,
        'isbn-13': None,
        'isbn-10': None,
        'description': None
    }


def get_df_from_csv():
    df = pd.read_csv('book_export_df2.csv', encoding='utf-8')

    df.columns = ['author',
                  'title',
                  'sub_title',
                  'org_title',
                  'org_sub_title',
                  'volume',
                  'publication_date',
                  'org_publication_year',
                  'print_format',
                  'pages',
                  'publisher',
                  'cover',
                  'language',
                  'language_iso',
                  'isbn-13',
                  'isbn-10',
                  'description']
    return df


def convert_to_df_format(row: dict) -> dict:
    return {'author': row['author'],
            'title': row['title'],
            'sub_title': row['sub_title'],
            'org_title': None,
            'org_sub_title': None,
            'volume': None,
            'publication_date': row['publication_date'],
            'org_publication_year': None,
            'print_format': row['format'],
            'pages': row['nof_pages'],
            'publisher': row['publisher'],
            'cover': row['image_name'],
            'language': row['language'],
            'language_iso': row['language_iso'],
            'isbn-13': row['isbn-13'],
            'isbn-10': row['isbn-10'],
            'description': row['description']
            }


def fetch_image(isbn: str):
    '''Gets all the information on a book from us.nicebooks.com'''
    retries = 0
    book_soup = get_soup(isbn)
    while book_soup is None and retries < 3:
        book_soup = get_soup(isbn)
        retries += 1

    if book_soup:
        isbn_dict = get_isbn_dict(book_soup)
        if 'isbn-13' in isbn_dict.keys():
            book_image_name = get_image(book_soup, isbn_dict['isbn-13'])


def is_found(book: dict) -> bool:
    if book['title']:
        return True
    return False


def find_and_add_book() -> None:
    input_var = input('ISBN-13: ')
    book = get_book_info(input_var)
    if is_found(book):
        book = convert_to_df_format(book)
        book_df = get_df_from_csv()
        book_df = book_df.append(book, ignore_index=True)
        book_df.to_csv('book_export_df2.csv', index=False)
    else:
        print("Didn't find any comic book")


def get_images() -> None:
    book_df = get_df_from_csv()
    isbn_13_list = book_df['isbn-13'].values
    book_counter = 1
    for isbn_13 in isbn_13_list:
        print(f'Fetching: {int(isbn_13)}, book {book_counter} of {len(isbn_13_list)}')
        if not math.isnan(isbn_13):
            fetch_image(str(int(isbn_13)))
        book_counter += 1


if __name__ == '__main__':
    find_and_add_book()
    # get_images()
