from functools import wraps

from flask import session, url_for, redirect, request, flash

__author__ = 'ibininja'

def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            flash("You must be logged in")
            return redirect(url_for('login', next=request.path)) #next=> to return to location before login.
        return func(*args, **kwargs)
    return decorated_function

def requires_admin_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session.keys() or session['admin'] is None:
            flash("You are not authorized to complete the requrested action")
            return redirect(url_for('login', next=request.path)) #next=> to return to location before login.
        return func(*args, **kwargs)
    return decorated_function

