import pandas as pd
import time
import requests
import functions
from classes import Book, Author, Publisher, Category
from database import Database

db = Database('testing.db')

category_count, author_count,  publisher_count = 112, 409, 349


def urlize_image(isbn):
    image_url = 'https://covers.openlibrary.org/b/isbn/' + isbn + '-L.jpg'
    return image_url


def add_book(title, author, category, publication_year, isbn13, numpages, publisher, average_rating, ratings_count):
    global category_count, author_count,  publisher_count
    book_image_url = urlize_image(isbn13)

    # check if category exists. if not, add category
    category_id = db.get_category_id(category)
    if not category_id:
        new_category = Category(None, category)
        db.insert_category(new_category)
        category_count += 1

    # check if author exists. if not, add author
    author_id = db.get_author_id(author)
    if not author_id:
        description = functions.get_description_of_author(authorName=author)
        birthday = functions.get_birthday_of_author(authorName=author)
        author_image_url = functions.get_image_url_of_author(authorName=author)
        new_author = Author(
            None, author, birthday, description, author_image_url)
        db.insert_author(new_author)
        author_count += 1

    # check if publisher exists. if not, add publisher
    publisher_id = db.get_publisher_id(publisher)
    if not publisher_id:
        new_publisher = Publisher(None, publisher)
        db.insert_publisher(new_publisher)
        publisher_count += 1

    # Create book object
    new_book = Book(None, title, average_rating, numpages, ratings_count, publication_year, author_count,
                    isbn13, publisher_count, book_image_url, category_count)

    # Add book to database
    db.insert_book(new_book)


data = pd.read_csv('newBooks.csv')


for i in range(728, len(data)):
    row = data.iloc[i].values
    title = str(row[1])
    category = str(row[2])
    author = str(row[3])
    average_rating = float(row[4])
    isbn13 = str(row[5])
    numpages = int(row[6])
    ratings_count = int(row[7])
    publication_year = int(row[8])
    publisher = str(row[9])

    add_book(title, author, category, publication_year, isbn13,
             numpages, publisher, average_rating, ratings_count)
