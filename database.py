from classes import *
import sqlite3 as dbapi2


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = dbapi2.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

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
