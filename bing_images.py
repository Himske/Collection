import json
import requests
import urllib.request
from bs4 import BeautifulSoup

# TODO: put header in a constant, so it only appears once
header = {
    'User-Agent':
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
}

query_string = '9781401268008'

# TODO: get filter settings from gui
filter_string = '+filterui:imagesize-large+filterui:aspect-tall'
# filter_string = 'filterui:imagesize-wallpaper+filterui:aspect-tall'

base_url = 'https://www.bing.com/images/search'

url = f'{base_url}?&q={query_string}&qft={filter_string}&FORM=IRFLTR'

image = urllib.request.urlopen(urllib.request.Request(url=url, headers=header))

image_soup = BeautifulSoup(image, 'html.parser')

for a in image_soup.find_all("a", {"class": "iusc"}):
    m = json.loads(a["m"])
    murl = m["murl"]  # mobile image
    turl = m["turl"]  # desktop image
    # print(turl)
    image = requests.get(turl)  # use to write image.content to a file, see comic_book_find.py :: get_image

print()
