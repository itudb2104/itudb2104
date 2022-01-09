from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from pages import pages
import db_init

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'

app.register_blueprint(blueprint=pages, url_prefix='/')

if __name__ == '__main__':
    db_init.create_tables()
    app.run(debug=True, port=8080)
