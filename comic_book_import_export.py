'''
Importing old comic book info from old csv file
if image url exists try to fetch the image and store it in a local folder
If isbn exists run scrape
If scrape is successfull store the grabbed information in a csv file and store any images in a
local folder
'''

import os
import math
import filecmp
import csv
import bs4 as bs
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
    session = HTMLSession()
    with session.get(SEARCH_URL, params={'q': search_isbn}, headers=HEADERS) as response:
        response.html.render()
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
    session = HTMLSession()
    image_name = None
    try:
        image_url = soup.find('img', attrs={'itemprop': 'image'}).get('src')
    except AttributeError:
        image_url = None
    if image_url:
        remote_image = session.get(image_url)
        with open(f'flask_collection/static/comic_book_covers/{isbn_13}.jpg', 'wb') as local_image:
            local_image.write(remote_image.content)
        image_name = local_image.name[42:]
        image_url = image_url[:image_url.rfind('?')]
        remote_image = session.get(image_url)
        with open(f'flask_collection/static/comic_book_covers/{isbn_13}_large.jpg', 'wb') as large_image:
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

        '''
        print(f'Title: {book_title}')
        print(f'Sub-Title: {book_sub_title}')
        print(f'Autor: {book_author}')
        print(f'Publisher: {book_publisher}')
        print(f'Publication Date: {book_publication_date}')
        print(f'Language ISO: {book_language_iso}')
        print(f'Language: {book_language}')
        print(f'Book Format: {book_format}')
        print(f'Number of pages: {book_nof_pages}')
        print(f'Image name: {book_image_name}')
        print(f'Description: {book_description}')
        '''
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
    df = pd.read_csv('comic_books.csv', encoding='utf-8')

    df.columns = ['title',
                  'sub_title',
                  'author',
                  'publisher',
                  'publication_year',
                  'original_title',
                  'original_subtitle',
                  'purchase_date',
                  'my_rating',
                  'cover',
                  'categories',
                  'isbn',
                  'took',
                  'notes',
                  'format',
                  'read_it',
                  'description']
    return df


def get_book_info_from_df(df: pd.DataFrame):
    comic_books = list()
    for row in df.itertuples(index=False):
        book_dict = convert_row_to_dict(row)
        print(f"{book_dict['title']}")
        comic_book = {
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

        if book_dict['isbn'] and not math.isnan(book_dict['isbn']):
            comic_book = get_book_info(str(book_dict['isbn']))
            # print(f'{title}: {isbn}: {comic_book}')
            if book_dict['cover'] and not pd.isna(book_dict['cover']):
                get_old_image(book_dict['cover'], book_dict['isbn'])
        merged_dict = merge_old_and_new_info(book_dict, comic_book)
        comic_books.append(merged_dict)
    return comic_books


def merge_old_and_new_info(old_dict, updated_dict):
    merged = {
        'author': updated_dict['author'],
        'old_author': old_dict['author'],
        'title': updated_dict['title'],
        'old_title': old_dict['title'],
        'sub_title': updated_dict['sub_title'],
        'old_sub_title': old_dict['sub_title'],
        'publisher': updated_dict['publisher'],
        'old_publisher': old_dict['publisher'],
        'publication_date': updated_dict['publication_date'],
        'old_publication_year': old_dict['publication_year'],
        'old_original_title': old_dict['original_title'],
        'old_original_subtitle': old_dict['original_subtitle'],
        'old_purchase_date': old_dict['purchase_date'],
        'old_my_rating': old_dict['my_rating'],
        'image_name': updated_dict['image_name'],
        'old_cover': old_dict['cover'],
        'old_categories': old_dict['categories'],
        'isbn-13': updated_dict['isbn-13'],
        'isbn-10': updated_dict['isbn-10'],
        'old_isbn': old_dict['isbn'],
        'old_took': old_dict['took'],
        'old_notes': old_dict['notes'],
        'format': updated_dict['format'],
        'old_print_format': old_dict['print_format'],
        'nof_pages': updated_dict['nof_pages'],
        'old_read_it': old_dict['read_it'],
        'description': updated_dict['description'],
        'old_description': old_dict['description'],
        'language': updated_dict['language'],
        'language_iso': updated_dict['language_iso']
    }
    return merged


def get_old_image(cover, isbn):
    image_url = cover
    if image_url:
        session = HTMLSession()
        remote_image = session.get(image_url)
        with open(f'flask_collection/static/comic_book_covers/{isbn}_old.jpg', \
                'wb') as local_image:
            local_image.write(remote_image.content)
            image_name = local_image.name[42:]
            # print(f'Image name: {image_name}')
        if filecmp.cmp(f'flask_collection/static/comic_book_covers/{image_name}',
                       'flask_collection/static/comic_book_covers/image_not_available.jpg'):
            os.remove(f'flask_collection/static/comic_book_covers/{image_name}')


def convert_row_to_dict(row):
    return {
        'title': row[0],
        'sub_title': row[1],
        'author': row[2],
        'publisher': row[3],
        'publication_year': int(row[4]) if not math.isnan(row[4]) else None,
        'original_title': row[5],
        'original_subtitle': row[6],
        'purchase_date': row[7],
        'my_rating': row[8],
        'cover': row[9],
        'categories': row[10],
        'isbn': int(row[11]) if not math.isnan(row[11]) else None,
        'took': row[12],
        'notes': row[13],
        'print_format': row[14],
        'read_it': row[15],
        'description': row[16]
    }


def import_export_book_info():
    comic_book_df = get_df_from_csv()
    comic_book_list = get_book_info_from_df(comic_book_df)
    with open('comic_book_export_fc.csv', 'w', encoding='utf-8', newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=comic_book_list[0].keys())
        fc.writeheader()
        fc.writerows(comic_book_list)
    out_df = pd.DataFrame(comic_book_list)
    out_df.to_csv('comic_book_export_df.csv')


if __name__ == '__main__':
    import_export_book_info()
