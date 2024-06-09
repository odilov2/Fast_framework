from pydantic import BaseModel
from typing import Optional


class RegisterModel(BaseModel):
        id: Optional[int]
        first_name: str
        last_name: str
        username: str
        password: str
        email: str
        is_staff: Optional[bool]
        is_active: Optional[bool]


class UsersModel(BaseModel):
        id: Optional[int]
        first_name: str
        last_name: str
        username: str
        password: str
        email: str
        is_staff: Optional[bool]
        is_active: Optional[bool]


class LoginModel(BaseModel):
        username: str
        password: str


class CategoryModel(BaseModel):
        id: Optional[int]
        name: str


class ProductModel(BaseModel):
        id: Optional[int]
        name: str
        description: str
        counts : int
        price: float
        category_id: Optional[int]


class OrderModel(BaseModel):
        id: Optional[int]
        users_id: int
        product_id: int
        counts: int
        oder_status: str


class UserOrderModel(BaseModel):
        username: str


# class JwtModel(BaseModel):
#     authjwt_secret_key: str = '968c69c21aacca8fc11df9c57950f5317c47994299512e5f169393dcdd586bfb'
