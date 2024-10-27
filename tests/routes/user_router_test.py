from unittest import TestCase
from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session
from fastapi import status
from fastapi.testclient import TestClient

from forum_system_api.main import app
from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.user import User
from forum_system_api.services.auth_service import get_current_user, require_admin_role
from tests.services import test_data as td


USERS_ENDPOINT = '/api/v1/users'
USERS_ME_ENDPOINT = USERS_ENDPOINT + '/me'
USERS_REGISTER_ENDPOINT = USERS_ENDPOINT + '/register'
USERS_PERMISSIONS_LIST_ENDPOINT = USERS_ENDPOINT + '/permissions/{}'
USERS_PERMISSIONS_DETAIL_ENDPOINT = USERS_ENDPOINT + '/{}/permissions'
USERS_GRANT_READ_PERMISSION_ENDPOINT = USERS_ENDPOINT + '/{}/permissions/{}/read'
USERS_GRANT_WRITE_PERMISSION_ENDPOINT = USERS_ENDPOINT + '/{}/permissions/{}/write'
USERS_REVOKE_PERMISSION_ENDPOINT = USERS_ENDPOINT + '/{}/permissions/{}'


class TestUserRouter_Should(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def setUp(self) -> None:
        self.mock_db = MagicMock(spec=Session)
        self.mock_admin = MagicMock(spec=User)
        self.mock_user = MagicMock(spec=User, **td.USER_1)
        self.mock_user2 = MagicMock(spec=User, **td.USER_2)
    
    def tearDown(self) -> None:
        app.dependency_overrides = {}

    @patch('forum_system_api.services.user_service.create')
    def test_registerUser_returns200_onSuccess(self, mock_create) -> None:
        # Arrange
        mock_create.return_value = self.mock_user
        app.dependency_overrides[get_db] = lambda: self.mock_db

        # Act
        response = self.client.post(USERS_REGISTER_ENDPOINT, json=td.USER_CREATE)
        
        # Assert
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    @patch('forum_system_api.api.api_v1.routes.user_router.user_service.get_all')
    def test_getAllUsers_returns200_onSuccess(self, mock_get_all) -> None:
        # Arrange
        mock_get_all.return_value = [self.mock_user, self.mock_user2]
        app.dependency_overrides[get_db] = lambda: self.mock_db
        app.dependency_overrides[require_admin_role] = lambda: self.mock_admin
        
        # Act
        response = self.client.get(USERS_ENDPOINT)
        
        # Assert
        self.assertIsInstance(response.json(), list)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_getCurrentUser_returns200_onSuccess(self) -> None:
        # Arrange
        app.dependency_overrides[get_current_user] = lambda: self.mock_user
        
        # Act
        response = self.client.get(USERS_ME_ENDPOINT)
        
        # Assert
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    @patch('forum_system_api.services.user_service.get_privileged_users')
    def test_viewPrivilegedUsers_returns200_onSuccess(self, mock_get_privileged_users) -> None:
        # Arrange
        permission1 = MagicMock(**td.PERMISSION_1)
        permission2 = MagicMock(**td.PERMISSION_2)

        mock_get_privileged_users.return_value = {self.mock_user: permission1, self.mock_user2: permission2}
        app.dependency_overrides[get_db] = lambda: self.mock_db
        app.dependency_overrides[require_admin_role] = lambda: self.mock_admin
        
        # Act
        response = self.client.get(USERS_PERMISSIONS_LIST_ENDPOINT.format(td.VALID_CATEGORY_ID))
        
        # Assert
        self.assertIsInstance(response.json(), list)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    @patch('forum_system_api.services.user_service.get_by_id')
    def test_viewUserPermissions_returns200_onSuccess(self, mock_get_by_id) -> None:
        # Arrange
        mock_get_by_id.return_value = self.mock_user
        app.dependency_overrides[get_db] = lambda: self.mock_db
        app.dependency_overrides[require_admin_role] = lambda: self.mock_admin
        
        # Act
        response = self.client.get(USERS_PERMISSIONS_DETAIL_ENDPOINT.format(td.VALID_USER_ID))
        
        # Assert
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    @patch('forum_system_api.services.user_service.get_by_id')
    def test_viewUserPermissions_returns404_whenUserNotFound(self, mock_get_by_id) -> None:
        # Arrange
        mock_get_by_id.return_value = None
        app.dependency_overrides[get_db] = lambda: self.mock_db
        app.dependency_overrides[require_admin_role] = lambda: self.mock_admin
        
        # Act
        response = self.client.get(USERS_PERMISSIONS_DETAIL_ENDPOINT.format(td.VALID_USER_ID))
        
        # Assert
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    @patch('forum_system_api.services.user_service.update_access_level')
    def test_grantReadPermission_returns200_onSuccess(self, mock_update_access_level) -> None:
        # Arrange
        mock_update_access_level.return_value = td.PERMISSION_1
        app.dependency_overrides[get_db] = lambda: self.mock_db
        app.dependency_overrides[require_admin_role] = lambda: self.mock_admin
        
        # Act
        response = self.client.put(USERS_GRANT_READ_PERMISSION_ENDPOINT.format(td.VALID_USER_ID, td.VALID_CATEGORY_ID))
        
        # Assert
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    @patch('forum_system_api.services.user_service.update_access_level')
    def test_grantWritePermission_returns200_onSuccess(self, mock_update_access_level) -> None:
        # Arrange
        mock_update_access_level.return_value = td.PERMISSION_1
        app.dependency_overrides[get_db] = lambda: self.mock_db
        app.dependency_overrides[require_admin_role] = lambda: self.mock_admin
        
        # Act
        response = self.client.put(USERS_GRANT_WRITE_PERMISSION_ENDPOINT.format(td.VALID_USER_ID, td.VALID_CATEGORY_ID))
        
        # Assert
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    @patch('forum_system_api.services.user_service.revoke_access')
    def test_revokeUserAccess_returns200_onSuccess(self, mock_revoke_access) -> None:
        # Arrange
        mock_revoke_access.return_value = True
        app.dependency_overrides[get_db] = lambda: self.mock_db
        app.dependency_overrides[require_admin_role] = lambda: self.mock_admin
        
        # Act
        response = self.client.delete(USERS_REVOKE_PERMISSION_ENDPOINT.format(td.VALID_USER_ID, td.VALID_CATEGORY_ID))
        
        # Assert
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
