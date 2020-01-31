'''
Docstring
'''

from flask import Blueprint
from flask import render_template, request
from flask_collection.models import Book


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    books = Book.query.order_by(Book.author.asc(), Book.title.asc())\
        .paginate(page=page, per_page=25)
    return render_template('home.html', books=books)
