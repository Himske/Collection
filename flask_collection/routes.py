'''
Docstring
'''

import os
from flask import render_template, url_for, flash, redirect, request, current_app
from flask_login import login_user, current_user, logout_user, login_required
from flask_collection import app, bcrypt, db
from flask_collection.forms import BookForm, RegistrationForm, LoginForm, RequestResetForm, \
    UpdateAccountForm
from flask_collection.models import Book, User


@app.route('/')
@app.route('/home')
def home():
    books = Book.query.all()
    return render_template('home.html', books=books)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


@app.route('/add_book', methods=['GET', 'POST'])
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
        return redirect(url_for('home'))
    return render_template('add_book.html', title='Add Book', form=form)


@app.route('/book/<book_id>')
@login_required
def view_book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book.html', title=book.title, book=book)


@app.route('/book/<book_id>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('view_book', book_id=book.id))
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


@app.route('/book/<book_id>/delete', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash(f'Book deleted!', 'success')
    return redirect(url_for('home'))
