from uuid import UUID

from pydantic import BaseModel

from forum_system_api.persistence.models.access_level import AccessLevel


class UserCategoryPermissionResponse(BaseModel):
    category_id: UUID
    access_level: AccessLevel

    class Config:
        from_attributes = True


class DetailedUserCategoryPermissionResponse(UserCategoryPermissionResponse):
    user_id: UUID
