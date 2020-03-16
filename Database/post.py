from Database.database import Database

class Book:

    @staticmethod
    def add_to_mongo_directly(data):
        mongo_data= Database.insert(collection='posts', data=data)
        return mongo_data

    @staticmethod
    def from_mongo(query):
        mongo_data =  Database.find_one(collection='posts', query={'isbn':int(query)})
        if mongo_data == None:
            return None
        else:
            return dict(mongo_data)

    @staticmethod
    def update_mongo_book(query, updates):
        Database.update(collection='posts', myquery={'isbn':int(query)}, updates={'$set':updates})

    @staticmethod
    def delete_from_mongo(query):
        Database.delete_one(collection='posts', query={'isbn':int(query)})