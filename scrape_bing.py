'''
Docstring
'''
import bs4 as bs
from requests_html import HTMLSession

SESSION = HTMLSession()

SEARCH_URL = 'https://www.bing.com/images/search'
PARAMS = {'q': 'påtaglig fara bok tom clancy'}

HEADERS = {
    'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'sv-SE, sv; q=0.8, en-US; q=0.5, en; q=0.3',
    # 'Cache-Control': 'max-age=0',
    # 'Connection': 'Keep-Alive',
    'Host': 'www.bing.com',
    'Referer': 'www.bing.com/images/search',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
}

RESPONSE = SESSION.get(SEARCH_URL, params=PARAMS, headers=HEADERS)

RESPONSE.html.render(timeout=32, wait=0.5)

# soup = bs.BeautifulSoup(RESPONSE.text, 'lxml')
soup = bs.BeautifulSoup(RESPONSE.html.html, 'html5lib')

image_link_divs = soup.find_all('div', attrs={'class': 'imgpt'})

image_no = 1

for image_link_div in image_link_divs:
    image_url = 'https://www.bing.com' + image_link_div.a.get('href')
    image_response = SESSION.get(image_url, headers=HEADERS)
    soup = bs.BeautifulSoup(image_response.html.html, 'html5lib')

    '''
    with open(f'images/test{image_no}.jpg', 'wb') as local_image:
        local_image.write(image_response.content)
    '''
    image_no += 1
    print('======================================================================================')
