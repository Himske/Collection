import sys
import googlebooksapi
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc


class SearchWidget(qtw.QWidget):

    submitted = qtc.pyqtSignal(str, object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search_button = qtw.QPushButton('Search')
        layout = qtw.QHBoxLayout()
        self.isbn_string = qtw.QLineEdit('9781473232273')
        layout.addWidget(qtw.QLabel('ISBN'))
        layout.addWidget(self.isbn_string)
        layout.addWidget(self.search_button)
        self.setLayout(layout)
        self.search_button.clicked.connect(self.on_submit)

    def on_submit(self):
        book = googlebooksapi.get_raw_content(self.isbn_string.text())
        self.submitted.emit(f'Searching googlebooksapi for {self.isbn_string.text()}',
                            googlebooksapi.extract_data(book))


class GoogleBookWidget(qtw.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = qtw.QVBoxLayout()

        layout.addWidget(qtw.QLabel('Autor(s)'))
        self.authors = qtw.QLineEdit('')
        layout.addWidget(self.authors)

        layout.addWidget(qtw.QLabel('Title'))
        self.title = qtw.QLineEdit('')
        layout.addWidget(self.title)

        layout.addWidget(qtw.QLabel('Sub-Title'))
        self.sub_title = qtw.QLineEdit('')
        layout.addWidget(self.sub_title)

        layout.addWidget(qtw.QLabel('Description'))
        self.description = qtw.QPlainTextEdit('')
        layout.addWidget(self.description)

        layout.addWidget(qtw.QLabel('Publication date'))
        self.publication_date = qtw.QLineEdit('')
        layout.addWidget(self.publication_date)

        layout.addWidget(qtw.QLabel('Publisher'))
        self.publisher = qtw.QLineEdit('')
        layout.addWidget(self.publisher)

        layout.addWidget(qtw.QLabel('Language'))
        self.language = qtw.QLineEdit('')
        layout.addWidget(self.language)

        layout.addWidget(qtw.QLabel('ISBN-10'))
        self.isbn_10 = qtw.QLineEdit('')
        layout.addWidget(self.isbn_10)

        layout.addWidget(qtw.QLabel('ISBN-13'))
        self.isbn_13 = qtw.QLineEdit('')
        layout.addWidget(self.isbn_13)

        self.setLayout(layout)


class MainWindow(qtw.QMainWindow):

    def __init__(self):
        """MainWindow constructor."""
        super().__init__()

        self.resize(1280, 480)

        self.setWindowTitle('ISBN Search')

        self.menubar = qtw.QMenuBar(self)
        self.menubar.setGeometry(qtc.QRect(0, 0, 541, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.statusbar = qtw.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.search_widget = SearchWidget()
        self.search_widget.submitted.connect(self.show_status)
        # self.setCentralWidget(self.search_widget)

        self.google_book_widget = GoogleBookWidget()
        # self.setCentralWidget(self.google_book_widget)
        # self.addDockWidget(qtc.Qt.DockWidgetAreas.BottomDockWidgetArea, self.google_book_widget)

        central_widget = qtw.QWidget()
        layout = qtw.QVBoxLayout()
        layout.addWidget(self.search_widget)
        layout.addWidget(self.google_book_widget)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.show()

    @qtc.pyqtSlot(str, object)
    def show_status(self, status, book):
        self.statusbar.showMessage(status, 2000)
        if book:
            self.google_book_widget.authors.setText(str(book['authors']))
            self.google_book_widget.title.setText(str(book['title']))
            self.google_book_widget.sub_title.setText(str(book['subtitle']))
            self.google_book_widget.description.setPlainText(str(book['description']))
            self.google_book_widget.publication_date.setText(str(book['publication_date']))
            self.google_book_widget.publisher.setText(str(book['publisher']))
            self.google_book_widget.language.setText(str(book['language']))
            self.google_book_widget.isbn_10.setText(str(book['ISBN_10']))
            self.google_book_widget.isbn_13.setText(str(book['ISBN_13']))
        else:
            self.statusbar.showMessage('No book found', 5000)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
