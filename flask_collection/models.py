'''
Docstring
'''

from flask_collection import db

class Book(db.Model):
    '''Docstring'''
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    sub_title = db.Column(db.String(50))
    volume = db.Column(db.Integer)
    publication_date = db.Column(db.DateTime)
    print_format = db.Column(db.String(20))
    pages = db.Column(db.Integer)
    publisher = db.Column(db.String(20))
    cover = db.Column(db.String(20))
    language = db.Column(db.String(20))
    language_iso = db.Column(db.String(2))
    isbn_13 = db.Column(db.String(13))
    isbn_10 = db.Column(db.String(10))
    description = db.Column(db.Text)

    def __repr__(self):
        return f'{self.title} written by {self.author}'
