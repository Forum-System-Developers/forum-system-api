import unittest
from unittest.mock import MagicMock, patch
from datetime import timedelta
from uuid import uuid4

from fastapi import HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session

from forum_system_api.persistence.models.user import User
from forum_system_api.services import auth_service
from tests.services.test_data import USER_1, VALID_PASSWORD


class AuthService_Should(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock(spec=Session)
        self.user = User(**USER_1)
        self.mock_access_token = 'access_token'
        self.mock_refresh_token = 'refresh_token'
        self.payload = {
            'sub': str(self.user.id), 
            'token_version': str(self.user.token_version), 
            'is_admin': False
        }
    
    @patch('forum_system_api.services.auth_service.create_token')
    def test_createAccessToken_returnsToken(self, mock_create_token) -> None:
        # Arrange
        mock_create_token.return_value = self.mock_access_token
        
        # Act
        token = auth_service.create_access_token(data={})
        
        # Assert
        self.assertEqual(self.mock_access_token, token)

    @patch('forum_system_api.services.auth_service.create_token')
    def test_createRefreshToken_returnsToken(self, mock_create_token) -> None:
        # Arrange
        mock_create_token.return_value = self.mock_refresh_token
        
        # Act
        token = auth_service.create_refresh_token(data={})
        
        # Assert
        self.assertEqual(self.mock_refresh_token, token)

    def test_createToken_returnsToken(self) -> None:
        # Arrange & Act
        token = auth_service.create_token(data={}, expires_delta=timedelta(minutes=5))
        
        # Assert
        self.assertIsInstance(token, str)

    @patch('forum_system_api.services.auth_service.jwt.encode')
    def test_createToken_raises500_whenTokenCreationFails(self, mock_jwt_encode) -> None:
        # Arrange
        mock_jwt_encode.side_effect = JWTError()
        
        # Act & Assert
        with self.assertRaises(HTTPException) as ctx:
            auth_service.create_token(data={}, expires_delta=timedelta(minutes=5))
        
        self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR, ctx.exception.status_code)
        self.assertEqual('Could not create token', ctx.exception.detail)
    
    @patch('forum_system_api.services.auth_service.create_token_data')
    @patch('forum_system_api.services.auth_service.create_refresh_token')
    @patch('forum_system_api.services.auth_service.create_access_token')
    def test_createAccessAndRefreshTokens_returnsTokens(
        self, 
        mock_create_access_token, 
        mock_create_refresh_token, 
        mock_create_token_data
    ) -> None:
        # Arrange
        mock_create_access_token.return_value = self.mock_access_token
        mock_create_refresh_token.return_value = self.mock_refresh_token
        mock_create_token_data.return_value = self.payload
        
        # Act
        token_response = auth_service.create_access_and_refresh_tokens(
            user=self.user, 
            db=self.mock_db
        )
        
        # Assert
        mock_create_token_data.assert_called_once_with(user=self.user, db=self.mock_db)
        mock_create_access_token.assert_called_once_with(self.payload)
        mock_create_refresh_token.assert_called_once_with(self.payload)
        self.assertEqual(self.mock_access_token, token_response['access_token'])
        self.assertEqual(self.mock_refresh_token, token_response['refresh_token'])
        self.assertEqual('bearer', token_response['token_type'])
    
    @patch('forum_system_api.services.auth_service.verify_token')
    @patch('forum_system_api.services.auth_service.create_access_token')
    def test_refreshAccessToken_returnsToken(self, mock_create_access_token, mock_verify_token) -> None:
        # Arrange
        mock_verify_token.return_value = self.payload
        mock_create_access_token.return_value = self.mock_access_token
        
        # Act
        token = auth_service.refresh_access_token(refresh_token=self.mock_refresh_token, db=self.mock_db)
        
        # Assert
        mock_create_access_token.assert_called_once_with(self.payload)
        self.assertEqual(self.mock_access_token, token)

    @patch('forum_system_api.services.auth_service.jwt.decode')
    @patch('forum_system_api.services.auth_service.user_service.get_by_id')
    def test_verifyToken_returnsPayload(self, mock_get_by_id, mock_jwt_decode) -> None:
        # Arrange
        mock_jwt_decode.return_value = self.payload
        mock_get_by_id.return_value = self.user
        
        # Act
        result = auth_service.verify_token(token=self.mock_access_token, db=self.mock_db)
        
        # Assert
        mock_get_by_id.assert_called_once_with(user_id=self.user.id, db=self.mock_db)
        self.assertDictEqual(self.payload, result)

    @patch('forum_system_api.services.auth_service.jwt.decode')
    @patch('forum_system_api.services.auth_service.user_service.get_by_id')
    def test_verifyToken_raises401_whenUserNotFound(self, mock_get_by_id, mock_jwt_decode) -> None:
        # Arrange
        mock_jwt_decode.return_value = self.payload
        mock_get_by_id.return_value = None
        
        # Act & Assert
        with self.assertRaises(HTTPException) as ctx:
            auth_service.verify_token(token=self.mock_access_token, db=self.mock_db)
        
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, ctx.exception.status_code)
        self.assertEqual('Could not verify token', ctx.exception.detail)

    @patch('forum_system_api.services.auth_service.jwt.decode')
    @patch('forum_system_api.services.auth_service.user_service.get_by_id')
    def test_verifyToken_raises401_whenTokenVersionMismatch(self, mock_get_by_id, mock_jwt_decode) -> None:
        # Arrange
        mock_jwt_decode.return_value = {'sub': str(self.user.id), 'token_version': str(uuid4())}
        mock_get_by_id.return_value = self.user
        
        # Act & Assert
        with self.assertRaises(HTTPException) as ctx:
            auth_service.verify_token(token=self.mock_access_token, db=self.mock_db)
        
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, ctx.exception.status_code)
        self.assertEqual('Could not verify token', ctx.exception.detail)
    
    @patch('forum_system_api.services.auth_service.jwt.decode')
    def test_verifyToken_raises401_whenTokenIsInvalid(self, mock_jwt_decode) -> None:
        # Arrange
        mock_jwt_decode.side_effect = JWTError()
        
        # Act & Assert
        with self.assertRaises(HTTPException) as ctx:
            auth_service.verify_token(token=self.mock_access_token, db=self.mock_db)
        
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, ctx.exception.status_code)
        self.assertEqual('Could not verify token', ctx.exception.detail)

    @patch('forum_system_api.services.auth_service.uuid4')
    def test_updateTokenVersion_returnsTokenVersion(self, mock_uuid4) -> None:
        # Arrange
        mock_uuid4.return_value = self.user.token_version
        
        # Act
        token_version = auth_service.update_token_version(user=self.user, db=self.mock_db)
        
        # Assert
        self.assertEqual(self.user.token_version, token_version)
    
    def test_updateTokenVersion_raises404_whenUserIsNotFound(self) -> None:
        # Act & Assert
        with self.assertRaises(HTTPException) as ctx:
            auth_service.update_token_version(user=None, db=self.mock_db)
        
        self.assertEqual(status.HTTP_404_NOT_FOUND, ctx.exception.status_code)
        self.assertEqual('User not found', ctx.exception.detail)

    @patch('forum_system_api.services.auth_service.verify_password')
    @patch('forum_system_api.services.user_service.get_by_username')
    def test_authenticateUser_returnsUser(self, mock_get_by_username, mock_verify_password) -> None:
        # Arrange
        mock_get_by_username.return_value = self.user
        mock_verify_password.return_value = True
        
        # Act
        user = auth_service.authenticate_user(
            username=self.user.username, 
            password=VALID_PASSWORD, 
            db=self.mock_db
        )
        
        # Assert
        self.assertEqual(self.user, user)

    @patch('forum_system_api.services.user_service.get_by_username')
    def test_authenticateUser_raises401_whenUserNotFound(self, mock_get_by_username) -> None:
        # Arrange
        mock_get_by_username.return_value = None
        
        # Act & Assert
        with self.assertRaises(HTTPException) as ctx:
            auth_service.authenticate_user(
                username=self.user.username, 
                password=VALID_PASSWORD, 
                db=self.mock_db
            )
        
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, ctx.exception.status_code)
        self.assertEqual('Could not authenticate user', ctx.exception.detail)

    @patch('forum_system_api.services.auth_service.verify_password')
    @patch('forum_system_api.services.user_service.get_by_username')
    def test_authenticateUser_raises401_whenPasswordIsInvalid(
        self, 
        mock_get_by_username, 
        mock_verify_password
    ) -> None:
        # Arrange
        mock_get_by_username.return_value = self.user
        mock_verify_password.return_value = False
        
        # Act & Assert
        with self.assertRaises(HTTPException) as ctx:
            auth_service.authenticate_user(
                username=self.user.username, 
                password=VALID_PASSWORD, 
                db=self.mock_db
            )
        
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, ctx.exception.status_code)
        self.assertEqual('Could not authenticate user', ctx.exception.detail)
    
    @patch('forum_system_api.services.auth_service.is_admin')
    @patch('forum_system_api.services.auth_service.update_token_version')
    def test_createTokenData_returnsPayload(self, mock_update_token_version, mock_is_admin) -> None:
        # Arrange
        mock_update_token_version.return_value = self.user.token_version
        mock_is_admin.return_value = False
        
        # Act
        payload = auth_service.create_token_data(user=self.user, db=self.mock_db)
        
        # Assert
        mock_update_token_version.assert_called_once_with(user=self.user, db=self.mock_db)
        mock_is_admin.assert_called_once_with(user_id=self.user.id, db=self.mock_db)
        self.assertDictEqual(self.payload, payload)

    @patch('forum_system_api.services.user_service.get_by_id')
    @patch('forum_system_api.services.auth_service.verify_token')
    def test_getCurrentUser_returnsUser(self, mock_verify_token, mock_get_user_by_id) -> None:
        # Arrange
        mock_verify_token.return_value = {'sub': self.user.id}
        mock_get_user_by_id.return_value = self.user
        
        # Act
        user = auth_service.get_current_user(token=self.mock_access_token, db=self.mock_db)
        
        # Assert
        mock_verify_token.assert_called_once_with(token=self.mock_access_token, db=self.mock_db)
        self.assertEqual(self.user, user)

    @patch('forum_system_api.services.auth_service.verify_token')
    def test_getCurrentUser_raises401_whenTokenIsInvalid(self, mock_verify_token) -> None:
        # Arrange
        mock_verify_token.side_effect = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
        # Act & Assert
        with self.assertRaises(HTTPException):
            auth_service.get_current_user(token=self.mock_access_token, db=self.mock_db)

    @patch('forum_system_api.services.user_service.is_admin')
    def test_requireAdminRole_returnsUser_whenUserIsAdmin(self, mock_is_admin) -> None:
        # Arrange
        mock_is_admin.return_value = True
        
        # Act
        user = auth_service.require_admin_role(user=self.user, db=self.mock_db)
        
        # Assert
        self.assertEqual(self.user, user)

    @patch('forum_system_api.services.user_service.is_admin')
    def test_requireAdminRole_raises403_whenUserIsNotAdmin(self, mock_is_admin) -> None:
        # Arrange
        mock_is_admin.return_value = False
        
        # Act & Assert
        with self.assertRaises(HTTPException) as ctx:
            auth_service.require_admin_role(user=self.user, db=self.mock_db)
        
        self.assertEqual(status.HTTP_403_FORBIDDEN, ctx.exception.status_code)
        self.assertEqual('Access denied', ctx.exception.detail)
