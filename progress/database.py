from classes import *
import sqlite3 as dbapi2


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = dbapi2.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    # Books

    def insert_book(self, book):
        self.cursor.execute("INSERT INTO books VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (book.title, book.average_rating, book.num_pages, book.ratings_count, book.publication_year, book.authorID,  book.isbn, book.publisherID, book.image_url, book.category))
        self.conn.commit()

    def update_book(self, book):
        self.cursor.execute("UPDATE books SET title=?, average_rating=?, num_pages=?, ratings_count=?, publication_year=?, author=?, year=?, isbn=?, publisher=?, image_url=? category=? WHERE id=?",
                            (book.title, book.average_rating, book.num_pages, book.ratings_count, book.publication_year, book.author, book.year, book.isbn, book.publisher, book.image_url, book.category, book.id))
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

    # Authors

    def insert_author(self, author):
        self.cursor.execute("INSERT INTO authors VALUES (?)",
                            (author.name))
        self.conn.commit()

    def update_author(self, author):
        self.cursor.execute("UPDATE authors SET name=? WHERE id=?",
                            (author.name, author.id))
        self.conn.commit()

    def delete_author(self, id):
        self.cursor.execute("DELETE FROM authors WHERE id=?", (id,))
        self.conn.commit()

    def get_all_authors_by_name(self, name):
        self.cursor.execute(
            "SELECT * FROM authors WHERE name LIKE '%' || ? || '%'", (name,))
        return self.cursor.fetchall()

    # Categories

    def insert_category(self, category):
        self.cursor.execute("INSERT INTO categories VALUES ( ?)",
                            (category.name,))
        self.conn.commit()

    def update_category(self, category):
        self.cursor.execute("UPDATE categories SET name=? WHERE id=?",
                            (category.name, category.id))
        self.conn.commit()

    def delete_category(self, id):
        self.cursor.execute("DELETE FROM categories WHERE id=?", (id,))
        self.conn.commit()

    # Users

    def insert_user(self, user):
        self.cursor.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?, ?, ?)",
                            (user.fullname, user.username, user.password, user.email, user.gender, user.birthday))
        self.conn.commit()

    def update_user(self, user):
        self.cursor.execute("UPDATE users SET name=?, username=? email=?, birthday=?, password=?, gender=? WHERE id=?",
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
            "INSERT INTO follows VALUES (?, ?)", (userID, followerID))
        self.conn.commit()

    def unfollow_user(self, userID, followerID):
        self.cursor.execute(
            "DELETE FROM follows WHERE userID=? AND followerID=?", (userID, followerID))
        self.conn.commit()

    # Evaluations

    def insert_evaluation(self, evaluation):
        self.cursor.execute(
            "INSERT INTO evaluations VALUES(?,?,?,?)", (
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

    # Libraries

    def insert_library(self, library):
        self.cursor.execute(
            "INSERT INTO libraries VALUES(?,?)", (library.userID, library.bookID))
        self.conn.commit()

    def update_library(self, library):
        self.cursor.execute(
            "UPDATE libraries SET userID=?, bookID=? WHERE id=?", (library.user_id, library.book_id, library.id))
        self.conn.commit()

    def delete_library(self, id):
        self.cursor.execute("DELETE FROM libraries WHERE id=?", (id,))
        self.conn.commit()

    def get_library_by_user_id(self, user_id):
        self.cursor.execute(
            "SELECT * FROM libraries WHERE userID=?", (user_id,))
        return self.cursor.fetchall()

    # Publishers

    def insert_publisher(self, publisher):
        self.cursor.execute(
            "INSERT INTO publishers VALUES(?)", (publisher.name))
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

    # Follows

    def get_user_followers(self, user_id):
        self.cursor.execute(
            "SELECT * FROM follows WHERE followerID=?", (user_id,))
        return self.cursor.fetchall()

    def get_user_followeds(self, user_id):
        self.cursor.execute(
            "SELECT * FROM follows WHERE followedID=?", (user_id,))
        return self.cursor.fetchall()

    def get_user_follower_count(self, user_id):
        self.cursor.execute(
            "SELECT COUNT(*) FROM follows WHERE followerID=?", (user_id,))
        return self.cursor.fetchone()

    def get_user_followed_count(self, user_id):
        self.cursor.execute(
            "SELECT COUNT(*) FROM follows WHERE followedID=?", (user_id,))
        return self.cursor.fetchone()
