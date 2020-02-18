'''
Testfile for comic_book_find
'''

import pytest
from comic_book_find import is_found

@pytest.fixture
def not_found():
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

@pytest.fixture
def found():
    return {
        'author': 'Author',
        'title': 'Title',
        'sub_title': 'Sub-Title',
        'publisher': 'Publisher',
        'publication_date': '2020-02-18',
        'language': 'English',
        'language_iso': 'en',
        'nof_pages': 100,
        'format': 'Hardcover',
        'image_name': '12345678.jpg',
        'isbn-13': '1234567890123',
        'isbn-10': '1234567890',
        'description': 'Bla bla bla'
    }


def test_is_found(found):
    assert is_found(found)


def test_is_not_found(not_found):
    assert not is_found(not_found)
