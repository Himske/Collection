'''
Docstring
'''
import bs4 as bs
from requests_html import HTMLSession

SESSION = HTMLSession()

# SEARCH_URL = 'https://us.nicebooks.com/search/isbn'
SEARCH_URL = 'https://us.nicebooks.com/search'
# PARAMS = {'isbn': '9780307593962'} # author and introduction
# PARAMS = {'q': '9780553382563'} # only author
# PARAMS = {'q': '9780765319197'} # with subtitle
# PARAMS = {'isbn': '9781779501202'} # Doomsday Clock Part 1
# PARAMS = {'isbn': '9781401220884'} # Superman : Brainiac
# PARAMS = {'q': '9789171197078'}
PARAMS = {'q': '9789189128316'}

HEADERS = {
    'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'sv-SE, sv; q=0.8, en-US; q=0.5, en; q=0.3',
    # 'Cache-Control': 'max-age=0',
    # 'Connection': 'Keep-Alive',
    'Host': 'us.nicebooks.com',
    'Referer': 'https://us.nicebooks.com/search/isbn',
    # 'User-Agent': 'my-app/0.0.1'
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
}


def get_soup():
    response = SESSION.get(SEARCH_URL, params=PARAMS, headers=HEADERS)
    response.html.render()
    # soup = bs.BeautifulSoup(RESPONSE.text, 'lxml')
    soup = bs.BeautifulSoup(response.html.html, 'html5lib')
    try:
        book_url = 'https://us.nicebooks.com' + soup.find('a', attrs={'class': 'title'}).get('href')
        response = SESSION.get(book_url, headers=HEADERS)
        soup = bs.BeautifulSoup(response.text, 'html5lib')
    except:
        soup = None
    return soup


def get_element_text(soup: bs.BeautifulSoup, tag, itemprop):
    element = soup.find(tag, attrs={'itemprop': itemprop})
    if element:
        return element.text
    return None


def get_element_content(soup: bs.BeautifulSoup, tag, itemprop):
    try:
        element = soup.find(tag, attrs={'itemprop': itemprop}).get('content')
    except:
        element = None
    return element


def get_author(soup: bs.BeautifulSoup):
    author = soup.find(itemprop='author')
    if author:
        return author.span.text
    return None


def get_book_format(soup: bs.BeautifulSoup):
    book_format = soup.find('link', attrs={'itemprop': 'bookFormat'})
    if book_format:
        book_format = str(book_format.find_parent("div").text.strip())
        return book_format.replace('Format:', '')
    return None


def get_isbn_dict(soup: bs.BeautifulSoup):
    result = dict()
    isbn_list = soup.find_all('div', attrs={'itemprop': 'isbn'})
    if isbn_list:
        for isbn in isbn_list:
            if isbn.find_previous_sibling('div').text == 'ISBN-10':
                isbn_10 = isbn.text
                print(f'ISBN 10: {isbn_10}')
                result.update({'isbn-10': isbn_10})
            else:
                isbn_13 = isbn.text
                print(f'ISBN 13: {isbn_13}')
                result.update({'isbn-13': isbn_13})
    return result


def get_image(soup: bs.BeautifulSoup, isbn_13: str):
    try:
        image_url = soup.find('img', attrs={'itemprop': 'image'}).get('src')
    except:
        image_url = None
    if image_url:
        remote_image = SESSION.get(image_url)
        with open(f'flask_collection/static/cover_images/{isbn_13}.jpg', 'wb') as local_image:
            local_image.write(remote_image.content)
        image_name = local_image.name[37:]
        print(f'Image name: {image_name}')
        image_url = image_url[:image_url.rfind('?')]
        remote_image = SESSION.get(image_url)
        with open(f'flask_collection/static/cover_images/{isbn_13}_large.jpg', 'wb') as large_image:
            large_image.write(remote_image.content)


if __name__ == '__main__':
    retries = 0
    book_soup = get_soup()
    while book_soup is None and retries < 3:
        book_soup = get_soup()
        retries += 1

    if book_soup:
        # book_title = get_title(book_soup)
        book_title = get_element_text(book_soup, 'span', 'name')
        print(f'Title: {book_title}')
        book_sub_title = get_element_text(book_soup, 'small', 'alternativeHeadline')
        print(f'Sub-Title: {book_sub_title}')
        book_author = get_author(book_soup)
        print(f'Autor: {book_author}')
        book_publisher = get_element_text(book_soup, 'a', 'publisher')
        print(f'Publisher: {book_publisher}')
        book_publication_date = get_element_content(book_soup, 'div', 'datePublished')
        print(f'Publication Date: {book_publication_date}')
        book_language_iso = get_element_content(book_soup, 'div', 'inLanguage')
        print(f'Language ISO: {book_language_iso}')
        book_language = get_element_text(book_soup, 'div', 'inLanguage')
        print(f'Language: {book_language}')
        book_format = get_book_format(book_soup)
        print(f'Book Format: {book_format}')
        book_nof_pages = get_element_text(book_soup, 'div', 'numberOfPages')
        print(f'Number of pages: {book_nof_pages}')
        isbn_dict = get_isbn_dict(book_soup)
        book_description = get_element_text(book_soup, 'p', 'description')
        print(f'Description: {book_description}')
        if 'isbn-13' in isbn_dict.keys():
            get_image(book_soup, isbn_dict['isbn-13'])
