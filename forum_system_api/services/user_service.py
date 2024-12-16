import logging
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from forum_system_api.persistence.models.access_level import AccessLevel
from forum_system_api.persistence.models.admin import Admin
from forum_system_api.persistence.models.category import Category
from forum_system_api.persistence.models.user import User
from forum_system_api.persistence.models.user_category_permission import (
    UserCategoryPermission,
)
from forum_system_api.schemas.user import UserCreate
from forum_system_api.services import category_service
from forum_system_api.services.utils.password_utils import hash_password

logger = logging.getLogger(__name__)


def get_all(db: Session) -> list[User]:
    """
    Retrieve all User records from the database.

    Args:
        db (Session): The database session used to query the User records.

    Returns:
        list[User]: A list of all User records in the database.
    """
    users = db.query(User).all()
    logger.info("Retrieved all users from the database")

    return users


def get_by_id(user_id: UUID, db: Session) -> User | None:
    """
    Retrieve a user by their unique identifier.

    Args:
        user_id (UUID): The unique identifier of the user.
        db (Session): The database session to use for the query.

    Returns:
        Optional[User]: The user object if found, otherwise None.
    """
    user = db.query(User).filter(User.id == user_id).first()
    logger.warning(f"Retrieved user with ID: {user_id} from the database or None")

    return user


def get_by_username(username: str, db: Session) -> Optional[User]:
    """
    Retrieve a user by their username.

    Args:
        username (str): The username of the user to retrieve.
        db (Session): The database session to use for the query.

    Returns:
        Optional[User]: The user object if found, otherwise None.
    """
    user = db.query(User).filter(User.username == username).first()
    logger.warning(
        f"Retrieved user with username: {username} from the database or None"
    )

    return user


def get_by_email(email: str, db: Session) -> Optional[User]:
    """
    Retrieve a user by their email address.

    Args:
        email (str): The email address of the user to retrieve.
        db (Session): The database session to use for the query.

    Returns:
        Optional[User]: The user object if found, otherwise None.
    """
    user = db.query(User).filter(User.email == email).first()
    logger.warning(f"Retrieved user with email: {email} from the database or None")

    return user


