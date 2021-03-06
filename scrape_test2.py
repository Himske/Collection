'''
Docstring
'''
import bs4 as bs
import requests

SESSION = requests.Session()

BOOK_URL = 'https://isbndb.com/book/9781779501202'
# PARAMS = {'isbn': '9780307593962'} # author and introduction
# PARAMS = {'isbn': '9780553382563'} # only author
# PARAMS = {'isbn': '9780765319197'} # with subtitle
PARAMS = {'isbn': '9781779501202'} # Doomsday Clock Part 1

HEADERS = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'sv-SE, sv; q=0.8, en-US; q=0.5, en; q=0.3',
    'Cache-Control': 'no-cache',
    'Connection': 'Keep-Alive',
    'Host': 'isbndb.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
}

RESPONSE = SESSION.get(BOOK_URL, headers=HEADERS)
# RESPONSE = SESSION.get(BOOK_URL, params=PARAMS, headers=HEADERS)

# soup = bs.BeautifulSoup(RESPONSE.text, 'lxml')
soup = bs.BeautifulSoup(RESPONSE.text, 'html5lib')

book_div = soup.find('div', attrs={'class': 'book-table'})

image_url = soup.find('object', attrs={'type': 'image/png'}).get('data')
if image_url:
    remote_image = SESSION.get(image_url)
    with open(f'images/{PARAMS["isbn"]}.jpg', 'wb') as local_image:
        local_image.write(remote_image.content)
    image_name = local_image.name[7:] # if folder name is images
    print(image_name)

for child in book_div.table.tbody.children:
    print(child)

'''
title = soup.find('span', attrs={'itemprop': 'name'})
if title:
    print(title.text)

image_url = soup.find('img', attrs={'itemprop': 'image'}).get('src')
if image_url:
    remote_image = SESSION.get(image_url)
    with open(f'images/{PARAMS["isbn"]}.jpg', 'wb') as local_image:
        local_image.write(remote_image.content)
    image_name = local_image.name[7:] # if folder name is images
    print(image_name)
    image_url = image_url[:image_url.rfind('?')]
    remote_image = SESSION.get(image_url)
    with open(f'images/{PARAMS["isbn"]}_large.jpg', 'wb') as large_image:
        large_image.write(remote_image.content)

sub_title = soup.find('small', attrs={'itemprop': 'alternativeHeadline'})
if sub_title:
    print(sub_title.text.strip())

author = soup.find(itemprop='author')
if author:
    print(author.span.text)

publisher = soup.find('a', attrs={'itemprop': 'publisher'})
if publisher:
    print(publisher.text)

publication_date = soup.find('div', attrs={'itemprop': 'datePublished'}).get('content')
if publication_date:
    print(publication_date)

language_iso = soup.find('div', attrs={'itemprop': 'inLanguage'}).get('content')
if language_iso:
    print(language_iso)

language = soup.find('div', attrs={'itemprop': 'inLanguage'})
if language:
    print(language.text)

book_format = soup.find('link', attrs={'itemprop': 'bookFormat'})
if book_format:
    print(book_format.find_parent('div').text.strip())

nof_pages = soup.find('div', attrs={'itemprop': 'numberOfPages'})
if nof_pages:
    print(nof_pages.text)

isbn_list = soup.find_all('div', attrs={'itemprop': 'isbn'})
if isbn_list:
    for isbn in isbn_list:
        if isbn.find_previous_sibling('div').text == 'ISBN-10':
            isbn_10 = isbn.text
            print(isbn_10)
        else:
            isbn_13 = isbn.text
            print(isbn_13)

description = soup.find('p', attrs={'itemprop': 'description'})
if description:
    print(description.text)
'''
