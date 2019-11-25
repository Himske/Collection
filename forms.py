'''
Docstring
'''

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, FileField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class BookForm(FlaskForm):
    author = StringField('Author', validators=[DataRequired(), Length(min=2, max=50)])
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=50)])
    sub_title = StringField('Sub Title', validators=[Optional(), Length(min=2, max=50)])
    volume = StringField('Volume', validators=[Optional()])
    publication_date = DateField('Publication Date', validators=[Optional()])
    print_format = StringField('Format', validators=[Optional(), Length(min=2, max=20)])
    pages = IntegerField('Pages', validators=[Optional(), NumberRange(max=2000)])
    publisher = StringField('Publisher', validators=[Optional(), Length(min=2, max=20)])
    cover = FileField('Cover', validators=[Optional()])
    language = StringField('Language', validators=[Optional()])
    language_iso = StringField('ISO Language', validators=[Optional()])
    isbn_13 = StringField('ISBN-13', validators=[Optional()])
    isbn_10 = StringField('ISBN-10', validators=[Optional()])
    description = TextAreaField('Description')
    submit = SubmitField('Add Book')
