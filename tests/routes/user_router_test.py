import unittest
from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session
from fastapi import status
from fastapi.testclient import TestClient

from forum_system_api.main import app
from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.user import User
from forum_system_api.api.api_v1.constants import endpoints as e
from forum_system_api.services.auth_service import get_current_user, require_admin_role
from tests.services import test_data as td


client = TestClient(app)

class TestUserRouter_Should(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_db = MagicMock(spec=Session)
        self.mock_admin = MagicMock(spec=User)
        self.user = MagicMock(spec=User, **td.USER_1)
        self.user2 = MagicMock(spec=User, **td.USER_2)
    
    def tearDown(self) -> None:
        app.dependency_overrides = {}

    @patch('forum_system_api.services.user_service.create')
    def test_registerUser_returns200_onSuccess(self, mock_create) -> None:
        # Arrange
        mock_create.return_value = self.user
        app.dependency_overrides[get_db] = lambda: self.mock_db

        # Act
        response = client.post(e.USERS_REGISTER_ENDPOINT, json=td.USER_CREATE)
        
        # Assert
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    @patch('forum_system_api.api.api_v1.routes.user_router.user_service.get_all')
    def test_getAllUsers_returns200_onSuccess(self, mock_get_all) -> None:
        # Arrange
        mock_get_all.return_value = [self.user, self.user2]
        app.dependency_overrides[get_db] = lambda: self.mock_db
        app.dependency_overrides[require_admin_role] = lambda: self.mock_admin
        
        # Act
        response = client.get(e.USERS_ENDPOINT)
        
        # Assert
        self.assertIsInstance(response.json(), list)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_getCurrentUser_returns200_onSuccess(self) -> None:
        # Arrange
        app.dependency_overrides[get_current_user] = lambda: self.user
        
        # Act
        response = client.get(e.USERS_ME_ENDPOINT)
        
        # Assert
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    @patch('forum_system_api.services.user_service.get_privileged_users')
    def test_viewPrivilegedUsers_returns200_onSuccess(self, mock_get_privileged_users) -> None:
        # Arrange
        permission1 = MagicMock(**td.PERMISSION_1)
        permission2 = MagicMock(**td.PERMISSION_2)

        mock_get_privileged_users.return_value = {self.user: permission1, self.user2: permission2}
        app.dependency_overrides[get_db] = lambda: self.mock_db
        app.dependency_overrides[require_admin_role] = lambda: self.mock_admin
        
        # Act
        response = client.get(e.USERS_PERMISSIONS_LIST_ENDPOINT.format(td.VALID_CATEGORY_ID))
        
        # Assert
        self.assertIsInstance(response.json(), list)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
