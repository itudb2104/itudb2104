import datetime


class Book:
    def __init__(self, id, title, average_rating, num_pages, ratings_count, publication_year, author, year, isbn, publisher, image_url, category):
        self.id = id
        self.title = title
        self.average_rating = average_rating
        self.num_pages = num_pages
        self.ratings_count = ratings_count
        self.publication_year = publication_year
        self.author = author
        self.isbn = isbn
        self.publisher = publisher
        self.image_url = image_url
        self.category = category


class Author:
    def __init__(self, id, name, birthday, description, image_url):
        self.id = id
        self.name = name
        self.birthday = birthday
        self.biography = description
        self.image_url = image_url


class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class User:
    def __init__(self, id, fullname, username, password, email, gender, birthday):
        self.id = id
        self.fullname = fullname
        self.username = username
        self.password = password
        self.email = email
        self.gender = gender
        self.birthday = birthday


class Evaluation:
    def __init__(self, id, bookID, userID, text, vote):
        self.id = id
        self.bookID = bookID
        self.userID = userID
        self.text = text
        self.vote = vote


class Library:
    def __init__(self, id, userID, bookID, source):
        self.id = id
        self.userID = userID
        self.bookID = bookID
        self.adding_date = datetime.datetime.now()
        self.source = source


class Publisher:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class RequestBook:
    def __init__(self, id, userID, bookID, explanation):
        self.id = id
        self.userID = userID
        self.bookID = bookID
        self.requestDate = datetime.datetime.now()
        self.explanation = explanation
