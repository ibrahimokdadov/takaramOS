import src.models.users.constants as UserConstants
from flask import Blueprint, render_template, make_response

from src.common.database import Database
from src.models.items.views import view_items
from src.models.users.user import User

__author__ = 'ibininja'

user_blueprints = Blueprint('users', __name__)


@user_blueprints.route('/admin/list/users')
def list_users():
    users = User.get_all_users()
    return render_template("admin/list_users.html", users=users)


@user_blueprints.route('/admin/list/user/delete/<string:user_id>')
def delete_user(user_id):
    result = Database.remove_one(UserConstants.COLLECTION, {"_id": user_id})
    #TODO: remove user_id from other collections.
    return make_response(list_users())