def create(user_data: UserCreate, db: Session) -> User:
    """
    Creates a new user in the database.
    This function ensures that the provided username and email are unique,
    hashes the user's password, and then creates a new user record in the
    database.

    Args:
        user_data (UserCreate): An instance containing the user's data.
        db (Session): The database session to use for the operation.

    Returns:
        User: The newly created user object.
    """
    ensure_unique_username_and_email(
        username=user_data.username, email=str(user_data.email), db=db
    )
    logger.info("Ensured that the username and email are unique")

    hashed_password = hash_password(user_data.password)

    user = User(
        password_hash=hashed_password, **user_data.model_dump(exclude={"password"})
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info(f"Created a new user with ID: {user.id}")

    return user


def is_admin(user_id: UUID, db: Session) -> bool:
    """
    Checks if a user is an admin.

    Args:
        user_id (UUID): The unique identifier of the user.
        db (Session): The database session to use for the query.

    Returns:
        bool: True if the user is an admin, False otherwise.
    """
    is_admin = (db.query(Admin).filter(Admin.user_id == user_id).first()) is not None
    logger.info(f"Checked if user with ID {user_id} is an admin")

    return is_admin


def get_privileged_users(
    category_id: UUID, db: Session
) -> dict[User, UserCategoryPermission]:
    """
    Retrieve privileged users for a given category.

    Args:
        category_id (UUID): The unique identifier of the category.
        db (Session): The database session.

    Returns:
        dict[User, UserCategoryPermission]: A dictionary mapping users to their permissions in the category.

    Raises:
        HTTPException: If the category is not found or if the category is not private.
    """
    category = category_service.get_by_id(category_id=category_id, db=db)
    if category is None:
        logger.error(f"Category with ID {category_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    logger.info(f"Retrieved category with ID: {category_id}")

    if not category.is_private:
        logger.error(f"Category with ID {category_id} is not private")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Category is not private"
        )

    privileged_users = {
        permission.user: permission for permission in category.permissions
    }
    logger.info(f"Retrieved privileged users for category with ID: {category_id}")

    return privileged_users


def get_user_permissions(user_id: UUID, db: Session) -> list[UserCategoryPermission]:
    """
    Retrieve the permissions of a user by their user ID.

    Args:
        user_id (UUID): The unique identifier of the user.
        db (Session): The database session used to query the user.

    Returns:
        list[UserCategoryPermission]: A list of permissions associated with the user.

    Raises:
        HTTPException: If the user is not found, an HTTP 404 exception is raised.
    """
    user = get_by_id(user_id=user_id, db=db)
    if user is None:
        logger.error(f"User with ID {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    permission = user.permissions
    logger.info(f"Retrieved permissions for user with ID: {user_id}")

    return permission


def revoke_access(user_id: UUID, category_id: UUID, db: Session) -> bool:
    """
    Revokes a user's access to a specific category.

    Args:
        user_id (UUID): The unique identifier of the user.
        category_id (UUID): The unique identifier of the category.
        db (Session): The database session.

    Returns:
        bool: True if the access was successfully revoked.

    Raises:
        HTTPException: If the permission is not found.
    """
    _, _, permission = get_user_category_permission(
        user_id=user_id, category_id=category_id, db=db
    )

    if permission is None:
        logger.error(
            f"Permission for user with ID {user_id} in category with ID {category_id} not found"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found"
        )
    logger.info(
        f"Revoking access for user with ID {user_id} in category with ID {category_id}"
    )

    db.delete(permission)
    db.commit()
    logger.info(
        f"Revoked access for user with ID {user_id} in category with ID {category_id}"
    )

    return True


def update_access_level(
    user_id: UUID, category_id: UUID, access_level: AccessLevel, db: Session
) -> UserCategoryPermission:
    """
    Updates the access level of a user for a specific category. If the user does not
    already have a permission entry for the category, a new one is created.

    Args:
        user_id (UUID): The unique identifier of the user.
        category_id (UUID): The unique identifier of the category.
        access_level (AccessLevel): The new access level to be set for the user.
        db (Session): The database session to use for the operation.

    Returns:
        UserCategoryPermission: The updated or newly created user category permission.
    """
    _, category, permission = get_user_category_permission(
        user_id=user_id, category_id=category_id, db=db
    )

    if permission is None:
        permission = UserCategoryPermission(
            user_id=user_id, category_id=category_id, access_level=access_level
        )
        category.permissions.append(permission)
        logger.info(
            f"Created new permission for user with ID {user_id} in category with ID {category_id}"
        )
    else:
        permission.access_level = access_level
        logger.info(
            f"Updated permission for user with ID {user_id} in category with ID {category_id}"
        )

    db.commit()
    db.refresh(permission)
    logger.info(
        f"Committed and refreshed permission for user with ID {user_id} in category with ID {category_id}"
    )

    return permission


def get_user_category_permission(
    user_id: UUID, category_id: UUID, db: Session
) -> tuple[User, Category, Optional[UserCategoryPermission]]:
    """
    Retrieve the user, category, and the user's permission for the specified category.

    Args:
        user_id (UUID): The unique identifier of the user.
        category_id (UUID): The unique identifier of the category.
        db (Session): The database session.

    Returns:
        tuple[User, Category, Optional[UserCategoryPermission]]: A tuple containing the user, category,
        and the user's permission for the category, if any.

    Raises:
        HTTPException: If the user or category is not found.
    """
    user = get_by_id(user_id=user_id, db=db)
    if user is None:
        logger.error(f"User with ID {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    logger.info(f"Retrieved user with ID: {user_id}")

    category = category_service.get_by_id(category_id=category_id, db=db)
    if category is None:
        logger.error(f"Category with ID {category_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    logger.info(f"Retrieved category with ID: {category_id}")

    permission = next((p for p in category.permissions if p.user_id == user_id), None)
    logger.info(
        f"Retrieved permission for user with ID {user_id} in category with ID {category_id}"
    )

    return user, category, permission


def ensure_unique_username_and_email(username: str, email: str, db: Session) -> None:
    """
    Ensures that the provided username and email are unique in the database.

    Args:
        username (str): The username to check for uniqueness.
        email (str): The email to check for uniqueness.
        db (Session): The database session to use for the queries.

    Raises:
        HTTPException: If the username already exists, raises an exception with status code 409 and detail "Username already exists".
        HTTPException: If the email already exists, raises an exception with status code 409 and detail "Email already exists".
    """
    if get_by_username(username, db) is not None:
        logger.error(f"Username {username} already exists")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already exists"
        )
    logger.info(f"Ensured that the username {username} is unique")

    if get_by_email(email, db) is not None:
        logger.error(f"Email {email} already exists")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
        )
