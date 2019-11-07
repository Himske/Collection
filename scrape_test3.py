'''
Docstring
'''
import bs4 as bs
from requests_html import HTMLSession

SESSION = HTMLSession()

# SEARCH_URL = 'https://us.nicebooks.com/search/isbn'
SEARCH_URL = 'https://us.nicebooks.com/search'
# PARAMS = {'isbn': '9780307593962'} # author and introduction
# PARAMS = {'isbn': '9780553382563'} # only author
# PARAMS = {'isbn': '9780765319197'} # with subtitle
# PARAMS = {'isbn': '9781779501202'} # Doomsday Clock Part 1
# PARAMS = {'isbn': '9781401220884'} # Superman : Brainiac
PARAMS = {'q': '9780553382563'}

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

RESPONSE = SESSION.get(SEARCH_URL, params=PARAMS, headers=HEADERS)

RESPONSE.html.render()

# soup = bs.BeautifulSoup(RESPONSE.text, 'lxml')
soup = bs.BeautifulSoup(RESPONSE.html.html, 'html5lib')

BOOK_URL = 'https://us.nicebooks.com' + soup.find('a', attrs={'class': 'title'}).get('href')
RESPONSE = SESSION.get(BOOK_URL, headers=HEADERS)

soup = bs.BeautifulSoup(RESPONSE.text, 'html5lib')

title = soup.find('span', attrs={'itemprop': 'name'})
if title:
    print(f'Title: {title.text}')

sub_title = soup.find('small', attrs={'itemprop': 'alternativeHeadline'})
if sub_title:
    print(f'Sub-Title: {sub_title.text.strip()}')

author = soup.find(itemprop='author')
if author:
    print(f'Autor: {author.span.text}')

publisher = soup.find('a', attrs={'itemprop': 'publisher'})
if publisher:
    print(f'Publisher: {publisher.text}')

publication_date = soup.find('div', attrs={'itemprop': 'datePublished'}).get('content')
if publication_date:
    print(f'Publication Date: {publication_date}')

language_iso = soup.find('div', attrs={'itemprop': 'inLanguage'}).get('content')
if language_iso:
    print(f'Language ISO: {language_iso}')

language = soup.find('div', attrs={'itemprop': 'inLanguage'})
if language:
    print(f'Language: {language.text}')

book_format = soup.find('link', attrs={'itemprop': 'bookFormat'})
if book_format:
    print(f'Book Format: {book_format.find_parent("div").text.strip()}')

nof_pages = soup.find('div', attrs={'itemprop': 'numberOfPages'})
if nof_pages:
    print(f'Number of pages: {nof_pages.text}')

isbn_list = soup.find_all('div', attrs={'itemprop': 'isbn'})
if isbn_list:
    for isbn in isbn_list:
        if isbn.find_previous_sibling('div').text == 'ISBN-10':
            isbn_10 = isbn.text
            print(f'ISBN 10: {isbn_10}')
        else:
            isbn_13 = isbn.text
            print(f'ISBN 13: {isbn_13}')

# TODO: check that isbn_13 isn't None
image_url = soup.find('img', attrs={'itemprop': 'image'}).get('src')
if image_url:
    remote_image = SESSION.get(image_url)
    with open(f'images/{isbn_13}.jpg', 'wb') as local_image:
        local_image.write(remote_image.content)
    image_name = local_image.name[7:] # if folder name is images
    print(f'Image name: {image_name}')
    image_url = image_url[:image_url.rfind('?')]
    remote_image = SESSION.get(image_url)
    with open(f'images/{isbn_13}_large.jpg', 'wb') as large_image:
        large_image.write(remote_image.content)

description = soup.find('p', attrs={'itemprop': 'description'})
if description:
    print(f'Description: {description.text}')