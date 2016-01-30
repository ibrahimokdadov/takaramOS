import datetime
import uuid
import src.models.messages.constants as MessageConstants
from src.common.database import Database

__author__ = 'ibininja'


class Message(object):
    def __init__(self, title, user_id, item_id, date_posted=datetime.datetime.utcnow(), _id=None):
        self.title = title
        self.user_id = user_id
        self.item_id = item_id
        self.date_posted = date_posted
        self._id = uuid.uuid4.hex() if _id is None else _id

    def json(self):
        return {
            "title": self.title,
            "user_id": self.user_id,
            "item_id": self.item_id,
            "date_posted": self.date_posted,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.insert(MessageConstants.COLLECTION, self.json())
