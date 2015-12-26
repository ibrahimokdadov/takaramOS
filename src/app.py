import os
from flask import Flask, render_template, request, session, make_response, url_for, send_from_directory
from src.common.database import Database
from src.models.items.item import Item
from src.models.users.user import User

__author__ = 'ibininja'

app = Flask(__name__)
app.secret_key = 'takaram'

# UPLOAD_FOLDER = './static/resources/'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.before_first_request
def initialize_database():
    Database.initialize()


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


@app.route('/user/items/view')
def view_items():
    if session.get('email') is None:
        return render_template("login.html", message="You must be logged in to view your items")
    else:
        if session['email'] is None:
            return render_template("login.html", message="You must be logged in to view your items")
        user = User.get_user_by_email(session['email'])
        items = Item.get_items_by_user_id(user._id)
        return render_template("items.html", items=items)


@app.route('/items/view')
def view_all_items():
    items = Item.get_all_items()
    return render_template("all_items.html", items=items)


@app.route('/user/items/add', methods=['POST', 'GET'])
def add_item():
    if session.get('email') is None:
        return render_template("login.html", message="You must be logged in to add items")
    else:
        if request.method == 'GET':
            return render_template("add_item.html")
        else:
            uploaded_file_list = request.files.getlist("file")
            title = request.form['title']
            description = request.form['description']
            contact = request.form['contact']
            user = User.get_user_by_email(session['email'])
            # Target folder for these uploads.
            target = os.path.join(APP_ROOT, 'static/resources/images/{}'.format(user.username))
            # target = './static/resources/{}'.format(upload_key)
            try:
                if not os.path.isdir(target):
                    os.mkdir(target)
            except:
                return render_template("message_center.html",
                                       message="System was not able to store uploaded file in server! Contact Admin.")
            filename = ''
            for upload in uploaded_file_list:
                filename = upload.filename.rsplit("/")[0]
                # TODO: Change this to be in Config File.
                destination = os.path.join(APP_ROOT, 'static/resources/images/{}/{}'.format(user.username, filename))
                # destination = "/".join([target, filename])

                upload.save(destination)
            user.add_item(title=title, description=description,
                          image_url='resources/images/{}/{}'.format(user.username, filename), contact=contact)
            # TODO: make this go for approval center.
            return make_response(view_items())


@app.route('/user/items/detail/<string:item_id>')
def item_details(item_id):
    item = Item.get_item_by_id(item_id)
    if item is not None:
        return render_template("item_details.html", item=item)
    else:
        return render_template("message_center.html",
                               message="Item {} does not have details. Contact Us if you need further information!".format(
                                       item.title))


@app.route('/user/items/delete/<string:item_id>')
def delete_item(item_id):
    if session.get('email') is not None:
        item = Item.get_item_by_id(item_id)
        if item is not None:
            user = User.get_user_by_email(session['email'])
            if item.user_id == user._id:
                item.remove_item()
                return make_response(view_items())
        return render_template("items.html", message="You can't remove item")
    else:
        return render_template("login.html", message="You must be logged-in to remove items.")


@app.route('/logout')
def logout():
    session['email'] = None
    return render_template("home.html")


if __name__ == "__main__":
    app.run(port=4555, debug=True)
