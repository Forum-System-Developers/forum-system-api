from datetime import datetime, timedelta
from uuid import UUID, uuid4

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from forum_system_api.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_DAYS,
    SECRET_KEY,
)
from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.user import User
from forum_system_api.services import user_service
from forum_system_api.services.user_service import is_admin
from forum_system_api.services.utils.password_utils import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def create_access_token(data: dict) -> str:
    """
    Generates an access token with the given data and an expiration time.

    Args:
        data (dict): The data to be included in the token payload.

    Returns:
        str: The generated access token as a string.
    """
    return create_token(
        data=data, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )


def create_refresh_token(data: dict) -> str:
    """
    Generates a refresh token with the provided data and a predefined expiration time.

    Args:
        data (dict): The data to be included in the refresh token.

    Returns:
        str: The generated refresh token as a string.
    """
    return create_token(
        data=data, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )


def create_token(data: dict, expires_delta: timedelta) -> str:
    """
    Creates a JSON Web Token (JWT) with the given data and expiration delta.

    Args:
        data (dict): The payload data to include in the token.
        expires_delta (timedelta): The time duration after which the token will expire.

    Returns:
        str: The encoded JWT as a string.

    Raises:
        HTTPException: If there is an error in creating the token.
    """
    try:
        payload = data.copy()
        expire = datetime.now() + expires_delta
        payload.update({"exp": expire})
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create token",
        )


def create_access_and_refresh_tokens(user: User, db: Session) -> dict:
    """
    Generates access and refresh tokens for a given user.

    Args:
        user (User): The user object for whom the tokens are being created.
        db (Session): The database session used to update the token version.

    Returns:
        dict: A dictionary containing the access token, refresh token, and token type.
    """
    token_version = update_token_version(user=user, db=db)
    token_data = {
        "sub": str(user.id),
        "token_version": str(token_version),
        "is_admin": "true" if is_admin(user_id=user.id, db=db) else "false",
    }
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


def refresh_access_token(refresh_token: str, db: Session) -> str:
    """
    Refreshes the access token using the provided refresh token.

    Args:
        refresh_token (str): The refresh token used to generate a new access token.
        db (Session): The database session used for token verification.

    Returns:
        str: A new access token.
    """
    payload = verify_token(token=refresh_token, db=db)
    user_id = payload.get("sub")
    token_version = payload.get("token_version")

    return create_access_token({"sub": user_id, "token_version": token_version})


def verify_token(token: str, db: Session) -> dict:
    """
    Verifies the provided JWT token and returns the payload if valid.

    Args:
        token (str): The JWT token to be verified.
        db (Session): The database session to use for querying user information.

    Returns:
        dict: The decoded payload from the JWT token if verification is successful.

    Raises:
        HTTPException: If the token cannot be verified or if the user associated with the token cannot be found or has an invalid token version.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not verify token"
        )

    user_id = UUID(payload.get("sub"))
    token_version = UUID(payload.get("token_version"))
    user = user_service.get_by_id(user_id=user_id, db=db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not verify token"
        )
    if user.token_version != token_version:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not verify token"
        )

    return payload


def update_token_version(user: User, db: Session) -> UUID:
    """
    Updates the token version for a given user.

    Args:
        user (User): The user whose token version is to be updated.
        db (Session): The database session to use for committing the changes.

    Returns:
        UUID: The new token version of the user.

    Raises:
        HTTPException: If the user is not found.
    """
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user.token_version = uuid4()
    db.commit()
    db.refresh(user)

    return user.token_version


def authenticate_user(username: str, password: str, db: Session) -> User:
    """
    Authenticate a user by their username and password.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.
        db (Session): The database session.

    Returns:
        User: The authenticated user object.

    Raises:
        HTTPException: If the user cannot be authenticated due to incorrect username or password.
    """
    user = user_service.get_by_username(username=username, db=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not authenticate user",
        )

    verified_password = verify_password(password, user.password_hash)
    if not verified_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not authenticate user",
        )

    return user


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """
    Retrieve the current user based on the provided token.

    Args:
        token (str): The authentication token provided by the user.
        db (Session): The database session dependency.

    Returns:
        User: The user object corresponding to the token.

    Raises:
        HTTPException: If the token is invalid or the user does not exist.
    """
    token_data = verify_token(token=token, db=db)
    user_id = token_data.get("sub")
    user = user_service.get_by_id(user_id=user_id, db=db)

    return user


def require_admin_role(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> User:
    """
    Dependency that ensures the current user has an admin role.

    Args:
        user (User): The current user, obtained from the `get_current_user` dependency.
        db (Session): The database session, obtained from the `get_db` dependency.

    Returns:
        User: The current user if they have an admin role.

    Raises:
        HTTPException: If the current user does not have an admin role, with a 403 Forbidden status code.
    """
    is_admin = user_service.is_admin(user_id=user.id, db=db)

    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )

    return user
