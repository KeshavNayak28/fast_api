from fastapi import FastAPI, Body, Query
from Database.database import Database
from fastapi.encoders import jsonable_encoder
from Database.post import Book
import datetime
from Module import validation
from typing import List


app = FastAPI()

mongo_book = Book()

Database.intialize()


@app.get("/books/{isbn}")
async def get_book_by_isbn(isbn:int):
    books = mongo_book.from_mongo(isbn)
    if books == None:
        return 'book with isbn {} does not exist'.format(isbn)
    else:
        books['_id'] =  str(books['_id'])
        return books

@app.post("/books")
async def add_book_to_mongo(books: List[validation.Add_Book] =Body(...)):
    for book in books:
        book_dict = book.dict()
        books = await get_book_by_isbn(int(book_dict['isbn']))
        if books == 'book with isbn {} does not exist'.format(book_dict['isbn']):
            book_dict.update({'date_of_creation':datetime.datetime.now()})
            mongo_book.add_to_mongo_directly(book_dict)
            return await get_book_by_isbn(int(book_dict['isbn']))
        else:
            return 'book with isbn {} already exists'.format(int(isbn))

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

@app.delete('/books/{isbn}')
async def delete_from_mongo(isbn):
    books = await get_book_by_isbn(isbn)
    if books == 'book with isbn {} does not exist'.format(isbn):
        return books
    else:
        mongo_book.delete_from_mongo(isbn)
        return 'Book with isbn {} deleted'.format(isbn)