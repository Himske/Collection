import json
import requests


def get_raw_content(isbn: str) -> dict:
    book = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}')
    content = book.content.decode(book.encoding)

    return json.JSONDecoder().raw_decode(s=content)[0]


def extract_data(book_dict: dict) -> dict:
    data = dict()
    if 'items' in book_dict:
        books = book_dict['items']
        for book in books:
            volume = book['volumeInfo']

            data['authors'] = volume['authors']

            data['title'] = volume['title']

            if 'subtitle' in volume:
                data['subtitle'] = volume['subtitle']

            data['publication_date'] = volume['publishedDate']

            data['language'] = volume['language']

            for isbn in volume['industryIdentifiers']:
                if isbn['type'] == 'ISBN_10':
                    data['ISBN_10'] = isbn['identifier']
                if isbn['type'] == 'ISBN_13':
                    data['ISBN_13'] = isbn['identifier']

            if 'pageCount' in volume:
                data['pages'] = volume['pageCount']

            if 'publisher' in volume:
                data['publisher'] = volume['publisher']

            if 'description' in volume:
                data['description'] = volume['description']

            data['image_links'] = volume['imageLinks']

            sale_info = book['saleInfo']
            data['country'] = sale_info['country']

    return data


if __name__ == '__main__':
    # book = get_raw_content('9789189538580')
    # book = get_raw_content('9789176424513')  # subtitle
    book = get_raw_content('9781473232273')  # boxset

    if book['totalItems'] > 0:
        print(extract_data(book))
    else:
        print('No book found')
