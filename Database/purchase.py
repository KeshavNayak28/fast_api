from Database.database import Database

class Purchase:


    @staticmethod
    def purchase_to_mongo(data):
        Database.insert(collection='purchase', data= data)

    @staticmethod
    def from_mongo_purchase(user_id):
        ls = []
        pipeline = ([
            {"$match": {"user_id": int(user_id)}},
            {"$group":
                 {"_id": int(user_id),
                  "purchases": {"$addToSet": "$purchase_detail"}, "email": {"$first": "$email"}
                  }},
            {"$project": {"purchases": 1, "_id": 1, "email": 1}}
        ])
        user_purchases = [user_purchases for user_purchases in  Database.aggregate(collection='purchase', pipeline=pipeline)]
        return user_purchases
