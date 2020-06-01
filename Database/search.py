from Database.database import Database
import pymongo


class Search:

    @staticmethod
    def query_score_name(key):
        cursor = Database.DATABASE['books'].find({'$text': {'$search': key}}, {'score': {'$meta': "textScore"}})
        search_result = cursor.sort([('score', {'$meta': 'textScore'})])
        return search_result

    @staticmethod
    def query_score_page(page_no):
        range1 = page_no - 50
        range2 = page_no + 50
        query = {'book_detail.pages':{'$gte':range1, '$lte':range2}}
        cursor = Database.find_data(collection='books', query=query)
        return cursor

