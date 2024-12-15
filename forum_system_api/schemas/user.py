import re
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator

from forum_system_api.persistence.models.user import User
from forum_system_api.persistence.models.user_category_permission import (
    UserCategoryPermission,
)
from forum_system_api.schemas.category_permission import UserCategoryPermissionResponse

PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,30}$"


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
    first_name: str = Field(
        min_length=2,
        max_length=30,
        pattern=r"^[a-zA-Z]+(?:-[a-zA-Z]+)*$",
        examples=["First Name"],
    )
    last_name: str = Field(
        min_length=2,
        max_length=30,
        pattern=r"^[a-zA-Z]+(?:-[a-zA-Z]+)*$",
        examples=["Last Name"],
    )
    email: EmailStr

    class Config:
        from_attributes = True

    @field_validator("username", "first_name", "last_name", mode="before")
    def strip_whitespace(cls, value: str) -> str:
        return value.strip()


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=30, examples=["ExamplePassword1!"])

    @field_validator("password", mode="before")
    def strip_whitespace(cls, value: str) -> str:
        return value.strip()

    @field_validator("password")
    def check_password(cls, password):
        if not re.match(PASSWORD_REGEX, password):
            raise ValueError(
                "Password must contain at least one lowercase letter, \
                one uppercase letter, one digit, one special character(@$!%*?&), \
                and be between 8 and 30 characters long."
            )
        return password


class UserResponse(UserBase):
    id: UUID
    created_at: datetime


class UserPermissionsResponse(UserResponse):
    permissions: list[UserCategoryPermissionResponse]

    @classmethod
    def create_response(
        cls, user: User, permissions: list[UserCategoryPermission]
    ) -> "UserPermissionsResponse":
        return cls(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            created_at=user.created_at,
            permissions=[
                UserCategoryPermissionResponse(
                    category_id=permission.category_id,
                    access_level=permission.access_level,
                )
                for permission in permissions
            ],
        )
