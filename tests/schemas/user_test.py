from unittest import TestCase

from forum_system_api.schemas.user import UserCreate
from tests.services import test_data as td


class TestUserSchemas(TestCase):
    def test_userCreate_raisesValueError_whenPasswordIsInvalid(self) -> None:
        # Arrange
        user_data = td.USER_CREATE.copy()
        user_data['password'] = 'invalid password'
        
        # Act & Assert
        with self.assertRaises(ValueError):
            UserCreate(**user_data)
