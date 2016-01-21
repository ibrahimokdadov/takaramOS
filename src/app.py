import os
from flask import Flask, render_template, request, session, make_response, url_for, send_from_directory

from src.common.database import Database
from src.models.admins.admin import Admin
from src.models.admins.views import admin_blueprints
from src.models.items.views import item_blueprints, view_items
from src.models.users.user import User
import src.models.admins.constants as AdminConstants
import src.models.users.constants as UserConstants
from src.models.users.views import user_blueprints

__author__ = 'ibininja'

app = Flask(__name__)
app.secret_key = 'takaram'

# UPLOAD_FOLDER = './static/resources/'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app.register_blueprint(item_blueprints)
app.register_blueprint(admin_blueprints)
app.register_blueprint(user_blueprints)


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.template_filter('datetimeformat')
def datetimeformat(value, format='%d/%m/%Y @ %H:%M'):
    return value.strftime(format)


@app.route('/')
def home_page():
    return render_template('home.html', img_name="laptop.jpg")


@app.route('/register', methods=['GET', 'POST'])
def register():
    session['email'] = None
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email, password=password)
        user.save_to_mongo()
        session['email'] = user.email
        return make_response(view_items())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('email') is None:
        if request.method == 'GET':
            return render_template('login.html')
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
                    return render_template("login.html", message="Invalid login")

            else:
                return render_template("login.html", message="User does not exist")
    else:
        if session['email'] is not None:
            return render_template("message_center.html", message="You are already logged In.")
        else:
            return render_template("login.html")


@app.route('/logout')
def logout():
    session['email'] = None
    session['admin'] = None
    return render_template("home.html")


if __name__ == "__main__":
    app.run(port=4556, debug=True)
