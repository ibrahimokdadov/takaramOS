import pymongo

__author__ = 'ibininja'


class Database(object):

    URI = "mongodb://127.0.0.1:27017"
    DB = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DB = client['takaram_db']

    @staticmethod
    def insert(collection, data):
        Database.DB[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DB[collection].find(query)

    @staticmethod
    def find_all(collection):
        return Database.DB[collection].find()

    @staticmethod
    def find_all_count(collection):
        return Database.DB[collection].find().count()

    @staticmethod
    def find_count(collection, query):
        return Database.DB[collection].find(query).count()

    @staticmethod
    def find_one(collection, query, projection=None):
        return Database.DB[collection].find_one(query, projection)

    @staticmethod
    def find_or(collection, query):
        return Database.DB[collection].find_one({'$or': [query]})

    @staticmethod
    def find_or_count(collection, query):
        return Database.DB[collection].find_one({'$or': [query]}).count()

    @staticmethod
    def find_and(collection, query):
        return Database.DB[collection].find_one({'$and': [query]})

    @staticmethod
    def find_and_count(collection, query):
        return Database.DB[collection].find_one({'$and': [query]}).count()

    @staticmethod
    def remove(collection, query):
        return Database.DB[collection].remove(query)

    @staticmethod
    def remove_one(collection, query):
        return Database.DB[collection].delete_one(query)

    @staticmethod
    def update_one(collection, query, setquery):
        return Database.DB[collection].update(query, setquery)
