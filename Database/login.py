from Database.database import Database


class User:

    @staticmethod
    def add_user_to_mongo(data):
        Database.insert(collection = 'users', data = data)

    @staticmethod
    def get_user_mongo(query):
        mongo_user =  Database.find_one_data(collection='users', query={'user_id': query})
        return mongo_user

    @staticmethod
    async def check_for_user_detail(query):
        mongo_email = [mongo_email for mongo_email in Database.find_data(collection='users', query= {'email':query})]
        return mongo_email