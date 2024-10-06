from datetime import datetime
from pydantic import BaseModel, EmailStr, constr


class UserBase(BaseModel):
    username: constr(min_length=3, max_length=30, strip_whitespace=True, pattern=r'^[a-zA-Z0-9]+$') # type: ignore
    first_name: constr(min_length=2, max_length=30, strip_whitespace=True, pattern=r'^[a-zA-Z]+$') # type: ignore 
    last_name: constr(min_length=2, max_length=30, strip_whitespace=True, pattern=r'^[a-zA-Z]+$') # type: ignore
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: constr(min_length=8, max_length=30, strip_whitespace=True) # type: ignore


class UserResponse(UserBase):
    created_at: datetime
