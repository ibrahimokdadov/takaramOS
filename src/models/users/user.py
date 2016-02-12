import uuid

import datetime

import src.models.users.constants as UserConstants
from src.common.database import Database
from src.models.items.item import Item

__author__ = 'ibininja'


class User(object):
    def __init__(self, username, email, password, date_created=datetime.datetime.utcnow(),profile=[], _id=None):
        self.username = username
        self.email = email
        self.password = password
        self.date_created= date_created
        self.profile = profile
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "date_created": self.date_created,
            "profile": self.profile,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.insert(UserConstants.COLLECTION, self.json())

    def add_item(self, title, description, image_url, contact):
        item = Item(title, description, image_url, contact, self._id)
        item.save_to_mongo()

    @classmethod
    def get_user_by_id(cls, user_id, collection):
        user = Database.find_one(collection, {"_id": user_id})
        if user is not None:
            return cls(**user)

    @classmethod
    def get_user_by_email(cls, email, collection):
        user = Database.find_one(collection, {"email": email})
        if user is not None:
            return cls(**user)

    @classmethod
    def get_user_by_username(cls, username, collection):
        user = Database.find_one(collection, {"username": username})
        if user is not None:
            return cls(**user)

    @classmethod
    def get_all_users(cls):
        users = Database.find_all(UserConstants.COLLECTION)
        if users is not None:
            return [cls(**user) for user in users]

    @staticmethod
    def delete_user(user_id):
        result = Database.remove()

    @classmethod
    def get_posted_users_count(cls):
        users = Database.aggregate(UserConstants.COLLECTION, [{"$group":{"_id":"$date_created", "count":{"$sum":1}}}, {"$sort":{"_id":1}}])
        return users

    def set_profile(self, profile):
        Database.update_one(UserConstants.COLLECTION, {"_id":self._id}, {"$set":{"profile":profile}})

