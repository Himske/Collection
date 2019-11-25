'''
Docstring
'''

from flask import Flask, render_template, url_for, flash, redirect
from forms import BookForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'c1f527892b63e6654766d74a389ffdf9'

books = [
    {
        'author': 'Isaac Asimov',
        'title': 'The End of Eternity',
        'sub_title': 'A Novel',
        'volume': None,
        'publication_date': '2011-03-29',
        'format': 'Paperback',
        'pages': '256',
        'publisher': 'Orb Books',
        'cover': '9780765319197.jpg',
        'language': 'English',
        'language_iso': 'en',
        'isbn_13': '9780765319197',
        'isbn_10': '0765319195',
        'description': "One of Isaac Asimov’s SF masterpieces, this stand-alone novel is a monument of the flowering of SF in the 20th century. It is widely regarded as Asimov’s single best SF novel and one every SF fan should read.Andrew Harlan is an Eternal, a member of the elite of the future. One of the few who live in Eternity, a location outside of place and time, Harlan’s job is to create carefully controlled and enacted Reality Changes. These Changes are small, exactingly calculated shifts in the course of history made for the benefit of humankind. Though each Change has been made for the greater good, there are always costs.During one of his assignments, Harlan meets and falls in love with Noÿs Lambent, a woman who lives in real time and space. Then Harlan learns that Noÿs will cease to exist after the next change, and risks everything to sneak her into Eternity.Unfortunately, they are caught. Harlan’s punishment? His next assignment: kill the woman he loves before the paradox they have created results in the destruction of Eternity."
    },
    {
        'author': 'Isaac Asimov',
        'title': 'I, Robot',
        'sub_title': None,
        'volume': None,
        'publication_date': '2008-04-29',
        'format': 'Paperback',
        'pages': '256',
        'publisher': 'Spectra',
        'cover': '9780553382563.jpg',
        'language': 'English',
        'language_iso': 'en',
        'isbn_13': '9780553382563',
        'isbn_10': '055338256X',
        'description': "Dr. Susan Calvin is a 75-year-old Robopsychologyist retiring from U.S. Robots in the year 2057 when she is interviewed by a reporter from the Interplanetary Press. Her interview forms the narrative of this novel, covering her participation in the development of independent, sensible, and rational robots, ruled by the three entrenched laws of robotics, and the many lessons of her career that have led her to contend that robots are more human than people and that they are vital to human survival."
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', books=books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    '''Endpoint for form for adding book'''
    form = BookForm()
    if form.validate_on_submit():
        flash(f'Book added!', 'success')
        return redirect(url_for('home'))
    return render_template('add_book.html', title='Add Book', form=form)

if __name__ == '__main__':
    app.run()
