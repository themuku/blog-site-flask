from models import User
from flask import session
from flask import current_app, g
from functools import wraps


def get_user():
    if session.get("user_id"):
        return User.query.get(session.get("user_id"))
    return None


def inject_user():
    user = None
    if 'user_id' in session:
        user = get_user()
    g.user = user
    return {}


def inject_user_data(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        inject_user()  # Call the context processor function
        return func(*args, **kwargs)
    return wrapper
