from pydantic import BaseModel
from typing import Optional


class RegisterModel(BaseModel):
        id: Optional[str]
        username: str
        password: str
        email: str
        is_staff: Optional[bool]
        is_active: Optional[bool]


class LoginModel(BaseModel):
        username: str
        password: str
