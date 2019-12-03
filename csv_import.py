import pandas as pd

df = pd.read_csv('books.csv', encoding='utf-8')

df.columns = ['title', 'sub_title', 'author', 'publisher', 'publication_year', 'original_title', 'original_subtitle', 'purchase_date', 'my_rating', 'cover', 'categories', 'isbn', 'took', 'notes', 'format', 'read_it', 'description']

for row in df.itertuples(index=False):
    # Title, _1, Author, Publisher, _4, _5, _6, _7, _8, Cover, Categories, ISBN, Took, Notes, Format, _15, Description = row
    title, sub_title, author, publisher, publication_year, original_title, original_subtitle, purchase_date, my_rating, cover, categories, isbn, took, notes, format, read_it, description = row
    print(author, title, isbn)
