import os
from flask import Flask, render_template, request, session, make_response, url_for, send_from_directory


from src.common.database import Database
from src.models.items.item import Item
from src.models.items.views import item_blueprints, view_items
from src.models.users.user import User

__author__ = 'ibininja'

app = Flask(__name__)
app.secret_key = 'takaram'

# UPLOAD_FOLDER = './static/resources/'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app.register_blueprint(item_blueprints)

@app.before_first_request
def initialize_database():
    Database.initialize()

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%d-%m-%Y @ %H:%M'):
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
            user = User.get_user_by_email(username_email)
            if user is not None:
                if user.password == password:
                    session['email'] = user.email
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





@app.route('/admin/pending/items')
def pending_items():
    items = Item.get_pending_items()
    return render_template("admin/pending_items.html", items=items)


@app.route('/user/items/approve/<string:item_id>')
def approve_item(item_id):
    if session.get('email') is not None:
        item = Item.get_item_by_id(item_id)
        if item is not None:
            Item.update_item(item_id)
            return make_response(pending_items())
        return make_response(pending_items())
    else:
        return render_template("login.html", message="You must be logged-in to remove items.")


@app.route('/logout')
def logout():
    session['email'] = None
    return render_template("home.html")


if __name__ == "__main__":
    app.run(port=4555, debug=True)
