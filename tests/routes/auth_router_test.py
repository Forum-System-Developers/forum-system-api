import unittest
from unittest.mock import MagicMock, patch

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.services import test_data as td
from forum_system_api.main import app
from forum_system_api.persistence.models.user import User
from forum_system_api.persistence.database import get_db
from forum_system_api.services.auth_service import (
    oauth2_scheme, 
    get_current_user, 
    require_admin_role
)


AUTH_ENDPOINT = '/api/v1/auth'
AUTH_LOGIN_ENDPOINT = AUTH_ENDPOINT + '/login'
AUTH_LOGOUT_ENDPOINT = AUTH_ENDPOINT + '/logout'
AUTH_REFRESH_ENDPOINT = AUTH_ENDPOINT + '/refresh'
AUTH_REVOKE_ENDPOINT = AUTH_ENDPOINT + '/revoke/{}'


class AuthRouter_Should(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def setUp(self) -> None:
        self.mock_db = MagicMock(spec=Session)
        self.mock_admin = MagicMock(spec=User)
        self.mock_user = MagicMock(spec=User, **td.USER_1)
        self.mock_access_token = 'access_token'
        self.mock_refresh_token = 'refresh_token'
    
    def tearDown(self) -> None:
        app.dependency_overrides = {}
    
    @patch('forum_system_api.services.auth_service.create_access_and_refresh_tokens')
    @patch('forum_system_api.services.auth_service.authenticate_user')
    def test_loginUser_returns200_onSuccess(
        self, 
        mock_authenticate_user, 
        create_access_and_refresh_tokens
    ) -> None:
        # Arrange
        mock_authenticate_user.return_value = self.mock_user
        create_access_and_refresh_tokens.return_value = {
            'access_token': self.mock_access_token,
            'refresh_token': self.mock_refresh_token,
            'token_type': 'bearer'
        }
        app.dependency_overrides[get_db] = lambda: self.mock_db
        
        # Act
        response = self.client.post(AUTH_LOGIN_ENDPOINT, data=td.OAUTH2_PASSWORD_REQUEST_FORM)
        
        # Assert
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    @patch('forum_system_api.services.auth_service.update_token_version')
    def test_logoutUser_returns200_onSuccess(self, mock_update_token_version) -> None:
        # Arrange
        app.dependency_overrides[get_current_user] = lambda: self.mock_user
        app.dependency_overrides[get_db] = lambda: self.mock_db
        
        # Act
        response = self.client.post(AUTH_LOGOUT_ENDPOINT)
        
        # Assert
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    @patch('forum_system_api.services.auth_service.refresh_access_token')
    def test_refreshToken_returns200_onSuccess(self, mock_refresh_access_token) -> None:
        # Arrange
        mock_refresh_access_token.return_value = self.mock_access_token
        app.dependency_overrides[get_db] = lambda: self.mock_db
        app.dependency_overrides[oauth2_scheme] = lambda: self.mock_refresh_token
        
        # Act
        response = self.client.post(AUTH_REFRESH_ENDPOINT, data={'refresh_token': self.mock_refresh_token})
        
        # Assert
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    @patch('forum_system_api.services.auth_service.update_token_version')
    def test_revokeToken_returns200_onSuccess(self, mock_update_token_version) -> None:
        # Arrange
        app.dependency_overrides[require_admin_role] = lambda: self.mock_admin
        app.dependency_overrides[get_db] = lambda: self.mock_db
        
        # Act
        response = self.client.put(AUTH_REVOKE_ENDPOINT.format(self.mock_user.id))
        
        # Assert
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
