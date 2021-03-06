from flask import session
from google.appengine.ext import ndb

from mymodules import ndbi


class User(ndb.Model):
    user_id = ndb.StringProperty()
    password = ndb.StringProperty()


def get_user_id():
    if 'user_id' in session:
        return session['user_id']
    else:
        return None

def is_anonymous():
    return 'user_id' in session


def user_exists(user_id):
    return ndbi.read(User, user_id = user_id) != None


def add_user(user_id):
    user_key = User(user_id = user_id,
                    password = '')
    user_key.key = ndb.Key(User, user_id)
    user_key.put()


def get_user_key(user_id):
    if user_id != None:
        return ndb.Key(User, user_id)
    else:
        return ndb.Key(User, 'anonymous')


def current_user():
    if 'user_id' in session:
        return ndb.Key(User, session['user_id'])
    else:
        return anonymous()


def anonymous():
    return ndb.Key(User, 'anonymous')