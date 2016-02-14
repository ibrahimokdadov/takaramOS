import os

import src.models.users.constants as UserConstants
from flask import Blueprint, render_template, make_response, request, session

from src.common.database import Database
from src.models.items.views import view_items
from src.models.users.user import User
import src.models.users.decorators as user_decorators

__author__ = 'ibininja'

user_blueprints = Blueprint('users', __name__)

APP_ROOT = (os.path.realpath('./'))


@user_blueprints.route('/admin/list/users')
@user_decorators.requires_admin_login
def list_users():
    users = User.get_all_users()
    return render_template("admin/list_users.jinja2", users=users)


@user_blueprints.route('/admin/list/user/delete/<string:user_id>')
@user_decorators.requires_admin_login
def delete_user(user_id):
    result = Database.remove_one(UserConstants.COLLECTION, {"_id": user_id})
    # TODO: remove user_id from other collections.
    return make_response(list_users())


@user_blueprints.route('/user/set/profile', methods=["POST", "GET"])
@user_decorators.requires_login
def set_profile():
    # if session.get('email') is None:
    #     return render_template("login.jinja2", message="You must be logged in to add profile")
    # else:
    if request.method == 'GET':
        return render_template("user/add_profile.html")
    else:
        full_name = request.form['full_name']
        country = request.form['country']
        uploaded_file_list = request.files.getlist("file")
        user = User.get_user_by_email(collection=UserConstants.COLLECTION, email=session['email'])

        # Target folder for these uploads.
        target = os.path.join(APP_ROOT, 'static/resources/images/{}/profile'.format(user.username))
        # target = './static/resources/{}'.format(upload_key)
        try:
            if not os.path.isdir(target):
                os.mkdir(target)
        except Exception as e:
            print(e)
            return render_template("message_center.jinja2",
                                   message="System was not able to store uploaded file in server! Contact Admin.")
        filename = ''

        images_path =''
        for upload in uploaded_file_list:
            print(upload.filename)
            filename = upload.filename.rsplit("/")[0]
            # TODO: Change this to be in Config File.
            destination = os.path.join(APP_ROOT,
                                       'static/resources/images/{}/profile/{}'.format(user.username, filename))
            images_path = 'resources/images/{}/profile/{}'.format(user.username, filename)
            # destination = "/".join([target, filename])
            upload.save(destination)
        profile = [{"avatar": images_path},{"full_name": full_name}, {"country": country} ]
        user.set_profile(profile)
        return make_response(get_profile())


@user_blueprints.route('/user/get/profile')
@user_decorators.requires_login
def get_profile():
    # if session.get('email') is None:
    #     return render_template("login.jinja2", message="You must be logged in to add profile")
    # else:
    user = User.get_user_by_email(collection=UserConstants.COLLECTION, email=session['email'])
    if user is not None:
        profile = user.profile
        if not profile:
            return make_response(set_profile())

        return render_template("user/view_profile.html", profile=profile)
    else:
        return render_template("login.jinja2", message="You must be logged in to add profile")
