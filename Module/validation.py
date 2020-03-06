from pydantic import BaseModel


class Add_Book(BaseModel):
    name:str
    price:int
    isbn:int

class Update_Book(BaseModel):
    name:str
    price:int