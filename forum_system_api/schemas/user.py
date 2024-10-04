from pydantic import BaseModel, EmailStr

from .validators import Password, Username, Name


class UserBase(BaseModel):
    username: Username
    first_name: Name
    last_name: Name
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: Password


class UserResponse(UserBase):
    pass
