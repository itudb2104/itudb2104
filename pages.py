from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from classes import *
from database import Database
from passlib.hash import pbkdf2_sha256 as hasher
from functions import calculate_age, get_description_by_isbn, get_birthday_of_author, get_image_url_of_author, get_description_of_author
import random
from datetime import date


db = Database("testing.db")

pages = Blueprint('pages', __name__,
                  template_folder='templates',   static_folder='static')


# Homepage
@pages.route('/')
def index():
    if 'username' in session:
        user = db.get_user_by_username(session['username'])
        categories = db.get_random_15_categories()
        top_3_books = dict(
            zip(list(range(3)), random.sample(db.get_top_n_books(500), 3)))

        authors = [db.get_author_by_booktitle(
            title[1]) for title in top_3_books.values()]

        editor_suggestions = random.sample(
            db.get_random_books_by_year('2012', 20), 3)

        e_authors = [db.get_author_by_booktitle(
            b[1]) for b in editor_suggestions]
        session['source'] = "index"
        return render_template('index.html', user=user, categories=categories, top_3_books=top_3_books, authors=authors, e_authors=e_authors, editor_suggestions=editor_suggestions)
    return redirect(url_for('pages.login'))


# Profile Details Page
@pages.route('/profile/<username>')
def profile(username):
    if 'username' in session:
        me = db.get_user_by_username(session['username'])
        meid = me[0]
        if me[2] == username:
            is_following = 0
            age = calculate_age(me[6])
            follower_count = db.get_user_follower_count(meid)[0]
            followed_count = db.get_user_followed_count(meid)[0]
            evaluation_count = db.get_user_evaluation_count(meid)[0]
            library_count = db.get_user_library_count(meid)[0]
            return render_template('profile.html', user=me, age=age, follower_count=follower_count, followed_count=followed_count, evaluation_count=evaluation_count, library_count=library_count, profile=me, is_following=is_following)
        else:
            other = db.get_user_by_username(username)
            otherID = other[0]
            is_following = db.is_following(meid, otherID)
            if is_following:
                is_following = 1
            else:
                is_following = -1
            age = calculate_age(other[6])
            follower_count = db.get_user_follower_count(otherID)[0]
            followed_count = db.get_user_followed_count(otherID)[0]
            evaluation_count = db.get_user_evaluation_count(otherID)[0]
            library_count = db.get_user_library_count(otherID)[0]
            return render_template('profile.html', user=me, profile=other, age=age, follower_count=follower_count, followed_count=followed_count, evaluation_count=evaluation_count, library_count=library_count, is_following=is_following)
    return redirect(url_for('pages.login'))


# # Edit Profile Page
@ pages.route('/edit-profile/<username>', methods=['GET', 'POST'])
def edit_profile(username):
    if 'username' in session:
        user = db.get_user_by_username(session['username'])
        if request.method == 'POST':
            genders = ["other", "male", "female"]

            fullname = request.form['fullname']
            email = request.form['email']
            birthday = request.form['birthday']
            gender = genders.index(request.form['gender'])

            password = db.get_user_password(username)[0][0]

            meid = db.get_user_id(username)[0][0]

            update_user = User(meid, fullname, username,
                               password, email, gender, birthday)

            db.update_user(update_user)
            flash('Profile updated!')

            user = db.get_user_by_username(session['username'])

            return render_template('edit_profile.html', user=user)
        return render_template('edit_profile.html', user=user)
    return redirect(url_for('pages.login'))


@ pages.route('/follow/<username>')
def follow(username):
    if 'username' in session:
        me = db.get_user_by_username(session['username'])
        meid = me[0]
        other = db.get_user_by_username(username)
        otherID = other[0]
        db.follow_user(meid, otherID)

        age = calculate_age(other[6])
        follower_count = db.get_user_follower_count(otherID)[0]
        followed_count = db.get_user_followed_count(otherID)[0]
        evaluation_count = db.get_user_evaluation_count(otherID)[0]
        library_count = db.get_user_library_count(otherID)[0]

        return render_template('profile.html', profile=other, user=me, age=age, follower_count=follower_count, followed_count=followed_count, evaluation_count=evaluation_count, library_count=library_count, is_following=1)
    return redirect(url_for('pages.login'))


