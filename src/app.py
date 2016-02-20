import os
from flask import Flask, render_template, request, session, make_response, url_for, send_from_directory

from src.common.database import Database
from src.models.admins.admin import Admin
from src.models.admins.views import admin_blueprints
from src.models.items.item import Item
from src.models.items.views import item_blueprints, view_items
from src.models.messages.views import message_blueprints
from src.models.users.user import User
import src.models.admins.constants as AdminConstants
import src.models.users.constants as UserConstants
import src.models.items.constants as ItemConstants
from src.models.users.views import user_blueprints

__author__ = 'ibininja'

app = Flask(__name__)
app.secret_key = 'takaram'

# UPLOAD_FOLDER = './static/resources/'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app.register_blueprint(item_blueprints)
app.register_blueprint(admin_blueprints)
app.register_blueprint(user_blueprints)
app.register_blueprint(message_blueprints)

@app.before_first_request
def initialize_database():
    Database.initialize()


@app.template_filter('datetimeformat')
def datetimeformat(value, format='%d/%m/%Y @ %H:%M'):
    return value.strftime(format)

@app.template_filter('is_list')
def is_list(value):
    return isinstance(value, list)


@app.route('/')
def index():
    return render_template('home.jinja2', img_name="laptop.jpg")


@app.route('/register', methods=['GET', 'POST'])
def register():
    session['email'] = None
    if request.method == 'GET':
        return render_template('register.jinja2')
    else:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User.get_user_by_username(username, UserConstants.COLLECTION)
        if user is None:
            user = User.get_user_by_email(email, UserConstants.COLLECTION)
            if user is None:
                user = User(username=username, email=email, password=password)
                user.save_to_mongo()
                session['email'] = user.email
                return make_response(view_items())
        return render_template("register.jinja2", message="Opps...Account information (username/email) are taken...Are you sure it is not you?")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('email') is None:
        if request.method == 'GET':
            return render_template('login.jinja2')
        else:
            username_email = request.form['username_email']
            password = request.form['password']
            user = User.get_user_by_email(username_email, UserConstants.COLLECTION)
            if user is not None:
                if user.password == password:
                    session['email'] = user.email
                    admin = Admin.get_user_by_email(username_email, AdminConstants.COLLECTION)
                    if admin is not None:
                        session['admin'] = admin.email
                    return make_response(view_items())
                else:
                    return render_template("login.jinja2", message="Invalid login")

            else:
                return render_template("login.jinja2", message="User does not exist")
    else:
        if session['email'] is not None:
            return render_template("message_center.jinja2", message="You are already logged In.")
        else:
            return render_template("login.jinja2")


@app.route('/logout')
def logout():
    session['email'] = None
    session['admin'] = None
    return render_template("home.jinja2")

@app.route('/search', methods=['GET', 'POST'])
def search():
    word = request.form['search_box']
    results = Item.search_items(word)
    return render_template("search.jinja2", results=results)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(port=4556, debug=True)
