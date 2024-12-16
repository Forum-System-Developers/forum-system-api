import unittest

from forum_system_api.services.utils.password_utils import (
    hash_password,
    verify_password,
)


class TestPasswordUtils(unittest.TestCase):

    def test_hashPassword_returnsHashedString(self) -> None:
        # Arrange
        password = "password"

        # Act
        hashed = hash_password(password)

        # Assert
        self.assertIsNotNone(hashed)
        self.assertIsInstance(hashed, str)

    def test_verifyPassword_returnsTrue_whenValidPassword(self) -> None:
        # Arrange
        plain_password = "password"
        hashed_password = hash_password(plain_password)

        # Act
        result = verify_password(plain_password, hashed_password)

        # Assert
        self.assertTrue(result)