@ pages.route('/unfollow/<username>')
def unfollow(username):
    if 'username' in session:
        me = db.get_user_by_username(session['username'])
        meid = me[0]
        other = db.get_user_by_username(username)
        otherID = other[0]
        db.unfollow_user(meid, otherID)

        age = calculate_age(other[6])
        follower_count = db.get_user_follower_count(otherID)[0]
        followed_count = db.get_user_followed_count(otherID)[0]
        evaluation_count = db.get_user_evaluation_count(otherID)[0]
        library_count = db.get_user_library_count(otherID)[0]

        return render_template('profile.html', profile=other, user=me, age=age, follower_count=follower_count, followed_count=followed_count, evaluation_count=evaluation_count, library_count=library_count, is_following=-1)
    return redirect(url_for('pages.login'))


# User Followings
@ pages.route('/followings/<username>')
def followings(username):
    if 'username' in session:
        user = db.get_user_by_username(session['username'])
        profile = db.get_user_by_username(username)
        profile_id = profile[0]
        followings = db.get_user_followeds(profile_id)
        return render_template('followings.html', user=user, followings=followings)
    return redirect(url_for('pages.login'))


# User Followers
@ pages.route('/followers/<username>')
def followers(username):
    if 'username' in session:
        user = db.get_user_by_username(session['username'])
        profile = db.get_user_by_username(username)
        profile_id = profile[0]
        followers = db.get_user_followers(profile_id)
        return render_template('followers.html', user=user, followers=followers)
    return redirect(url_for('pages.login'))


# # Change Password Page
@ pages.route('/change-password/<username>', methods=['GET', 'POST'])
def change_password(username):
    if 'username' in session:
        user = db.get_user_by_username(session['username'])
        if request.method == "POST":
            old_password = request.form['old-password']
            new_password = request.form['new-password']

            if not 4 < len(new_password) < 12:
                flash("Password length must be 4 to 12 characters")
                return render_template('change_password.html', user=user)

            if hasher.verify(old_password, user[3]):
                if old_password == new_password:
                    flash("New password cannot be the same as old password")
                    return render_template('change_password.html', user=user)
                new_password = hasher.hash(new_password)
                db.update_user_password(username, new_password)
                flash('Your password has changed!')
                session.pop('username', None)
                return redirect(url_for('pages.login'))
            flash('Şifreler uyuşmuyor!')
            return redirect(url_for('pages.change_password', username=username))
        return render_template('change_password.html', user=user)
    return redirect(url_for('pages.login'))


# Search Page
@ pages.route('/search-results', methods=['GET', 'POST'])
def search_results():
    if 'username' in session:
        user = db.get_user_by_username(session['username'])
        if request.method == "POST":
            query = request.form['search-term']
            book_results, author_results, user_results = db.search(query)
            if len(book_results) > 5:
                book_results = random.sample(book_results, 5)
            if len(author_results) > 5:
                author_results = random.sample(author_results, 5)
            if len(user_results) > 5:
                user_results = random.sample(user_results, 5)
            session['source'] = "search"
            return render_template('search_results.html', user=user, book_results=book_results, author_results=author_results, user_results=user_results)
        user = db.get_user_by_username(session['username'])
        return redirect(url_for('pages.index'))
    return redirect(url_for('pages.index'))


# Requests page
@ pages.route('/donate-book')
def donate_book():
    if 'username' in session:
        user = db.get_user_by_username(session['username'])

        requests = db.get_requests()
        print(requests)

        books = [db.get_book_by_id(r[2]) for r in requests]

        length = len(books)
        return render_template('donate_book.html', user=user, books=books, length=length)
    return redirect(url_for('pages.login'))


# Author Page
@ pages.route('/author/<author_id>')
def author(author_id):
    if 'username' in session:
        user = db.get_user_by_username(session['username'])
        aid = int(author_id)
        author = db.get_author_by_id(aid)
        # author_books = db.get_author_books(author_id)

        session['source'] = "author"
        return render_template('author.html', user=user, author=author)
    return render_template('author.html', author=author)


