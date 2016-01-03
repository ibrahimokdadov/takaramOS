from flask import Blueprint, session, render_template, make_response

from src.models.admins.admin import Admin
from src.models.items.item import Item

__author__ = 'ibininja'

admin_blueprints = Blueprint('admins', __name__)


@admin_blueprints.route('/admin/dashboard')
def dashboard():
    # verify User is admin
    if session.get('email') is None:
        return render_template("login.html", message="The page you requested is not available")
    else:
        admin = Admin.get_user_by_email(session['email'])
        if admin is None:
            return render_template("message_center.html",
                                   message="System could not detect rights to access to this area.")
        else:
            items_count = admin.get_number_of_all_items()
            approved_items_count = admin.get_number_of_all_approved_items()
            pending_items_count = admin.get_number_of_all_pending_items()
            users_count = admin.get_number_of_users()
            return render_template("admin/dashboard.html", items_count=items_count,
                                   approved_items_count=approved_items_count, pending_items_count=pending_items_count,
                                   users_count=users_count)





@admin_blueprints.route('/admin/pending/items')
def pending_items():
    items = Item.get_pending_items()
    return render_template("admin/pending_items.html", items=items)


@admin_blueprints.route('/user/items/approve/<string:item_id>')
def approve_item(item_id):
    if session.get('email') is not None:
        item = Item.get_item_by_id(item_id)
        if item is not None:
            Item.update_item(item_id)
            return make_response(pending_items())
        return make_response(pending_items())
    else:
        return render_template("login.html", message="You must be logged-in to remove items.")