from flask import Blueprint, render_template, session, request, make_response
from src.models.items.item import Item
from src.models.messages.message import Message
from src.models.users.user import User
import src.models.messages.constants as MessageConstants
import src.models.users.constants as UserConstants

__author__ = 'ibininja'

message_blueprints = Blueprint("messages", __name__)


@message_blueprints.route('/user/messages/sent/<string:user_email>')
def get_sent_messages(user_email):
    if session.get('email') is None:
        return render_template("login.jinja2", message="You must be logged in to add items")
    else:
        if user_email == session['email']:
            user = User.get_user_by_email(collection=UserConstants.COLLECTION, email=user_email)
            if user is not None:
                messages = Message.get_sent_messages_by_user_id(user._id)
                recieved_messages = Message.get_recieved_messages_by_user_id(user._id)
                unread_recieved_messages_count = 0
                for recieved_message in recieved_messages:
                    unread_recieved_messages_count += Message.get_unread_recieved_replies_count(user_id=recieved_message.sender_id, item_id=recieved_message.item_id)
                unread_replies_list = {}
                for message in messages:
                    unread_replies_list[message._id] = Message.get_unread_recieved_replies_count(user_id=user._id,
                                                                                                 item_id=message.item_id)

                return render_template("user/messages/sent_messages.jinja2", user_id=user._id, messages=messages,
                                       unread_replies=unread_replies_list,
                                       unread_recieved_messages_count=unread_recieved_messages_count)
            else:
                return render_template("message_center.jinja2", message="Could not locate user")
        else:
            return render_template("message_center.jinja2",
                                   message="Looks like you used an email that could not be authorized")


@message_blueprints.route('/user/messages/recieved/<string:user_email>')
def get_recieved_messages(user_email):
    if session.get('email') is None:
        return render_template("login.jinja2", message="You must be logged in to add items")
    else:
        if user_email == session['email']:
            user = User.get_user_by_email(collection=UserConstants.COLLECTION, email=user_email)
            if user is not None:
                messages = Message.get_recieved_messages_by_user_id(user._id)
                unread_messages_count = Message.get_unread_recieved_messages_count(user._id)
                sent_messages = Message.get_sent_messages_by_user_id(user._id)
                unread_sent_messages_count = 0
                for sent_message in sent_messages:
                    unread_sent_messages_count += Message.get_unread_sent_messages_count(user_id=sent_message.sender_id,
                                                                                         item_id=sent_message.item_id)
                unread_replies_list = {}
                for message in messages:
                    unread_replies_list[message._id] = message.get_unread_recieved_replies_count(user_id=user._id,
                                                                                                 item_id=message.item_id)
                return render_template("user/messages/recieved_messages.jinja2", user_id=user._id, messages=messages,
                                       unread_messages_count=unread_messages_count, unread_replies=unread_replies_list,
                                       unread_sent_messages_count=unread_sent_messages_count)
            else:
                return render_template("message_center.jinja2", message="Could not locate user")
        else:
            return render_template("message_center.jinja2",
                                   message="Looks like you used an email that could not be authorized")


@message_blueprints.route('/user/message/details/<string:message_id>')
def get_message_details(message_id):
    # TODO: add verification mechanism to verify that user is part of the message (user_id, sender_id, recipient_id)
    if session.get('email') is None:
        return render_template("login.jinja2", message="You must be logged in to add items")
    else:
        message = Message.get_message_by_id(message_id)
        if message is not None:
            user = User.get_user_by_email(collection=UserConstants.COLLECTION, email=session['email'])
            if (user._id == message.sender_id) or (user._id == message.recipient_id):
                if (user._id == message.recipient_id):
                    message.mark_massage_read()
                item = Item.get_item_by_id(message.item_id)
                messages = Message.get_messages_by_item_id(message.item_id)
                for reply in messages:
                    if (user._id == reply.recipient_id):
                        reply.mark_massage_read()

                return render_template("user/messages/message_details.jinja2", user_id=user._id, messages=messages,
                                       item=item)
            else:
                return render_template("message_center.jinja2",
                                       message="you are not allowed to view details of this message")
        else:
            return render_template("message_center.jinja2", message="could not find message details")


@message_blueprints.route('/user/messages/add/<string:item_id>', methods=['GET', 'POST'])
def add_message(item_id):
    if session.get('email') is None:
        return render_template("login.jinja2", message="You must be logged in to add items")
    else:
        if request.method == 'GET':
            return render_template("user/messages/add_message.jinja2", item_id=item_id)
        else:
            # TODO: add check sender_id and recipient id to verify they are not same to avoind sending to oneself.
            user = User.get_user_by_email(collection=UserConstants.COLLECTION, email=session['email'])
            title = request.form['title']
            content = request.form['content']
            item_id = item_id
            recipient_id = Item.get_user_id(item_id)
            recipient_user = User.get_user_by_id(collection=UserConstants.COLLECTION, user_id=recipient_id["user_id"])
            # TODO: verify none is none or empty.
            message = Message(title=title, content=content, item_id=item_id, sender_id=user._id,
                              sender_username=user.username, recipient_id=recipient_id["user_id"],
                              recipient_username=recipient_user.username)
            message.save_to_mongo()
            return make_response(get_sent_messages(user.email))


@message_blueprints.route('/user/message/reply/<string:item_id>', methods=['GET', 'POST'])
def add_reply(item_id):
    if session.get('email') is None:
        return render_template("login.jinja2", message="You must be logged in to add items")
    else:
        if request.method == 'POST':

            # TODO: add check sender_id and recipient id to verify they are not same to avoind sending to oneself.
            content = request.form['content']
            message = Message.get_main_message_by_item_id(item_id)
            if message is not None:
                user = User.get_user_by_email(collection=UserConstants.COLLECTION, email=session['email'])
                if user._id == message.sender_id:
                    # TODO: verify none is none or empty.
                    new_message = Message(title=message.title, content=content, item_id=item_id, sender_id=user._id,
                                          sender_username=user.username, recipient_id=message.recipient_id,
                                          recipient_username=message.recipient_username, parent_id=message._id)
                    new_message.save_to_mongo()
                    return make_response(get_sent_messages(user.email))
                elif user._id == message.recipient_id:
                    new_message = Message(title=message.title, content=content, item_id=item_id, sender_id=user._id,
                                          sender_username=user.username, recipient_id=message.sender_id,
                                          recipient_username=message.sender_username, parent_id=message._id)
                    new_message.save_to_mongo()
                    return make_response(get_sent_messages(user.email))
                else:
                    return render_template("message_center.jinja2",
                                           message="you are not allowed to view details of this message")
            else:
                return render_template("message_center.jinja2", message="could not find message to reply to")
        else:
            return render_template("message_center.jinja2")
