from functools import wraps

from flask import session, url_for, redirect, request

__author__ = 'ibininja'

def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('login', next=request.path)) #next=> to return to location before login.
        return func(*args, **kwargs)
    return decorated_function


