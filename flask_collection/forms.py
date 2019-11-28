'''
Docstring
'''

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, DateField, SubmitField, TextAreaField, \
    PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, Email, EqualTo, \
    ValidationError
from flask_login import current_user
from flask_collection.models import User

class BookForm(FlaskForm):
    author = StringField('Author', validators=[DataRequired(), Length(min=2, max=50)])
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=50)])
    sub_title = StringField('Sub Title', validators=[Optional(), Length(min=2, max=50)])
    volume = StringField('Volume', validators=[Optional()])
    publication_date = DateField('Publication Date', validators=[Optional()])
    print_format = StringField('Format', validators=[Optional(), Length(min=2, max=20)])
    pages = IntegerField('Pages', validators=[Optional(), NumberRange(max=2000)])
    publisher = StringField('Publisher', validators=[Optional(), Length(min=2, max=20)])
    cover = FileField('Cover', validators=[FileAllowed(['jpg', 'png']), Optional()])
    language = StringField('Language', validators=[Optional()])
    language_iso = StringField('ISO Language', validators=[Optional()])
    isbn_13 = StringField('ISBN-13', validators=[Optional()])
    isbn_10 = StringField('ISBN-10', validators=[Optional()])
    description = TextAreaField('Description')
    submit = SubmitField('Add Book')


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
