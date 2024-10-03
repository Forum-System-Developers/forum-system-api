from typing import Annotated
from pydantic import BaseModel, EmailStr, constr


class UserBase(BaseModel):
    username: Annotated[str, constr(strip_whitespace=True, min_length=3, max_length=30)]
    first_name: Annotated[str, constr(strip_whitespace=True, min_length=2, max_length=30)]
    last_name: Annotated[str, constr(strip_whitespace=True, min_length=2, max_length=30)]
    email: EmailStr


class UserCreate(UserBase):
    password: Annotated[str, constr(strip_whitespace=True, min_length=8, max_length=30)]


class UserResponse(UserBase):
    pass
