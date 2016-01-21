import src.models.users.constants as UserConstants
from flask import Blueprint, render_template

from src.models.users.user import User

__author__ = 'ibininja'

user_blueprints = Blueprint('users', __name__)

@user_blueprints.route('/admin/list/users')
def list_users():

    users = User.get_all_users()
    return render_template("admin/list_users.html", users=users)