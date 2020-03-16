import jsonify
from fastapi import FastAPI, Body, Query
from Database.database import Database
from Database.post import Book
from Database.login import User
from Database.purchase import Purchase
import datetime
from Module import validation
from typing import List

app = FastAPI()


'''calls the Book class and User class in databse.py'''
mongo_book = Book
mongo_user = User
mongo_purchase = Purchase

'''initializes Database connection to deault port 27017'''
Database.intialize()


@app.get('/purcahse/{user_id}/{isbn}')
async def user_purchase(user_id, isbn):
    user_detail = await get_by_user_id(user_id=int(user_id))
    user = {
        'user_name':user_detail['user_name'],
        'email':user_detail['email'],
        'user_id':int(user_id)
    }
    book_detail = await get_book_by_isbn(isbn = isbn)
    book = {
        'name': book_detail['name'],
        'price': book_detail['price'],
        'isbn': int(isbn),
        'date_of_purchase': datetime.datetime.now()
    }
    user.update({'purchase_detail':book})
    mongo_purchase.purchase_to_mongo(user)
    user['_id'] = str(user['_id'])
    return user


@app.get('/purchase/details/{user_id}')
async def user_purchase_detail(user_id):
    all_purchases = mongo_purchase.from_mongo_purchase(int(user_id))
    if len(all_purchases) > 0:
        return all_purchases
    else:
        return 'No Purchases'


'''-------------------------------------------User Collection-------------------------------------------------------'''


@app.post('/users')
async def create_user(user:validation.Create_User =Body(...)):
    user_dict = user.dict()
    user_check= await get_by_user_id(user_dict['user_id'])
    user_email_check = await User.check_for_email(user_dict['email'])
    if len(user_email_check)>0:
        return 'user email {} already exits'.format(user_dict['email'])
    if user_check == 'user doesnt exists':
        user_dict.update({'date_of_creation': datetime.datetime.now()})
        mongo_user.add_user_to_mongo(user_dict)
        return await get_by_user_id(user_dict['user_id'])
    else:
        return 'book already exists'


@app.get('/users{user_id}')
async def get_by_user_id(user_id: int):
    user = User.get_user_mongo(query=user_id)
    if user == None:
        return 'user doesnt exists'
    else:
        user['_id'] = str(user['_id'])
        return user


'''---------------------------------------------Book Collection------------------------------------------------------'''
def validbook(BookObject):
    if 'name' in BookObject and 'price' in BookObject and 'isbn' in BookObject:
        return True
    else:
        return False


'''Gives the book with specified isbn from mongo'''
@app.get("/books/{isbn}")
async def get_book_by_isbn(isbn:int):
    books = mongo_book.from_mongo(isbn)
    if books == None:
        return 'book with isbn {} does not exist'.format(isbn)
    else:
        books['_id'] =  str(books['_id'])
        return books

'''Adds single book or list of books with specified field to mongo'''
@app.post("/books")
async def add_book_to_mongo(books: List[validation.Add_Book] =Body(...)):
    new_collection =[]
    ls = []
    for book in books:
        book_dict = book.dict()
        book_check = await get_book_by_isbn(int(book_dict['isbn']))
        if book_check == 'book with isbn {} does not exist'.format(book_dict['isbn']):
            book_dict.update({'date_of_creation':datetime.datetime.now()})
            mongo_book.add_to_mongo_directly(book_dict)
            book_dict['_id'] = str(book_dict['_id'])
            new_collection.append(book_dict)
        else:
            ls.append(book_dict)

    if len(books) == len(new_collection):
        return new_collection
    else:
        return 'books below sent to mongo \n {0} \n books below already exist \n {1} '.format(new_collection, ls)



'''Update Book to mongo'''
@app.patch('/books/{isbn}')
async def update_mongo(isbn:int, price:int = Query(None, description='enter the price'), name:str= Query(None)):
    books = await get_book_by_isbn(isbn)
    if books == 'book with isbn {} does not exist'.format(isbn):
        return books
    elif name==None:
        update = {'price':price,'name':books['name']}
        mongo_book.update_mongo_book(query=isbn, updates=update)
        return await get_book_by_isbn(int(isbn))
    else:
        update = {'price': price, 'name': name}
        mongo_book.update_mongo_book(query=isbn, updates=update)
        return await get_book_by_isbn(int(isbn))


'''Delete a mongo book'''
@app.delete('/books/{isbn}')
async def delete_from_mongo(isbn):
    books = await get_book_by_isbn(isbn)
    if books == 'book with isbn {} does not exist'.format(isbn):
        return books
    else:
        await mongo_book.delete_from_mongo(isbn)
        return 'Book with isbn {} deleted'.format(isbn)