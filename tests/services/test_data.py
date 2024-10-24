from uuid import uuid4
from datetime import datetime, timezone

from forum_system_api.persistence.models.access_level import AccessLevel


VALID_USER_ID = uuid4()
VALID_USERNAME = "testuser"
VALID_PASSWORD = "Password1!"
VALID_PASSWORD_HASH = "hashed_password"
VALID_EMAIL = "test_user@test.com"
VALID_FIRST_NAME = "Test"
VALID_LAST_NAME = "User"
VALID_TOKEN_VERSION = uuid4()
VALID_CREATED_AT = datetime.now(timezone.utc)

USER_1 = {
    "id": VALID_USER_ID,
    "username": VALID_USERNAME,
    "password_hash": VALID_PASSWORD_HASH,
    "email": VALID_EMAIL,
    "first_name": VALID_FIRST_NAME,
    "last_name": VALID_LAST_NAME,
    "token_version": VALID_TOKEN_VERSION,
    "created_at": VALID_CREATED_AT
}

VALID_USER_ID_2 = uuid4()
VALID_USERNAME_2 = "testuser2"
VALID_PASSWORD_HASH_2 = "hashed_password2"
VALID_EMAIL_2 = "test_user@test.com"
VALID_FIRST_NAME_2 = "Test"
VALID_LAST_NAME_2 = "User"
VALID_TOKEN_VERSION_2 = uuid4()
VALID_CREATED_AT_2 = datetime.now(timezone.utc)

USER_2 = {
    "id": VALID_USER_ID_2,
    "username": VALID_USERNAME_2,
    "password_hash": VALID_PASSWORD_HASH_2,
    "email": VALID_EMAIL_2,
    "first_name": VALID_FIRST_NAME_2,
    "last_name": VALID_LAST_NAME_2,
    "token_version": VALID_TOKEN_VERSION_2,
    "created_at": VALID_CREATED_AT_2
}

USER_CREATE = {
    "username": VALID_USERNAME, 
    "password": VALID_PASSWORD,
    "email": VALID_EMAIL,
    "first_name": VALID_FIRST_NAME,
    "last_name": VALID_LAST_NAME
}

VALID_CATEGORY_ID = uuid4()
VALID_CATEGORY_NAME = "Category 1"
VALID_IS_PRIVATE = False
VALID_IS_LOCKED = False
VALID_CREATED_AT = datetime.now(timezone.utc)

CATEGORY_1 = {
    "id": VALID_CATEGORY_ID,
    "name": VALID_CATEGORY_NAME,
    "is_private": VALID_IS_PRIVATE,
    "is_locked": VALID_IS_LOCKED,
    "created_at": VALID_CREATED_AT
}

VALID_CATEGORY_ID_2 = uuid4()
VALID_CATEGORY_NAME_2 = "Category 2"
VALID_IS_PRIVATE_2 = True
VALID_IS_LOCKED_2 = True
VALID_CREATED_AT_2 = datetime.now(timezone.utc)

CATEGORY_2 = {
    "id": VALID_CATEGORY_ID_2,
    "name": VALID_CATEGORY_NAME_2,
    "is_private": VALID_IS_PRIVATE_2,
    "is_locked": VALID_IS_LOCKED_2,
    "created_at": VALID_CREATED_AT_2
}

CATEGORY_CREATE = {
    "name": "New Category", 
    "is_private": False, 
    "is_locked":False
}

VALID_MESSAGE_ID = uuid4()
VALID_CONTENT = "Hello, this is a test message."
VALID_AUTHOR_ID = uuid4()
VALID_CONVERSATION_ID = uuid4()
VALID_CREATED_AT = datetime.now(timezone.utc)

MESSAGE_1 = {
    "id": VALID_MESSAGE_ID,
    "content": VALID_CONTENT,
    "author_id": VALID_AUTHOR_ID,
    "conversation_id": VALID_CONVERSATION_ID,
    "created_at": VALID_CREATED_AT
}

MESSAGE_CREATE = {
    "content": "Hello", 
    "receiver_id": str(VALID_USER_ID)
}

PERMISSION_1 = {
    "user_id": VALID_USER_ID,
    "category_id": VALID_CATEGORY_ID,
    "access_level": AccessLevel.READ.value
}

PERMISSION_2 = {
    "user_id": VALID_USER_ID_2,
    "category_id": VALID_CATEGORY_ID,
    "access_level": AccessLevel.WRITE.value
}

OAUTH2_PASSWORD_REQUEST_FORM = {
    "grant_type": "password",
    "username": VALID_USERNAME,
    "password": VALID_PASSWORD
}
