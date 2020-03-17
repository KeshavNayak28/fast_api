from starlette.testclient import TestClient
from app import app


''''''
client = TestClient(app)




'''--------------------------------------------Test for Books--------------------------------------------------------'''

def test_add_book():
    response = client.post("/books", json=[{'name':'Superman', 'price':80, 'isbn':8}])
    assert response.status_code == 201

def test_get_book_isbn(isbn=1):
    response = client.get('/books/{}'.format(isbn))
    assert response.status_code == 202

    data =response.json()
    assert data['isbn'] == isbn

def test_delete_book(isbn=8):
    response = client.delete("/books/{}".format(isbn))
    assert response.status_code == 202




'''------------------------------------------------Test for Users----------------------------------------------------'''

#def test_create_user():
#    response = client.post('/users', json={"user_name": "Madhav Nayak", "email": "madhav123@example.com", "user_id": 3})
#    assert response.status_code == 201

def test_get_by_user_id(user_id = 2):
    response = client.get('/users/{}'.format(user_id))
    assert response.status_code == 202

    data=response.json()
    assert data['user_id'] == user_id



'''-----------------------------------------------Test for Purchases-------------------------------------------------'''

def test_user_purchase(user_id=3, isbn=1):
    response = client.get('/purchase/{}/{}'.format(user_id,isbn))
    assert response.status_code == 201


def test_user_purchase_details(user_id=2):
    response = client.get('/purchase/detail/{}'.format(user_id))
    assert response.status_code == 201

    data = response.json()
    assert data['user_id'] == user_id