# Add Book
@ pages.route('/add-book', methods=['GET', 'POST'])
def add_book():
    if 'username' in session:
        if session['username'] == "admin":
            user = db.get_user_by_username(session['username'])

            if request.method == 'POST':
                title = request.form['title']
                author = request.form['author']
                category = request.form['category']
                publication_year = request.form['publication-year']
                isbn13 = request.form['isbn13']

                # Check if book already exists by ISBN13
                search_book = db.get_book_by_isbn(isbn13)
                if search_book:
                    flash('Book already exists!')
                    return render_template('add_book.html', user=user)

                numpages = request.form['numpages']
                publisher = request.form['publisher']
                image_url = request.form['image-url']

                # check if category exists
                # if not, add category
                category_id = db.get_category_id(category)
                if not category_id:
                    new_category = Category(None, category)
                    db.insert_category(new_category)
                category_id = db.get_category_id(category)[0]

                # check if author exists
                # if not, add author
                author_id = db.get_author_id(author)
                if not author_id:
                    description = get_description_of_author(authorName=author)
                    birthday = get_birthday_of_author(authorName=author)
                    image_url = get_image_url_of_author(authorName=author)
                    new_author = Author(
                        None, author, birthday, description, image_url)
                    db.insert_author(new_author)
                author_id = db.get_author_id(author)[0]

                # check if publisher exists
                # if not, add publisher
                publisher_id = db.get_publisher_id(publisher)
                if not publisher_id:
                    new_publisher = Publisher(None, publisher)
                    db.insert_publisher(new_publisher)
                publisher_id = db.get_publisher_id(publisher)[0]

                # Create book object
                new_book = Book(None, title, 0, numpages, 0, publication_year, author_id,
                                isbn13, publisher_id, image_url, category_id)

                # Add book to database
                db.insert_book(new_book)

                flash('Book added!')
                return redirect(url_for('pages.add_book'))

            return render_template('add_book.html', user=user)
        return redirect(url_for('pages.index'))
    return redirect(url_for('pages.index'))


# Book Details Page
@ pages.route('/book/<isbn>')
def book(isbn):
    book = db.get_book_by_isbn(isbn)
    description = get_description_by_isbn(isbn)
    if 'username' in session:
        user = db.get_user_by_username(session['username'])
        rating = round(book[2])
        author = db.get_author_by_id(book[6])[1]
        category = db.get_category_by_id(book[10])[1]
        publisher = db.get_publisher_by_id(book[8])[1]
        is_in_user_library = db.is_in_user_library(user[0], book[0])
        is_in_user_requests = db.is_in_user_requests(user[0], book[0])
        is_evaluated = db.is_evaluated(user[0], book[0])
        session['source'] = "book"
        book_suggestions_4 = random.sample(
            db.suggest_n_book_by_book_isbn(isbn, 10), 4)
        authors_suggestions = [db.get_author_by_booktitle(
            b[1]) for b in book_suggestions_4]

        evaluations = db.get_all_evaluations_by_book_id(book[0])
        return render_template('book.html', user=user, book=book, evaluations=evaluations, description=description, author=author, category=category, rating=rating, publisher=publisher, is_in_user_library=is_in_user_library, is_in_user_requests=is_in_user_requests, is_evaluated=is_evaluated, book_suggestions_4=book_suggestions_4, authors_suggestions=authors_suggestions)
    return redirect(url_for('pages.index'))


# Add to Library
@ pages.route("/add-to-library/<int:user_id>/<int:book_id>")
def add_to_library(user_id, book_id):
    if 'username' in session:
        user = db.get_user_by_username(session['username'])
        if user[0] == user_id:
            book = db.get_book_by_id(book_id)
            description = get_description_by_isbn(book[7])
            rating = int(book[2])
            author = db.get_author_by_id(book[6])[1]
            category = db.get_category_by_id(book[10])[1]
            publisher = db.get_publisher_by_id(book[8])[1]
            source = session['source']
            is_in_user_requests = db.is_in_user_requests(user[0], book[0])
            is_evaluated = db.is_evaluated(user[0], book[0])
            new_library = Library(None, user_id, book_id, source)
            db.insert_library(new_library)
            book_suggestions_4 = random.sample(
                db.suggest_n_book_by_book_isbn(book[7], 10), 4)
        authors_suggestions = [db.get_author_by_booktitle(
            b[1]) for b in book_suggestions_4]
        evaluations = db.get_all_evaluations_by_book_id(book[0])
        return render_template('book.html', book=book, evaluations=evaluations, publisher=publisher, rating=rating, author=author, category=category, description=description, user=user, book_suggestions_4=book_suggestions_4, authors_suggestions=authors_suggestions, is_in_user_library=True, is_in_user_requests=is_in_user_requests, is_evaluated=is_evaluated)
    return redirect(url_for('pages.index'))


