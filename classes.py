import datetime


class Book:
    def __init__(self, id, title, average_rating, num_pages, ratings_count, publication_year, authorID, isbn, publisherID, image_url, categoryID):
        self.id = id
        self.title = title
        self.average_rating = average_rating
        self.num_pages = num_pages
        self.ratings_count = ratings_count
        self.publication_year = publication_year
        self.authorID = authorID
        self.isbn = isbn
        self.publisherID = publisherID
        self.image_url = image_url
        self.categoryID = categoryID


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
        self.evaluationDate = datetime.date.today()


class Library:
    def __init__(self, id, userID, bookID, source):
        self.id = id
        self.userID = userID
        self.bookID = bookID
        self.adding_date = datetime.date.today()
        self.source = source


class Publisher:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Request:
    def __init__(self, id, userID, bookID, source):
        self.id = id
        self.userID = userID
        self.bookID = bookID
        self.requestDate = datetime.date.today()
        self.source = source
