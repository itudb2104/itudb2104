from classes import *
import sqlite3 as dbapi2
from datetime import datetime


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = dbapi2.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    # Books

    def insert_book(self, book):
        self.cursor.execute("INSERT INTO books VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (book.title, book.average_rating, book.num_pages, book.ratings_count, book.publication_year, book.authorID,  book.isbn, book.publisherID, book.image_url, book.categoryID))
        self.conn.commit()

    def update_book(self, book):
        self.cursor.execute("UPDATE books SET title=?, average_rating=?, num_pages=?, ratings_count=?, publication_year=?, authorID=?, isbn=?, publisherID=?, image_url=?, categoryID=? WHERE id=?",
                            (book.title, book.average_rating, book.num_pages, book.ratings_count, book.publication_year, book.authorID, book.isbn, book.publisherID, book.image_url, book.categoryID, book.id))
        self.conn.commit()

    def delete_book(self, id):
        self.cursor.execute("DELETE FROM books WHERE id=?", (id,))
        self.conn.commit()

    def get_all_books_by_author(self, author):
        self.cursor.execute(
            "SELECT * FROM books WHERE LIKE '%' || ? || '%'", (author,))
        return self.cursor.fetchall()

    def get_all_books_by_title(self, title):
        self.cursor.execute(
            "SELECT * FROM books WHERE title LIKE '%' || ? || '%'", (title,))
        return self.cursor.fetchall()

    def get_top_n_books(self, n):
        self.cursor.execute(
            "SELECT * FROM books ORDER BY average_rating DESC LIMIT ?", (n,))
        return self.cursor.fetchall()

    def get_top_n_books_by_category(self, category, n):
        self.cursor.execute(
            "SELECT * FROM books WHERE category=? ORDER BY average_rating DESC LIMIT ?", (category, n))
        return self.cursor.fetchall()

    def get_n_latest_books(self, n):
        self.cursor.execute(
            "SELECT * FROM books ORDER BY publication_year DESC LIMIT ?", (n,))
        return self.cursor.fetchall()

    def get_book_evaluations(self, bookID):
        self.cursor.execute(
            "SELECT * FROM evaluations WHERE bookID=?", (bookID,))
        return self.cursor.fetchall()

    def get_book_by_isbn(self, isbn):
        self.cursor.execute(
            "SELECT * FROM books WHERE isbn=?", (isbn,))
        return self.cursor.fetchone()

    def get_book_by_id(self, id):
        self.cursor.execute("SELECT * FROM books WHERE id=?", (id,))
        return self.cursor.fetchone()

    # Authors

    def insert_author(self, author):
        self.cursor.execute("INSERT INTO authors VALUES(NULL, ?, ?,?,?)",
                            (author.name, author.birthday, author.biography, author.image_url))
        self.conn.commit()

    def update_author(self, author):
        self.cursor.execute("UPDATE authors SET name=?, birthday=?, biography=?, image_url=? WHERE id=?",
                            (author.name, author.birthday, author.biography, author.image_url, author.id))
        self.conn.commit()

    def delete_author(self, id):
        self.cursor.execute("DELETE FROM authors WHERE id=?", (id,))
        self.conn.commit()

    def get_all_authors_by_name(self, name):
        self.cursor.execute(
            "SELECT * FROM authors WHERE name LIKE '%' || ? || '%'", (name,))
        return self.cursor.fetchall()

    def get_author_id(self, name):
        self.cursor.execute(
            "SELECT id FROM authors WHERE name=?", (name,))
        return self.cursor.fetchone()

    def get_author_by_booktitle(self, title):
        self.cursor.execute(
            "SELECT authorID FROM books WHERE title=?", (title,))
        author_id = self.cursor.fetchone()[0]
        self.cursor.execute(
            "SELECT name FROM authors WHERE id=?", (author_id,))
        author_name = self.cursor.fetchone()[0]
        return author_name

    def get_author_by_id(self, id):
        self.cursor.execute("SELECT * FROM authors WHERE id=?", (id,))
        return self.cursor.fetchone()

    def get_random_books_by_author_id(self, author_id, n):
        self.cursor.execute(
            "SELECT * FROM books WHERE authorID=? ORDER BY RANDOM() LIMIT ?", (author_id, n))
        return self.cursor.fetchall()

    # Categories

    def insert_category(self, category):
        self.cursor.execute("INSERT INTO categories VALUES (NULL, ?)",
                            (category.name,))
        self.conn.commit()

    def update_category(self, category):
        self.cursor.execute("UPDATE categories SET name=? WHERE id=?",
                            (category.name, category.id))
        self.conn.commit()

    def delete_category(self, id):
        self.cursor.execute("DELETE FROM categories WHERE id=?", (id,))
        self.conn.commit()

    def get_category_id(self, name):
        self.cursor.execute(
            "SELECT id FROM categories WHERE name=?", (name,))
        return self.cursor.fetchone()

    def get_category_by_id(self, id):
        self.cursor.execute("SELECT * FROM categories WHERE id=?", (id,))
        return self.cursor.fetchone()

    def get_random_books_by_category_id(self, category_id, n):
        self.cursor.execute(
            "SELECT * FROM books WHERE categoryID=? ORDER BY RANDOM() LIMIT ?", (category_id, n))
        return self.cursor.fetchall()

    def get_random_15_categories(self):
        self.cursor.execute(
            "SELECT * FROM categories ORDER BY RANDOM() LIMIT 15")
        return self.cursor.fetchall()

    # Users

    def insert_user(self, user):
        self.cursor.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?, ?, ?)",
                            (user.fullname, user.username, user.password, user.email, user.gender, user.birthday))
        self.conn.commit()

    def update_user(self, user):
        self.cursor.execute("UPDATE users SET fullname=?, username=?, email=?, birthday=?, password=?, gender=? WHERE id=?",
                            (user.fullname, user.username, user.email, user.birthday, user.password, user.gender, user.id))
        self.conn.commit()

    def delete_user(self, id):
        self.cursor.execute("DELETE FROM users WHERE id=?", (id,))
        self.conn.commit()

    def get_all_users_by_name(self, name):
        self.cursor.execute(
            "SELECT * FROM users WHERE name LIKE '%' || ? || '%'", (name,))
        return self.cursor.fetchall()

    def get_user_by_username(self, username):
        self.cursor.execute(
            "SELECT * FROM users WHERE username=?", (username,))
        return self.cursor.fetchone()

    def get_user_password(self, username):
        self.cursor.execute(
            "SELECT password FROM users WHERE username=?", (username,))
        return self.cursor.fetchall()

    def update_user_password(self, username, password):
        self.cursor.execute(
            "UPDATE users SET password=? WHERE username=?", (password, username))
        self.conn.commit()

    def get_user_birthday(self, username):
        self.cursor.execute(
            "SELECT birthday FROM users WHERE username=?", (username,))
        return self.cursor.fetchone()

    def get_user_id(self, username):
        self.cursor.execute(
            "SELECT id FROM users WHERE username=?", (username,))
        return self.cursor.fetchall()

    def get_user_evaluations(self, userID):
        self.cursor.execute(
            "SELECT * FROM evaluations WHERE userID=?", (userID,))
        return self.cursor.fetchall()

    def follow_user(self, userID, followerID):
        self.cursor.execute(
            "INSERT INTO follows VALUES (NULL,?, ?)", (userID, followerID))
        self.conn.commit()

    def unfollow_user(self, userID, followerID):
        self.cursor.execute(
            "DELETE FROM follows WHERE followerID=? AND followedID=?", (userID, followerID))
        self.conn.commit()

    def is_following(self, userID, followerID):
        self.cursor.execute(
            "SELECT * FROM follows WHERE followerID=? AND followedID=?", (userID, followerID))
        return self.cursor.fetchone()

    def get_user_by_id(self, id):
        self.cursor.execute("SELECT * FROM users WHERE id=?", (id,))
        return self.cursor.fetchone()

    # Evaluations

    def insert_evaluation(self, evaluation):
        self.cursor.execute(
            "INSERT INTO evaluations VALUES(NULL,?,?,?,?)", (
                evaluation.bookID, evaluation.userID, evaluation.text, evaluation.vote)
        )
        self.conn.commit()

    def update_evaluation(self, evaluation):
        self.cursor.execute(
            "UPDATE evaluations SET userID=?, bookID=?, text=?, vote=? WHERE id=?", (evaluation.bookID, evaluation.userID, evaluation.text, evaluation.vote, evaluation.id))
        self.conn.commit()

    def delete_evaluation(self, id):
        self.cursor.execute("DELETE FROM evaluations WHERE id=?", (id,))
        self.conn.commit()

    def get_all_evaluations_by_book_id(self, book_id):
        self.cursor.execute(
            "SELECT * FROM evaluations WHERE bookID=?", (book_id,))
        return self.cursor.fetchall()

    def get_all_evaluations_by_user_id(self, user_id):
        self.cursor.execute(
            "SELECT * FROM evaluations WHERE userID=?", (user_id,))
        return self.cursor.fetchall()

    def get_user_evaluation_count(self, user_id):
        self.cursor.execute(
            "SELECT COUNT(*) FROM evaluations WHERE userID=?", (user_id,))
        return self.cursor.fetchone()

    def is_evaluated(self, userID, bookID):
        self.cursor.execute(
            "SELECT * FROM evaluations WHERE userID=? AND bookID=?", (userID, bookID))
        return self.cursor.fetchone()

    # Libraries

    def insert_library(self, library):
        self.cursor.execute(
            "INSERT INTO libraries VALUES(NULL,?,?,?,?)", (library.userID, library.bookID, library.adding_date, library.source))
        self.conn.commit()

    def update_library(self, library):
        self.cursor.execute(
            "UPDATE libraries SET userID=?, bookID=? WHERE id=?", (library.user_id, library.book_id, library.id))
        self.conn.commit()

    def delete_library(self, user_id, book_id):
        self.cursor.execute(
            "DELETE FROM libraries WHERE userID=? AND bookID=?", (user_id, book_id))
        self.conn.commit()

    def get_library_by_user_id(self, user_id):
        self.cursor.execute(
            "SELECT * FROM libraries WHERE userID=?", (user_id,))
        return self.cursor.fetchall()

    def is_in_user_library(self, user_id, book_id):
        self.cursor.execute(
            "SELECT * FROM libraries WHERE userID=? AND bookID=?", (user_id, book_id))
        return self.cursor.fetchone()

    def get_user_library_count(self, user_id):
        self.cursor.execute(
            "SELECT COUNT(*) FROM libraries WHERE userID=?", (user_id,))
        return self.cursor.fetchone()

    def get_all_library_by_user_id(self, user_id):
        self.cursor.execute(
            "SELECT * FROM libraries WHERE userID=?", (user_id,))
        return self.cursor.fetchall()

    # Publishers

    def insert_publisher(self, publisher):
        self.cursor.execute(
            "INSERT INTO publishers VALUES(NULL,?)", (publisher.name,))
        self.conn.commit()

    def update_publisher(self, publisher):
        self.cursor.execute(
            "UPDATE publishers SET name=? WHERE id=?", (publisher.name, publisher.id))
        self.conn.commit()

    def delete_publisher(self, id):
        self.cursor.execute("DELETE FROM publishers WHERE id=?", (id,))
        self.conn.commit()

    def get_all_publishers_by_name(self, name):
        self.cursor.execute(
            "SELECT * FROM publishers WHERE name LIKE '%' || ? || '%'", (name,))
        return self.cursor.fetchall()

    def get_all_books_by_publisher_id(self, publisher_id):
        self.cursor.execute(
            "SELECT * FROM books WHERE publisher_id=?", (publisher_id,))
        return self.cursor.fetchall()

    def get_publisher_by_id(self, id):
        self.cursor.execute(
            "SELECT * FROM publishers WHERE id=?", (id,))
        return self.cursor.fetchone()

    def get_publisher_id(self, name):
        self.cursor.execute(
            "SELECT id FROM publishers WHERE name=?", (name,))
        return self.cursor.fetchone()

    # Follows

    def get_user_followers(self, user_id):
        self.cursor.execute(
            "SELECT * FROM follows WHERE followedID=?", (user_id,))
        follower_ids = self.cursor.fetchall()
        followers = [self.get_user_by_id(follower_id[1])
                     for follower_id in follower_ids]
        return followers

    def get_user_followeds(self, user_id):
        self.cursor.execute(
            "SELECT * FROM follows WHERE followerID=?", (user_id,))
        followed_ids = self.cursor.fetchall()
        followeds = [self.get_user_by_id(followed_id[2])
                     for followed_id in followed_ids]
        return followeds

    def get_user_follower_count(self, user_id):
        self.cursor.execute(
            "SELECT COUNT(*) FROM follows WHERE followedID=?", (user_id,))
        return self.cursor.fetchone()

    def get_user_followed_count(self, user_id):
        self.cursor.execute(
            "SELECT COUNT(*) FROM follows WHERE followerID=?", (user_id,))
        return self.cursor.fetchone()

    # Search

    def search(self, query):
        self.cursor.execute(
            "SELECT * FROM books WHERE title LIKE '%' || ? || '%'", (query,))
        book_results = self.cursor.fetchall()
        self.cursor.execute(
            "SELECT * FROM authors WHERE name LIKE '%' || ? || '%'", (query,))
        author_results = self.cursor.fetchall()
        self.cursor.execute(
            "SELECT * FROM users WHERE username LIKE '%' || ? || '%'", (query,))
        user_results = self.cursor.fetchall()
        return book_results, author_results, user_results

    # Reqeusts

    def insert_request(self, request):
        self.cursor.execute(
            "INSERT INTO requests VALUES(NULL,?,?,?,?)", (request.userID, request.bookID, request.requestDate, request.source))
        self.conn.commit()

    def delete_request(self, user_id, book_id):
        self.cursor.execute(
            "DELETE FROM requests WHERE userID=? AND bookID=?", (user_id, book_id))
        self.conn.commit()

    def is_in_user_requests(self, user_id, book_id):
        self.cursor.execute(
            "SELECT * FROM requests WHERE userID=? AND bookID=?", (user_id, book_id))
        return self.cursor.fetchone()

    def get_requests(self):
        self.cursor.execute(
            "SELECT * FROM requests")
        return self.cursor.fetchall()

    def get_book_by_request_id(self, id):
        self.cursor.execute(
            "SELECT * FROM requests WHERE id=?", (id,))
        return self.cursor.fetchone()

    # Suggestions
    def get_random_greater_than_4(self, n):
        self.cursor.execute(
            "SELECT * FROM books WHERE average_rating > 4 ORDER BY RANDOM() LIMIT ?", (n,))
        return self.cursor.fetchall()

    def suggest_n_book_by_book_isbn(self, isbn, n):
        self.cursor.execute(
            "SELECT * FROM books WHERE isbn=?", (isbn,))
        book = self.cursor.fetchone()
        category = self.get_category_by_id(book[10])
        author = self.get_author_by_id(book[6])

        random_category_books = self.get_random_books_by_category_id(
            category[0], n)
        random_author_books = self.get_random_books_by_author_id(author[0], n)

        suggestions = random_category_books + random_author_books

        if len(suggestions) > 2:
            n = len(suggestions) * 2
        else:
            n = 8
        random_greater_than_4 = self.get_random_greater_than_4(n)
        suggestions += random_greater_than_4

        suggestions = list(filter(lambda b: b[0] != book[0], suggestions))

        return suggestions

    def get_random_books_by_year(self, year, n):
        self.cursor.execute(
            "SELECT * FROM books WHERE publication_year=? ORDER BY RANDOM() LIMIT ?", (year, n))
        return self.cursor.fetchall()
