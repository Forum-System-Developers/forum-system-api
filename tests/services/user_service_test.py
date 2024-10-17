import unittest
from unittest.mock import MagicMock
from uuid import uuid4

from sqlalchemy.orm import Session

from forum_system_api.persistence.models.user import User
from forum_system_api.services import user_service
from tests.services.test_data import USER_1, USER_2


class UserService_Should(unittest.TestCase):    
    def setUp(self):
        self.mock_db = MagicMock(spec=Session)
        self.user_id = uuid4()
        self.user = User(**USER_1)
        self.user2 = User(**USER_2)

    def test_getAll_returnsAllUsers(self) -> None:
        # Arrange
        query_mock = self.mock_db.query.return_value
        query_mock.all.return_value = [self.user, self.user2]

        # Act
        users = user_service.get_all(self.mock_db)

        # Assert
        self.assertListEqual(users, [self.user, self.user2])
        self.mock_db.query.assert_called_once_with(User)
        query_mock.all.assert_called_once()

    def test_getAll_returnsEmptyList_whenNoUsers(self) -> None:
        # Arrange
        query_mock = self.mock_db.query.return_value
        query_mock.all.return_value = []

        # Act
        users = user_service.get_all(self.mock_db)

        # Assert
        self.assertListEqual(users, list())
        self.mock_db.query.assert_called_once_with(User)
        query_mock.all.assert_called_once()
