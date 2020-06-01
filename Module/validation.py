from pydantic import BaseModel, EmailStr


class Book_Detail(BaseModel):
    pages:int
    published_date: str

class Add_Book(BaseModel):
    name:str
    price:int
    isbn:int
    book_detail: Book_Detail

class Update_Book(BaseModel):
    name:str
    price:int

class Create_User(BaseModel):
    user_name:str
    email:EmailStr
    user_id:int