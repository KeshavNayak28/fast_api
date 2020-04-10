from starlette.status import HTTP_201_CREATED, HTTP_202_ACCEPTED
from fastapi import FastAPI, Body, Query, HTTPException
from Database.database import Database
from Database.post import Book
from Database.login import User
from Database.purchase import Purchase
import datetime
from Module import validation
from typing import List

app = FastAPI()


'''calls the Book class, User class, and Purchase class in database.py'''
mongo_book = Book
mongo_user = User
mongo_purchase = Purchase

'''initializes Database connection to deault port 27017'''
Database.intialize()


'''------------------------------------------Purchase Collection-----------------------------------------------------'''
@app.get('/purcahse/{user_id}/{isbn}',status_code=HTTP_201_CREATED, tags=['Purchases'])
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


@app.get('/purchase/details/{user_id}', status_code=HTTP_202_ACCEPTED, tags=['Purchases'])
async def user_purchase_detail(user_id):
    all_purchases = mongo_purchase.from_mongo_purchase(int(user_id))
    if len(all_purchases) > 0:
        return all_purchases
    else:
        return 'No Purchases'


'''-------------------------------------------User Collection-------------------------------------------------------'''

'''Creates a user and adds it to mongo user collection'''
@app.post('/users', status_code=HTTP_201_CREATED, tags=['Users'])
async def create_user(user:validation.Create_User =Body(...),):
    user_dict = user.dict()
    user_check= await User.check_for_user_detail(int(user_dict['user_id']))
    user_email_check = await User.check_for_user_detail(user_dict['email'])
    if len(user_email_check)>0:
        raise HTTPException(status_code=409, detail= 'user email {} already exits'.format(user_dict['email']))
    if len(user_check) == 0:
        user_dict.update({'date_of_creation': datetime.datetime.now()})
        mongo_user.add_user_to_mongo(user_dict)
        return await get_by_user_id(user_dict['user_id'])
    else:
        return 'book already exists'

'''gets user details from mongo user collection'''
@app.get('/users/{user_id}',status_code=HTTP_202_ACCEPTED, tags=['Users'])
async def get_by_user_id(user_id):
    user = User.get_user_mongo(query=int(user_id))
    if user == None:
        raise HTTPException(status_code=404, detail='user doesnt exists')
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
@app.get("/books/{isbn}", status_code=HTTP_202_ACCEPTED, tags=['Books'])
async def get_book_by_isbn(isbn:int):
    books = mongo_book.from_mongo(isbn)
    if books == None:
        raise HTTPException(status_code=404, detail='book with isbn {} does not exist'.format(isbn))
    else:
        books['_id'] =  str(books['_id'])
        return books


'''Adds single book or list of books with specified field to mongo'''
@app.post("/books",  status_code=HTTP_201_CREATED,tags=['Books'])
async def add_book_to_mongo(books: List[validation.Add_Book] =Body(...)):
    new_collection =[]
    ls = []
    for book in books:
        book_dict = book.dict()
        book_check = await mongo_book.find_isbn_mongo(book_dict['isbn'])
        print(book_check)
        if len(book_check) == 0:
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
@app.patch('/books/{isbn}',tags=['Books'])
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
@app.delete('/books/{isbn}', status_code=HTTP_202_ACCEPTED, tags=['Books'])
async def delete_from_mongo(isbn:int):
    books = await mongo_book.find_isbn_mongo(isbn)
    if len(books) == 0:
        raise HTTPException(status_code=404, detail='book with isbn {} does not exist'.format(isbn))
    else:
        await mongo_book.delete_from_mongo(isbn)
        return 'Book with isbn {} deleted'.format(isbn)