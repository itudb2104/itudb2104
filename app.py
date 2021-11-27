from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from pages import pages

app = Flask(__name__)
app.register_blueprint(blueprint=pages, url_prefix='/')


if __name__ == '__main__':
    app.run(debug=True, port=8080)
