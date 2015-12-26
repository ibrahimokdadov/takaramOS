import uuid
import src.models.users.constants as UserConstants
from src.common.database import Database
from src.models.items.item import Item

__author__ = 'ibininja'


class User(object):
    def __init__(self, username, email, password, _id=None):
        self.username = username
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.insert(UserConstants.COLLECTION, self.json())

    def add_item(self, title, description, image_url, contact):
        item = Item(title, description, image_url, contact, self._id)
        item.save_to_mongo()

    @classmethod
    def get_user_by_id(cls, user_id):
        user = Database.find_one(UserConstants.COLLECTION, {"_id": user_id})
        if user is not None:
            return cls(**user)

    @classmethod
    def get_user_by_email(cls, email):
        user = Database.find_one(UserConstants.COLLECTION, {"email": email})
        if user is not None:
            return cls(**user)

    @classmethod
    def get_user_by_username(cls, username):
        user = Database.find_one(UserConstants.COLLECTION, {"username": username})
        if user is not None:
            return cls(**user)

