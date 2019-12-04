'''
Docstring
'''

import os
import filecmp
import pandas as pd
from requests_html import HTMLSession
from flask_collection.models import Book
from flask_collection import db

SESSION = HTMLSession()

df = pd.read_csv('books.csv', encoding='utf-8')

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

for row in df.itertuples(index=False):
    title, sub_title, author, publisher, publication_year, original_title, original_subtitle, \
        purchase_date, my_rating, cover, categories, isbn, took, notes, print_format, read_it, \
            description = row
    book = Book()
    book.author = author if not pd.isna(author) else 'Various'
    book.title = title if not pd.isna(title) else None
    book.sub_title = sub_title if not pd.isna(sub_title) else None
    book.org_title = original_title if not pd.isna(original_title) else None
    book.org_sub_title = original_subtitle if not pd.isna(original_subtitle) else None
    book.publisher = publisher if not pd.isna(publisher) else None
    book.org_publication_year = int(publication_year) if not pd.isna(publication_year) else None
    book.print_format = print_format if not pd.isna(print_format) else None
    book.description = description if not pd.isna(description) else None

    if not pd.isna(isbn):
        if len(isbn) == 13:
            book.isbn_13 = isbn
        else:
            book.isbn_10 = isbn

    image_url = cover if not pd.isna(cover) else None
    if image_url:
        remote_image = SESSION.get(image_url)
        with open(f'flask_collection/static/cover_images/{isbn}.jpg', 'wb') as local_image:
            local_image.write(remote_image.content)
            image_name = local_image.name[37:]
            # print(f'Image name: {image_name}')
        if filecmp.cmp(f'flask_collection/static/cover_images/{image_name}',
                       'flask_collection/static/cover_images/image_not_available.jpg'):
            os.remove(f'flask_collection/static/cover_images/{image_name}')
        else:
            book.cover = image_name
        '''
        image_url = image_url[:image_url.rfind('?')]
        remote_image = SESSION.get(image_url)
        with open(f'images/{isbn_13}_large.jpg', 'wb') as large_image:
            large_image.write(remote_image.content)
        '''
    db.session.add(book)
    db.session.commit()
