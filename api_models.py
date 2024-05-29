
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str


@app.get("/")
async def get_index():
    return {
        "message": "Get Index"
    }


@app.post("/")
async def get_index():
    return {
        "message": "Post Index"
    }


@app.post("/user/")
async def create_user(item: User):
    return item


@app.get("/user/")
async def read_user():
    return [
        {
         "first_name": "Elshodbek",
         "last_name": "Odilov",
         "username": "Odilov1",
         "email": "example@gmail.com",
         "password": "1234"
        },
        {
         "first_name": "Sherzod",
         "last_name": "Soatov",
         "username": "sher",
         "email": "example@gmail.com",
         "password": "sher1"
        }
    ]


class Product(BaseModel):
    name: str
    description: str
    price: float
    category_id: int


@app.post("/product/")
async def create_product(item: Product):
    return item


@app.get("/product/")
async def read_product():
    return [
        {
         "name": "apple",
         "description": "the best",
         "price": 10.5,
         "category_id": 2
        },
        {
         "name": "cherry",
         "description": "the best",
         "price": 12.5,
         "category_id": 2
        }
    ]


class Category(BaseModel):
    name: str


@app.post("/category/")
async def create_category(item: Category):
    return item


@app.get("/category/")
async def read_category():
    return {
        "name": "fruits"
    }


class Order(BaseModel):
    user_id: int
    product_id: int


@app.post("/order/")
async def create_order(item: Order):
    return item


@app.get("/order/")
async def read_order():
    return {
        "user_id": 1,
        "product_id": 2
    }

