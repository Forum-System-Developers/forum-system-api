from datetime import datetime
from pydantic import BaseModel, EmailStr, constr

from forum_system_api.persistence.models.category_permission import CategoryPermission
from forum_system_api.persistence.models.user import User
from forum_system_api.schemas.category_permission import CategoryPermissionResponse


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


class UserPermissionsResponse(UserResponse):
    permissions: list[CategoryPermissionResponse]

    @classmethod
    def create_response(
        cls, 
        user: User, 
        permissions: list[CategoryPermission]
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
