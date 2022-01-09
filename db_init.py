import sqlite3 as dbapi2

INIT_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        average_rating REAL NOT NULL,
        num_pages INTEGER NOT NULL,
        ratings_count INTEGER NOT NULL,
        publication_year INTEGER NOT NULL,
        authorID INTEGER NOT NULL,
        isbn TEXT NOT NULL,
        publisherID INTEGER NOT NULL,
        image_url TEXT NOT NULL,
        categoryID INTEGER NOT NULL,
        FOREIGN KEY (authorID) REFERENCES AUTHORS(id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (publisherID) REFERENCES PUBLISHERS(id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (categoryID) REFERENCES CATEGORIES(id) ON DELETE CASCADE ON UPDATE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS authors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        birthday TEXT,
        biography TEXT,
        image_url TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        email TEXT NOT NULL,
        gender INTEGER NOT NULL,
        birthday TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bookID INTEGER NOT NULL,
        userID INTEGER NOT NULL,
        text TEXT,
        vote INTEGER NOT NULL,
        FOREIGN KEY (bookID) REFERENCES BOOKS(id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (userID) REFERENCES USERS(id) ON DELETE CASCADE ON UPDATE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS libraries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userID INTEGER NOT NULL,
        bookID INTEGER NOT NULL,
        adding_date TIMESTAMP NOT NULL,
        source TEXT NOT NULL,
        FOREIGN KEY (userID) REFERENCES USERS(id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (bookID) REFERENCES BOOKS(id) ON DELETE CASCADE ON UPDATE CASCADE
        )
    """,
    """
    CREATE TABLE IF NOT EXISTS publishers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS follows (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        followerID INTEGER NOT NULL,
        followedID INTEGER NOT NULL,
        FOREIGN KEY (followerID) REFERENCES USERS(id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (followedID) REFERENCES USERS(id) ON DELETE CASCADE ON UPDATE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userID INTEGER NOT NULL,
        bookID INTEGER NOT NULL,
        request_date TIMESTAMP NOT NULL,
        source TEXT NOT NULL,
        FOREIGN KEY (userID) REFERENCES USERS(id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (bookID) REFERENCES BOOKS(id) ON DELETE CASCADE ON UPDATE CASCADE
    )
    """
]


def create_tables():
    with dbapi2.connect("testing.db") as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        connection.commit()
