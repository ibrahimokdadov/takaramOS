import os

from flask import Blueprint, session, render_template, make_response, request, jsonify

from src.models.items.item import Item
from src.models.users.user import User
import src.models.admins.constants as AdminConstants
import src.models.items.constants as ItemConstants
import src.models.users.constants as UserConstants

__author__ = 'ibininja'

item_blueprints = Blueprint('items', __name__)

# UPLOAD_FOLDER = './static/resources/'
APP_ROOT = (os.path.realpath('./'))


@item_blueprints.route('/user/items/view')
def view_items():
    if session.get('email') is None:
        return render_template("login.html", message="You must be logged in to view your items")
    else:
        if session['email'] is None:
            return render_template("login.html", message="You must be logged in to view your items")
        user = User.get_user_by_email(session['email'], UserConstants.COLLECTION)
        items = Item.get_items_by_user_id(user._id)
        return render_template("items.html", items=items)


@item_blueprints.route('/items/view')
def view_all_items():
    items = Item.get_all_approved_items()
    return render_template("all_items.html", items=items)


@item_blueprints.route('/user/items/add', methods=['POST', 'GET'])
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
            user = User.get_user_by_email(session['email'],UserConstants.COLLECTION)
            # Target folder for these uploads.
            target = os.path.join(APP_ROOT, 'static/resources/images/{}'.format(user.username))
            # target = './static/resources/{}'.format(upload_key)
            try:
                if not os.path.isdir(target):
                    os.mkdir(target)
            except Exception as e:
                print(e)
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


@item_blueprints.route('/user/items/detail/<string:item_id>')
def item_details(item_id):
    item = Item.get_item_by_id(item_id)
    if item is not None:
        if session.get('email') is not None:
            user = User.get_user_by_email(email=session['email'], collection=UserConstants.COLLECTION)

            if (user._id == item.user_id) or (session.get('admin') is not None):
                return render_template("item_details.html", item=item, editable=True)
            else:
                return render_template("item_details.html", item=item)
        else:
            return render_template("item_details.html", item=item)
    else:
        return render_template("message_center.html",
                               message="Item {} does not have details. Contact Us if you need further information!".format(
                                       item.title))


@item_blueprints.route('/user/items/delete/<string:item_id>')
def delete_item(item_id):
    if session.get('email') is not None:
        item = Item.get_item_by_id(item_id)
        if item is not None:
            user = User.get_user_by_email(email=session['email'], collection=UserConstants.COLLECTION)
            if item.user_id == user._id:
                item.remove_item()
                return make_response(view_items())
        return render_template("items.html", message="You can't remove item")
    else:
        return render_template("login.html", message="You must be logged-in to remove items.")


@item_blueprints.route('/user/items/edit/<string:item_id>/<string:attribute_name>/<string:attribute_value>')
def edit_item(item_id, attribute_name, attribute_value):
    item = Item.get_item_by_id(item_id)
    if item is not None:
        item.update_item(attribute_name=attribute_name, attribute_value=attribute_value)
        if session.get('admin') is not None:
            return render_template("item_details.html", item=item)
        else:
            item.update_item(attribute_name="approved", attribute_value=False)
            return render_template("message_center.html", message="Item will published as soon as the change is approved")
    else:
        return render_template("message_center.html",
                               message="Could not update Item {} . Contact Us if you need further information!".format(
                                       item.title))


@item_blueprints.route('/user/item/update/title', methods=['GET', 'POST'])
def update_title():
    item_id = request.form['pk']
    value = request.form['value']
    item = Item.get_item_by_id(item_id)
    item.update_item("title", value)
    if session.get('admin') is not None:
        return render_template("item_details.html", item=item)
    else:
        item.update_item(attribute_name="approved", attribute_value=False)
        return render_template("message_center.html", message="Item will published as soon as the change is approved")


@item_blueprints.route('/user/item/update/description', methods=['GET', 'POST'])
def update_description():
    item_id = request.form['pk']
    value = request.form['value']
    item = Item.get_item_by_id(item_id)
    item.update_item("description", value)
    if session.get('admin') is not None:
        return render_template("item_details.html", item=item)
    else:
        item.update_item(attribute_name="approved", attribute_value=False)
        return render_template("message_center.html", message="Item will published as soon as the change is approved")


@item_blueprints.route('/user/item/update/contact', methods=['GET', 'POST'])
def update_contact():
    item_id = request.form['pk']
    value = request.form['value']
    item = Item.get_item_by_id(item_id)
    item.update_item("contact", value)
    if session.get('admin') is not None:
        return render_template("item_details.html", item=item)
    else:
        item.update_item(attribute_name="approved", attribute_value=False)
        return render_template("message_center.html", message="Item will published as soon as the change is approved")
