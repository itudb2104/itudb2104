
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
