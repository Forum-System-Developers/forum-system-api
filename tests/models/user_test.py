from unittest import TestCase
from unittest.mock import MagicMock

from forum_system_api.persistence.models.user import User
from tests.services.test_data import USER_1, USER_2


class TestUserSchemas(TestCase):
    
    def test_userEquality_returnsFalse_whenUsersAreNotEqual(self) -> None:
        # Arrange
        user1 = User(**USER_1)
        user2 = User(**USER_2)

        # Act & Assert
        self.assertNotEqual(user1, user2)
    
    def test_userEquality_returnsFalse_whenOtherIsNotUser(self) -> None:    
        # Arrange
        user = User(**USER_1)
        other = MagicMock()

        # Act & Assert
        self.assertNotEqual(user, other)

    def test_conversationsProperty_returnsAllConversations(self) -> None:
        # Arrange
        user = User()
        user.conversations_as_user1 = [MagicMock(), MagicMock()]
        user.conversations_as_user2 = [MagicMock()]

        # Act
        conversations = user.conversations

        # Assert
        self.assertEqual(3, len(conversations))
        self.assertEqual(conversations, user.conversations_as_user1 + user.conversations_as_user2)
