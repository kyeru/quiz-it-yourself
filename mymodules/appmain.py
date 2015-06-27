from flask import Flask, url_for, redirect, request
from flask import render_template, session
import cgi
from os import urandom

from mymodules.counter import *
# from mymodules.fileparser import *
from mymodules.quiz import *
from mymodules.worddef import *

app = Flask(__name__)
app.Debug = True
app.secret_key = urandom(24)

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

class AppException(Exception):
    def __init__(self, msg):
        self.message = msg
    
    def __str__(self):
        return 'main: ' + self.message

# counter reset
@app.route('/init/')
def initiate():
    initiate_counter('QuizSeqNum')
    return 'Initiated.'

# empty page (default)
@app.route('/')
def default_page():
    return render_template('base.html',
                           style_url = style_url())

# data feeding by file
@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return quiz_file_upload()
    else:
        return quiz_file_upload_result()

# login
@app.route('/login/', methods=['GET', 'POST'])
def login():
    return 'login'

# quiz
@app.route('/quiz/', methods=['GET', 'POST'])
@app.route('/quiz/<user>/', methods=['GET', 'POST'])
def quiz_and_result(user = None):
    if request.method == 'GET':
        return quiz_input(user)
    else:
        return quiz_result(user)

# error handler
@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return error_page('Sorry, nothing at this URL', 'default_page')
    #return 'Sorry, nothing at this URL.', 404

@app.errorhandler(500)
def internal_server_error(e):
    return error_page('Internal Server Error: ' + str(e),
                      'default_page')
    #return 'Internal Server Error: ' + str(e)

# test
@app.route('/random/')
def read_random_data():
    try:
        (word, definition) = get_random_words(1)[0]
        return render_template('word_def.html',
                               style_url = style_url(),
                               word = word,
                               definition = definition)
    except Exception as e:
        return str(e)

# unused (for practice)
@app.route('/test/')
@app.route('/test/<something>/')
def test_page():
    page += '<body>'
    page += '<h1>App engine + Flask test</h1>'
    page += '<p>this is test paragraph</p>'
    page += '</body>'
    return page
