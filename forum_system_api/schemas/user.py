from pydantic import BaseModel, EmailStr

from .validators import PasswordType, UsernameType, NameType


class UserBase(BaseModel):
    username: UsernameType
    first_name: NameType
    last_name: NameType
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: PasswordType


class UserResponse(UserBase):
    pass
