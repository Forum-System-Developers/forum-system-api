from datetime import datetime
import re
from pydantic import BaseModel, EmailStr, Field, field_validator

from forum_system_api.schemas.custom_types import Username, Name, Password
from forum_system_api.persistence.models.user import User
from forum_system_api.persistence.models.user_category_permission import UserCategoryPermission
from forum_system_api.schemas.category_permission import UserCategoryPermissionResponse


PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,30}$'

class UserBase(BaseModel):
    username: Username
    first_name: Name
    last_name: Name
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: Password

    @field_validator('password')
    def check_password(cls, password):
        if not re.match(PASSWORD_REGEX, password):
            raise ValueError(
                'Password must contain at least one lowercase letter, \
                one uppercase letter, one digit, one special character(@$!%*?&), \
                and be between 8 and 30 characters long.')
        return password


class UserResponse(UserBase):
    created_at: datetime


class UserPermissionsResponse(UserResponse):
    permissions: list[UserCategoryPermissionResponse]

    @classmethod
    def create_response(
        cls, 
        user: User, 
        permissions: list[UserCategoryPermission]
    ) -> dict:
        return cls(
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            created_at=user.created_at,
            permissions=[
                {
                    "category_id": permission.category_id,
                    "access_level": permission.access_level
                }
                for permission in permissions
            ]
        )
