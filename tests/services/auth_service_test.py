import unittest
from unittest.mock import MagicMock, patch
from datetime import timedelta
from uuid import uuid4

from fastapi import HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session

from forum_system_api.persistence.models.user import User
from forum_system_api.services import auth_service
from tests.services.test_data import USER_1


class AuthService_Should(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock(spec=Session)
        self.user = User(**USER_1)
        self.access_token = 'access_token'
        self.refresh_token = 'refresh_token'
        self.payload = {
            'sub': str(self.user.id), 
            'token_version': str(self.user.token_version)
        }
    
    @patch('forum_system_api.services.auth_service.create_token')
    def test_createAccessToken_returnsToken(self, mock_create_token) -> None:
        # Arrange
        mock_create_token.return_value = self.access_token
        
        # Act
        token = auth_service.create_access_token(data={})
        
        # Assert
        self.assertEqual(self.access_token, token)

    @patch('forum_system_api.services.auth_service.create_token')
    def test_createRefreshToken_returnsToken(self, mock_create_token) -> None:
        # Arrange
        mock_create_token.return_value = self.refresh_token
        
        # Act
        token = auth_service.create_refresh_token(data={})
        
        # Assert
        self.assertEqual(self.refresh_token, token)

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
    
    @patch('forum_system_api.services.auth_service.verify_token')
    @patch('forum_system_api.services.auth_service.create_access_token')
    def test_refreshAccessToken_returnsToken(self, mock_create_access_token, mock_verify_token) -> None:
        # Arrange
        mock_verify_token.return_value = self.payload
        mock_create_access_token.return_value = self.access_token
        
        # Act
        token = auth_service.refresh_access_token(refresh_token=self.refresh_token, db=self.mock_db)
        
        # Assert
        mock_create_access_token.assert_called_once_with(self.payload)
        self.assertEqual(self.access_token, token)

    @patch('forum_system_api.services.auth_service.jwt.decode')
    @patch('forum_system_api.services.auth_service.user_service.get_by_id')
    def test_verifyToken_returnsPayload(self, mock_get_by_id, mock_jwt_decode) -> None:
        # Arrange
        mock_jwt_decode.return_value = self.payload
        mock_get_by_id.return_value = self.user
        
        # Act
        result = auth_service.verify_token(token=self.access_token, db=self.mock_db)
        
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
            auth_service.verify_token(token=self.access_token, db=self.mock_db)
        
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
            auth_service.verify_token(token=self.access_token, db=self.mock_db)
        
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, ctx.exception.status_code)
        self.assertEqual('Could not verify token', ctx.exception.detail)
    
    @patch('forum_system_api.services.auth_service.jwt.decode')
    def test_verifyToken_raises401_whenTokenIsInvalid(self, mock_jwt_decode) -> None:
        # Arrange
        mock_jwt_decode.side_effect = JWTError()
        
        # Act & Assert
        with self.assertRaises(HTTPException) as ctx:
            auth_service.verify_token(token=self.access_token, db=self.mock_db)
        
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, ctx.exception.status_code)
        self.assertEqual('Could not verify token', ctx.exception.detail)
