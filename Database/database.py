import pymongo

class Database:
    DATABASE = None
    uri = "mongodb://127.0.0.1:27017"

    @staticmethod
    def intialize():
        client = pymongo.MongoClient(Database.uri)
        Database.DATABASE = client['config']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)


    @staticmethod
    def delete_one(collection, query):
        return Database.DATABASE[collection].delete_one(query)

    @staticmethod
    def update( myquery, updates, collection):
        return Database.DATABASE[collection].update_one(myquery, updates)