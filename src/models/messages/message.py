import datetime
import uuid
import src.models.messages.constants as MessageConstants
from src.common.database import Database

__author__ = 'ibininja'


class Message(object):
    def __init__(self, title, content, item_id, sender_id, sender_username, recipient_id, recipient_username, date_posted=datetime.datetime.utcnow(),
                 is_read=False, parent_id=None, _id=None):
        self.title = title
        self.content = content
        self.item_id = item_id
        self.sender_id = sender_id
        self.sender_username = sender_username
        self.recipient_id = recipient_id
        self.recipient_username = recipient_username
        self.date_posted = date_posted
        self.is_read = is_read
        self.parent_id = parent_id
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "title": self.title,
            "content": self.content,
            "item_id": self.item_id,
            "sender_id": self.sender_id,
            "sender_username":self.sender_username,
            "recipient_id": self.recipient_id,
            "recipient_username":self.recipient_username,
            "date_posted": self.date_posted,
            "is_read": self.is_read,
            "parent_id": self.parent_id,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.insert(MessageConstants.COLLECTION, self.json())

    @classmethod
    def get_message_by_id(cls, message_id):
        message = Database.find_one(MessageConstants.COLLECTION, {"_id": message_id})
        if message is not None:
            return cls(**message)

    @classmethod
    def get_messages_by_item_id(cls, item_id):
        messages = Database.find(MessageConstants.COLLECTION, {"item_id": item_id})
        if messages is not None:
            return [cls(**message) for message in messages]

    @classmethod
    def get_main_message_by_item_id(cls, item_id):
        message = Database.find_one(MessageConstants.COLLECTION, {"item_id":item_id, "parent_id":None})
        if message is not None:
            return cls(**message)

    @classmethod
    def get_messages_by_user_id(cls, user_id):
        messages = Database.find(MessageConstants.COLLECTION, {"user_id": user_id})
        if messages is not None:
            return [(cls(**message) for message in messages)]

    @classmethod
    def get_sent_messages_by_user_id(cls, user_id):
        messages = Database.find(MessageConstants.COLLECTION, {"sender_id": user_id, "parent_id": None})
        if messages is not None:
            return [cls(**message) for message in messages]

    @classmethod
    def get_recieved_messages_by_user_id(cls, user_id):
        messages = Database.find(MessageConstants.COLLECTION, {"recipient_id": user_id, "parent_id": None})
        if messages is not None:
            return [cls(**message) for message in messages]

    @classmethod
    def get_unread_recieved_messages_count(cls, user_id):
        count = Database.find(MessageConstants.COLLECTION, {"recipient_id":user_id, "is_read":False, "parent_id":None}).count()
        return count

    @classmethod
    def get_unread_recieved_replies_count(cls, user_id, item_id):
        count = Database.find(MessageConstants.COLLECTION, {"recipient_id":user_id, "item_id":item_id, "is_read":False, "parent_id":{"$ne":None}}).count()
        return count

    @classmethod
    def get_unread_sent_messages_count(cls, user_id, item_id ):
        count = Database.find(MessageConstants.COLLECTION, {"recipient_id":user_id, "is_read":False, "item_id":item_id, "parent_id":{"$ne":None}}).count()
        return count

    @classmethod
    def get_unread_recieved_replies(cls, user_id):
        replies = Database.find(MessageConstants.COLLECTION, {"recipient_id":user_id, "is_read":False, "parent_id":{"$ne":None}})
        if replies is not None:
            return [cls(**reply) for reply in replies]

    def mark_massage_read(self):
        Database.update_one(MessageConstants.COLLECTION, {"_id":self._id}, {"$set":{"is_read":True}})