# Remove from Library
@ pages.route("/remove-from-library/<int:user_id>/<int:book_id>")
def remove_from_library(user_id, book_id):
    if 'username' in session:
        user = db.get_user_by_username(session['username'])
        if user[0] == user_id:
            book = db.get_book_by_id(book_id)
            description = get_description_by_isbn(book[7])
            rating = int(book[2])
            author = db.get_author_by_id(book[6])[1]
            category = db.get_category_by_id(book[10])[1]
            publisher = db.get_publisher_by_id(book[8])[1]
            is_in_user_requests = db.is_in_user_requests(user[0], book[0])
            is_evaluated = db.is_evaluated(user[0], book[0])
            db.delete_library(user_id, book_id)
            book_suggestions_4 = random.sample(
                db.suggest_n_book_by_book_isbn(book[7], 10), 4)
        authors_suggestions = [db.get_author_by_booktitle(
            b[1]) for b in book_suggestions_4]
        evaluations = db.get_all_evaluations_by_book_id(book[0])
        return render_template('book.html', book=book, evaluations=evaluations, publisher=publisher, rating=rating, author=author, category=category, description=description, user=user, book_suggestions_4=book_suggestions_4, authors_suggestions=authors_suggestions, is_in_user_library=False, is_in_user_requests=is_in_user_requests, is_evaluated=is_evaluated)
    return redirect(url_for('pages.index'))


# Request Book
@ pages.route('/add-to-requests/<int:user_id>/<int:book_id>')
def add_to_requests(user_id, book_id):
    if 'username' in session:
        user = db.get_user_by_username(session['username'])
        if user[0] == user_id:
            book = db.get_book_by_id(book_id)
            description = get_description_by_isbn(book[7])
            rating = int(book[2])
            author = db.get_author_by_id(book[6])[1]
            category = db.get_category_by_id(book[10])[1]
            publisher = db.get_publisher_by_id(book[8])[1]
            source = session['source']
            is_in_user_library = db.is_in_user_library(user[0], book[0])
            is_evaluated = db.is_evaluated(user[0], book[0])
            new_request = Request(None, user_id, book_id, source)
            db.insert_request(new_request)
            book_suggestions_4 = random.sample(
                db.suggest_n_book_by_book_isbn(book[7], 10), 4)
        authors_suggestions = [db.get_author_by_booktitle(
            b[1]) for b in book_suggestions_4]
        evaluations = db.get_all_evaluations_by_book_id(book[0])
        return render_template('book.html', book=book, evaluations=evaluations, publisher=publisher, rating=rating, author=author, category=category, description=description, user=user, book_suggestions_4=book_suggestions_4, authors_suggestions=authors_suggestions, is_in_user_requests=True, is_in_user_library=is_in_user_library, is_evaluated=is_evaluated)
    return redirect(url_for('pages.index'))


# Request Book
@ pages.route('/remove-from-requests/<int:user_id>/<int:book_id>')
def remove_from_requests(user_id, book_id):
    if 'username' in session:
        user = db.get_user_by_username(session['username'])
        if user[0] == user_id:
            book = db.get_book_by_id(book_id)
            description = get_description_by_isbn(book[7])
            rating = int(book[2])
            author = db.get_author_by_id(book[6])[1]
            category = db.get_category_by_id(book[10])[1]
            publisher = db.get_publisher_by_id(book[8])[1]
            source = session['source']
            is_in_user_library = db.is_in_user_library(user[0], book[0])
            is_evaluated = db.is_evaluated(user[0], book[0])
            db.delete_request(user_id, book_id)
            book_suggestions_4 = random.sample(
                db.suggest_n_book_by_book_isbn(book[7], 10), 4)
        authors_suggestions = [db.get_author_by_booktitle(
            b[1]) for b in book_suggestions_4]
        evaluations = db.get_all_evaluations_by_book_id(book[0])
        return render_template('book.html', book=book, evaluations=evaluations, publisher=publisher, rating=rating, author=author, category=category, description=description, user=user, is_in_user_requests=False, is_in_user_library=is_in_user_library, book_suggestions_4=book_suggestions_4, authors_suggestions=authors_suggestions, is_evaluated=is_evaluated)
    return redirect(url_for('pages.index'))


