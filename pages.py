from flask import Blueprint, render_template, request, redirect, url_for, flash

pages = Blueprint('pages', __name__,
                  template_folder='templates',   static_folder='static')


# Homepage
@pages.route('/')
def index():
    return render_template('index.html')


# Profile Details Page
@pages.route('/<username>')
def profile(username):
    return render_template('profile.html')


# # Edit Profile Page
@pages.route('/<username>/edit')
def edit_profile(username):
    return render_template('edit_profile.html')


# # Change Password Page
@pages.route('/<username>/change_password')
def change_password(username):
    return render_template('change_password.html')


# Search Page
@pages.route('/search_results')
def search_results():
    return render_template('search_results.html')


# Add Book
@pages.route('/add_book')
def add_book():
    return render_template('add_book.html')


# Book Details Page
@pages.route('/<bookname>')
def book(bookname):
    return render_template('book.html')


# Random Book Page
@pages.route('/random_book')
def random_book():
    return render_template('book.html')


# Login Page
@pages.route('/login')
def login():
    return render_template('login.html')


# Register Page
@pages.route('/register')
def register():
    return render_template('register.html')


# Logout Page
@pages.route('/logout')
def logout():
    return redirect(url_for('pages.index'))


# Error 404 Page
# @pages.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html')
