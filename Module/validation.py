from pydantic import BaseModel, EmailStr


class Add_Book(BaseModel):
    name:str
    price:int
    isbn:int

class Update_Book(BaseModel):
    name:str
    price:int

class Create_User(BaseModel):
    user_name:str
    email:EmailStr
    user_id:int