# Evaluate Book
@ pages.route('/evaluate-book/<int:user_id>/<int:book_id>', methods=['GET', 'POST'])
def evaluate_book(user_id, book_id):
    if 'username' in session:
        user = db.get_user_by_username(session['username'])
        book = db.get_book_by_id(book_id)
        is_evaluated = db.is_evaluated(user[0], book[0])
        if is_evaluated:
            return redirect(url_for('pages.index'))
        description = get_description_by_isbn(str(book[7]))
        author = db.get_author_by_id(book[6])[1]
        category = db.get_category_by_id(book[10])[1]
        publisher = db.get_publisher_by_id(book[8])[1]
        average_rating = book[2]
        ratings_count = book[4]
        is_in_user_library = db.is_in_user_library(user[0], book[0])
        is_in_user_requests = db.is_in_user_requests(user[0], book[0])
        if user[0] == user_id:
            if request.method == 'POST':
                text = request.form['text']
                vote = request.form['vote']
                new_ratings_count = ratings_count + 1
                new_average_rating = (
                    average_rating * ratings_count + int(average_rating)) / new_ratings_count
                new_evaluation = Evaluation(None, book_id, user_id, text, vote)
                new_book = Book(
                    book_id, book[1], new_average_rating, book[3], new_ratings_count, book[5], book[6], book[7], book[8], book[9], book[10])
                db.insert_evaluation(new_evaluation)
                db.update_book(new_book)
                book_suggestions_4 = random.sample(
                    db.suggest_n_book_by_book_isbn(book[7], 10), 4)
                authors_suggestions = [db.get_author_by_booktitle(
                    b[1]) for b in book_suggestions_4]
                evaluations = db.get_all_evaluations_by_book_id(book[0])
                return render_template('book.html', book=book, evaluations=evaluations, book_suggestions_4=book_suggestions_4, authors_suggestions=authors_suggestions, description=description, author=author, category=category, publisher=publisher, rating=round(average_rating), user=user, is_in_user_library=is_in_user_library, is_in_user_requests=is_in_user_requests, is_evaluated=True)
            return render_template('evaluate-book.html', user=user, book=book, author=author, category=category, publisher=publisher)
    return redirect(url_for('pages.index'))


# User Evaluations
@ pages.route('/evaluations/<username>')
def user_evaluations(username):
    if 'username' in session:
        user = db.get_user_by_username(session['username'])
        evaluations = db.get_all_evaluations_by_user_id(user_id=user[0])
        books = [db.get_book_by_id(e[1]) for e in evaluations]
        return render_template('evaluations.html', evaluations=evaluations, user=user, books=books, length=len(evaluations))
    return redirect(url_for('pages.index'))


# User Library
@ pages.route('/library/<username>')
def user_library(username):
    if 'username' in session:
        user = db.get_user_by_username(session['username'])
        library = db.get_all_library_by_user_id(user_id=user[0])
        books = [db.get_book_by_id(e[2]) for e in library]
        categories = [db.get_category_by_id(b[10])[1] for b in books]
        authors = [db.get_author_by_id(b[6])[1] for b in books]
        return render_template('library.html', library=library, user=user, books=books, categories=categories, authors=authors, length=len(library))
    return redirect(url_for('pages.index'))


# Category page
@ pages.route('/category/<int:category_id>')
def category(category_id):
    if 'username' in session:
        user = db.get_user_by_username(session['username'])
        books = db.get_random_books_by_category_id(category_id, 10)
        category = db.get_category_by_id(category_id)[1]
        length = len(books)
        authors = [db.get_author_by_id(b[6])[1] for b in books]
        return render_template('category.html', user=user, category=category, books=books, authors=authors, length=length)
    return redirect(url_for('pages.index'))


# Login Page
@ pages.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('pages.index'))
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        search_user = db.get_user_password(username)

        if len(search_user) == 0:
            flash("User not found")
            return redirect(url_for('pages.login'))

        if hasher.verify(password, search_user[0][0]):
            session['username'] = username
            return redirect(url_for('pages.profile', username=username))
        else:
            flash("Password incorrect")
            return redirect(url_for('pages.login'))
    return render_template('login.html')


# Register Page
@ pages.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('pages.profile', username=session['username']))
    if request.method == 'POST':
        genders = ["other", "male", "female"]

        fullname = request.form['fullname']
        email = request.form['email']
        birthday = request.form['birthday']
        if "gender" in request.form:
            gender = genders.index(request.form['gender'])
        else:
            flash("Please show your gender")
            return redirect(url_for('pages.register'))
        username = request.form['username']
        password = request.form['password']

        if not 4 < len(password) < 12:
            flash("Password length must be 4 to 12 characters")
            return redirect(url_for('pages.register'))

        search_username = db.get_user_id(username)
        if len(search_username) > 0:
            flash("Username already exists")
            return redirect(url_for('pages.register'))

        hashed_password = hasher.hash(password)

        new_user = User(None, fullname, username,
                        hashed_password, email, gender, birthday)

        db.insert_user(new_user)
        return redirect(url_for('pages.login'))
    return render_template('register.html')


# Logout Page
@ pages.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('pages.login'))


# Error 404 Page
@ pages.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')
