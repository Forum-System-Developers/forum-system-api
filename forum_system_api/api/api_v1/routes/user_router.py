from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.access_level import AccessLevel
from forum_system_api.persistence.models.user import User
from forum_system_api.schemas.category_permission import UserCategoryPermissionResponse
from forum_system_api.services import user_service
from forum_system_api.services.auth_service import get_current_user, require_admin_role
from forum_system_api.schemas.user import UserCreate, UserPermissionsResponse, UserResponse


router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/register', 
    response_model=UserResponse, 
    status_code=status.HTTP_201_CREATED, 
    description='Create a new user account with username, first name, last name, email, and password.'
)
def register_user(
    user_data: UserCreate, 
    db: Session = Depends(get_db)
) -> UserResponse:
    return user_service.create(user_data=user_data, db=db)


@router.get(
    '/me', 
    response_model=UserResponse, 
    description='Retrieve the current user\'s information.'
)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    return current_user


@router.get(
    '/', 
    response_model=list[UserResponse], 
    description='Retrieve a list of all user accounts. Admin privileges required.'
)
def get_all_users(
    admin: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
) -> list[UserResponse]:
    return user_service.get_all(db)


@router.get(
    '/permissions/{category_id}', 
    response_model=list[UserPermissionsResponse], 
    description='Get users with access to a specific category by category_id. Admin privileges required.'
)
def view_privileged_users(
    category_id: UUID = Path(..., description='The unique identifier of the category'), 
    admin: User = Depends(require_admin_role), 
    db: Session = Depends(get_db)
) -> list[UserPermissionsResponse]:
    privileged_users = user_service.get_privileged_users(category_id=category_id, db=db)
    return [
        UserPermissionsResponse.create_response(user, [permission])
        for user, permission in privileged_users.items()
    ]


@router.get(
    '/{user_id}/permissions', 
    response_model=UserPermissionsResponse, 
    description='Get the permissions of a user by user_id. Admin privileges required.'
)
def view_user_permissions(
    user_id: UUID = Path(..., description='The unique identifier of the user'),
    admin: User = Depends(require_admin_role), 
    db: Session = Depends(get_db)
) -> UserPermissionsResponse:
    user = user_service.get_by_id(user_id=user_id, db=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='User not found'
        )
    return UserPermissionsResponse.create_response(user, user.permissions)


@router.put(
    '/{user_id}/permissions/{category_id}/read', 
    response_model=UserCategoryPermissionResponse, 
    description='Grant a user read access to a category by user_id and category_id. Requires admin privileges.'
)
def grant_user_read_access(
    user_id: UUID = Path(..., description='The unique identifier of the user'), 
    category_id: UUID = Path(..., description='The unique identifier of the category'), 
    admin: User = Depends(require_admin_role), 
    db: Session = Depends(get_db)
) -> UserCategoryPermissionResponse:
    return user_service.update_access_level(
        user_id=user_id, 
        category_id=category_id, 
        access_level=AccessLevel.READ, 
        db=db
    )


@router.put(
    '/{user_id}/permissions/{category_id}/write', 
    response_model=UserCategoryPermissionResponse, 
    description='Grant a user write access to a category by user_id and category_id. Requires admin privileges.'
)
def grant_user_write_access(
    user_id: UUID = Path(..., description='The unique identifier of the user'), 
    category_id: UUID = Path(..., description='The unique identifier of the category'), 
    admin: User = Depends(require_admin_role), 
    db: Session = Depends(get_db)
) -> UserCategoryPermissionResponse:
    return user_service.update_access_level(
        user_id=user_id, 
        category_id=category_id, 
        access_level=AccessLevel.WRITE, 
        db=db
    )


@router.delete(
    '/{user_id}/permissions/{category_id}', 
    description='Revoke user access for a specific category by user_id and category_id. Admin privileges required.'
)
def revoke_user_access(
    user_id: UUID = Path(..., description='The unique identifier of the user'), 
    category_id: UUID = Path(..., description='The unique identifier of the category'), 
    admin: User = Depends(require_admin_role), 
    db: Session = Depends(get_db)
) -> dict:
    if user_service.revoke_access(user_id=user_id, category_id=category_id, db=db):
        return {'message': 'Access revoked'}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='User does not have access to this category'
        )
