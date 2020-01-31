'''
Docstring
'''

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_required
from flask_collection import db
from flask_collection.books.forms import BookForm
from flask_collection.models import Book


books = Blueprint('books', __name__)


@books.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    '''Endpoint for form for adding book'''
    form = BookForm()
    if form.validate_on_submit():
        cover_file = 'placeholder.png'
        if form.cover.data:
            cover_file = form.cover.data.filename
        book = Book(author=form.author.data,
                    title=form.title.data,
                    sub_title=form.sub_title.data,
                    org_title=form.org_title.data,
                    org_sub_title=form.org_sub_title.data,
                    volume=form.volume.data,
                    publication_date=form.publication_date.data,
                    org_publication_year=form.org_publication_year.data,
                    print_format=form.print_format.data,
                    pages=form.pages.data,
                    publisher=form.publisher.data,
                    cover=cover_file,
                    language=form.language.data,
                    language_iso=form.language_iso.data,
                    isbn_13=form.isbn_13.data,
                    isbn_10=form.isbn_10.data,
                    description=form.description.data)
        db.session.add(book)
        db.session.commit()
        flash(f'Book added!', 'success')
        return redirect(url_for('main.home'))
    return render_template('add_book.html', title='Add Book', form=form)


@books.route('/book/<book_id>')
def view_book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book.html', title=book.title, book=book)


@books.route('/book/<book_id>/update', methods=['GET', 'POST'])
@login_required
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookForm()

    if form.validate_on_submit():
        book.author = form.author.data
        book.title = form.title.data
        book.sub_title = form.sub_title.data
        book.org_title = form.org_title.data
        book.org_sub_title = form.org_sub_title.data
        book.volume = form.volume.data
        book.publication_date = form.publication_date.data
        book.org_publication_year = form.org_publication_year.data
        book.print_format = form.print_format.data
        book.pages = form.pages.data
        book.publisher = form.publisher.data
        if form.cover.data:
            book.cover = form.cover.data.filename
        book.language = form.language.data
        book.language_iso = form.language_iso.data
        book.isbn_13 = form.isbn_13.data
        book.isbn_10 = form.isbn_10.data
        book.description = form.description.data
        db.session.commit()
        flash(f'Book updated!', 'success')
        return redirect(url_for('books.view_book', book_id=book.id))
    elif request.method == 'GET':
        form.author.data = book.author
        form.title.data = book.title
        form.sub_title.data = book.sub_title
        form.org_title.data = book.org_title
        form.org_sub_title.data = book.org_sub_title
        form.volume.data = book.volume
        form.publication_date.data = book.publication_date
        form.org_publication_year.data = book.org_publication_year
        form.print_format.data = book.print_format
        form.pages.data = book.pages
        form.publisher.data = book.publisher
        form.cover.data = book.cover # TODO: This needs some fix since nothing is showing
        form.language.data = book.language
        form.language_iso.data = book.language_iso
        form.isbn_13.data = book.isbn_13
        form.isbn_10.data = book.isbn_10
        form.description.data = book.description
    
    return render_template('add_book.html', title='Update Book', form=form)


@books.route('/book/<book_id>/delete', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash(f'Book deleted!', 'success')
    return redirect(url_for('main.home'))


@books.route('/author/<string:author>')
def books_by_author(author):
    page = request.args.get('page', 1, type=int)
    books = Book.query.filter_by(author=author)\
        .order_by(Book.author.asc(), Book.title.asc())\
        .paginate(page=page, per_page=25)
    return render_template('books_by_author.html', books=books, author=author)
