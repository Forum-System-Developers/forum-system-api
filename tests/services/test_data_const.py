from uuid import uuid4
from datetime import datetime, timezone


VALID_USER_ID = uuid4()
VALID_USERNAME = "testuser"
VALID_PASSWORD = "password"
VALID_PASSWORD_HASH = "hashed_password"
VALID_EMAIL = "test_user@test.com"
VALID_FIRST_NAME = "Test"
VALID_LAST_NAME = "User"
VALID_TOKEN_VERSION = uuid4()
VALID_CREATED_AT = datetime.now(timezone.utc)


VALID_USER_ID_2 = uuid4()
VALID_USERNAME_2 = "testuser2"
VALID_PASSWORD_HASH_2 = "hashed_password2"
VALID_EMAIL_2 = "test_user@test.com"
VALID_FIRST_NAME_2 = "Test"
VALID_LAST_NAME_2 = "User"
VALID_TOKEN_VERSION_2 = uuid4()
VALID_CREATED_AT_2 = datetime.now(timezone.utc)


VALID_TOPIC_ID_1 = uuid4()
VALID_TOPIC_TITLE_1 = "Test Topic"
VALID_TOPIC_IS_LOCKED_1 = False
VALID_TOPIC_CREATED_AT_1 = datetime.now(timezone.utc)
VALID_AUTHOR_ID_1 = uuid4()
VALID_CATEGORY_ID_1 = uuid4()
VALID_BEST_REPLY_ID_2 = uuid4() 


VALID_TOPIC_ID_2 = uuid4()
VALID_TOPIC_TITLE_2 = "Test Topic 2"
VALID_TOPIC_IS_LOCKED_2 = False
VALID_TOPIC_CREATED_AT_2 = datetime.now(timezone.utc)
VALID_AUTHOR_ID_2 = uuid4()
VALID_CATEGORY_ID_2 = uuid4()
VALID_BEST_REPLY_ID_2 = uuid4()

