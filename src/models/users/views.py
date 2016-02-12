import src.models.users.constants as UserConstants
from flask import Blueprint, render_template, make_response, request, session

from src.common.database import Database
from src.models.items.views import view_items
from src.models.users.user import User

__author__ = 'ibininja'

user_blueprints = Blueprint('users', __name__)


@user_blueprints.route('/admin/list/users')
def list_users():
    users = User.get_all_users()
    return render_template("admin/list_users.jinja2", users=users)


@user_blueprints.route('/admin/list/user/delete/<string:user_id>')
def delete_user(user_id):
    result = Database.remove_one(UserConstants.COLLECTION, {"_id": user_id})
    # TODO: remove user_id from other collections.
    return make_response(list_users())


@user_blueprints.route('/user/set/profile', methods=["POST", "GET"])
def set_profile():
    if session.get('email') is None:
        return render_template("login.jinja2", message="You must be logged in to add profile")
    else:
        if request.method == 'GET':
            return render_template("user/add_profile.html")
        else:
            full_name = request.form['full_name']
            country = request.form['country']
            user = User.get_user_by_email(collection=UserConstants.COLLECTION, email=session['email'])
            profile = [{"full_name": full_name}, {"country": country}]
            user.set_profile(profile)
            return render_template("user/view_profile.html")


@user_blueprints.route('/user/get/profile')
def get_profile():
    if session.get('email') is None:
        return render_template("login.jinja2", message="You must be logged in to add profile")
    else:
        user = User.get_user_by_email(collection=UserConstants.COLLECTION, email=session['email'])
        if user is not None:
            profile = user.profile
            if not profile:
                return make_response(set_profile())

            return render_template("user/view_profile.html", profile=profile)
        else:
            return render_template("login.jinja2", message="You must be logged in to add profile")
