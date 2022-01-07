
INIT_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        email TEXT NOT NULL,
        gender INTEGER NOT NULL,
        birthday TIMESTAMP NOT NULL
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
        FOREIGN KEY (userID) REFERENCES USERS(id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (bookID) REFERENCES BOOKS(id) ON DELETE CASCADE ON UPDATE CASCADE
        )
    """,
    """
    CREATE TABLE IF NOT EXISTS users_evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userID INTEGER NOT NULL,
        evaluationID INTEGER NOT NULL,
        FOREIGN KEY (userID) REFERENCES USERS(id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (evaluationID) REFERENCES EVALUATIONS(id) ON DELETE CASCADE ON UPDATE CASCADE
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
    """
]


def create_tables():
    with dbapi2.connect("testing.db") as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        connection.commit()
