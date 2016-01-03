from src.common.database import Database

from src.models.users.user import User
import src.models.admins.constants as AdminConstants
import src.models.items.constants as ItemConstants
import src.models.users.constants as UserConstants

__author__ = 'ibininja'


class Admin(User):
    def __init__(self, username, email, password, _id=None):
        super(Admin, self).__init__(username=username, email=email, password=password)

    def json(self):
        return {
            "email": self.email,
            "password": self.password,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.insert(AdminConstants.COLLECTION, self.json())

    @staticmethod
    def get_number_of_all_items():
        items_number = Database.find_all_count(ItemConstants.COLLECTION)
        return items_number

    @staticmethod
    def get_number_of_all_pending_items():
        items_number = Database.find_count(ItemConstants.COLLECTION, {"approved": False})
        return items_number

    @staticmethod
    def get_number_of_all_approved_items():
        items_number = Database.find_count(ItemConstants.COLLECTION, {"approved": True})
        return items_number

    @staticmethod
    def get_number_of_users():
        users_number = Database.find_all_count(UserConstants.COLLECTION)
        return users_number