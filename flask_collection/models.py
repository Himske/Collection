'''
Docstring
'''

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from flask_collection import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        serializer = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return serializer.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

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
