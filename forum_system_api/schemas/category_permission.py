from uuid import UUID

from pydantic import BaseModel

from forum_system_api.persistence.models.access_level import AccessLevel


class CategoryPermissionResponse(BaseModel):
    category_id: UUID
    access_level: AccessLevel

    class Config:
        orm_mode = True


class DetailedCategoryPermissionResponse(CategoryPermissionResponse):
    user_id: UUID
