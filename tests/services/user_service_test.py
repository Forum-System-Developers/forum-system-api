import unittest
from unittest.mock import MagicMock, Mock, patch
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy.orm import Session

from forum_system_api.persistence.models.admin import Admin
from forum_system_api.persistence.models.user import User
from forum_system_api.persistence.models.user_category_permission import UserCategoryPermission
from forum_system_api.schemas.user import UserCreate
from forum_system_api.services import user_service
from tests.services.test_data import USER_1, USER_2, VALID_PASSWORD
from tests.services.utils import assert_filter_called_with


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

    def test_getById_returnsCorrect_whenUserIsFound(self) -> None:
        # Arrange
        query_mock = self.mock_db.query.return_value
        filter_mock = query_mock.filter.return_value
        filter_mock.first.return_value = self.user

        # Act
        user = user_service.get_by_id(self.user_id, self.mock_db)

        # Assert
        self.assertEqual(user, self.user)
        self.mock_db.query.assert_called_once_with(User)
        assert_filter_called_with(query_mock, User.id == self.user_id)

    def test_getById_returnsNone_whenUserIsNotFound(self) -> None:
        # Arrange
        query_mock = self.mock_db.query.return_value
        filter_mock = query_mock.filter.return_value
        filter_mock.first.return_value = None

        # Act
        user = user_service.get_by_id(self.user_id, self.mock_db)

        # Assert
        self.assertIsNone(user)
        self.mock_db.query.assert_called_once_with(User)
        assert_filter_called_with(query_mock, User.id == self.user_id)

    def test_getByUsername_returnsCorrect_whenUserIsFound(self) -> None:
        # Arrange
        query_mock = self.mock_db.query.return_value
        filter_mock = query_mock.filter.return_value
        filter_mock.first.return_value = self.user

        # Act
        user = user_service.get_by_username(self.user.username, self.mock_db)

        # Assert
        self.assertEqual(user, self.user)
        self.mock_db.query.assert_called_once_with(User)
        assert_filter_called_with(query_mock, User.username == self.user.username)

    def test_getByUsername_returnsNone_whenUserIsNotFound(self) -> None:
        # Arrange
        query_mock = self.mock_db.query.return_value
        filter_mock = query_mock.filter.return_value
        filter_mock.first.return_value = None

        # Act
        user = user_service.get_by_username(self.user.username, self.mock_db)

        # Assert
        self.assertIsNone(user)
        self.mock_db.query.assert_called_once_with(User)
        assert_filter_called_with(query_mock, User.username == self.user.username)

    def test_getByEmail_returnsCorrect_whenUserIsFound(self) -> None:
        # Arrange
        query_mock = self.mock_db.query.return_value
        filter_mock = query_mock.filter.return_value
        filter_mock.first.return_value = self.user

        # Act
        user = user_service.get_by_email(self.user.email, self.mock_db)

        # Assert
        self.assertEqual(user, self.user)
        self.mock_db.query.assert_called_once_with(User)
        assert_filter_called_with(query_mock, User.email == self.user.email)
    
    def test_getByEmail_returnsNone_whenUserIsNotFound(self) -> None:
        # Arrange
        query_mock = self.mock_db.query.return_value
        filter_mock = query_mock.filter.return_value
        filter_mock.first.return_value = None

        # Act
        user = user_service.get_by_email(self.user.email, self.mock_db)

        # Assert
        self.assertIsNone(user)
        self.mock_db.query.assert_called_once_with(User)
        assert_filter_called_with(query_mock, User.email == self.user.email)

    @patch("forum_system_api.services.user_service.get_by_username")
    def test_create_raises400_whenUsernameAlreadyExists(self, mock_get_by_username) -> None:
        # Arrange
        user_with_existing_username = UserCreate(
            username=self.user.username,
            email=self.user2.email,
            password=VALID_PASSWORD,
            first_name=self.user2.first_name,
            last_name=self.user2.last_name
        )
        mock_get_by_username.return_value = self.user

        # Act & Assert
        with self.assertRaises(HTTPException) as exception_ctx:
            user_service.create(user_with_existing_username, self.mock_db)

        # Assert
        self.assertEqual(exception_ctx.exception.status_code, 400)
        self.assertIn("Username already exists", str(exception_ctx.exception))

    @patch("forum_system_api.services.user_service.get_by_email")
    @patch("forum_system_api.services.user_service.get_by_username")
    def test_create_raises400_whenEmailAlreadyExists(self, mock_get_by_username, mock_get_by_email) -> None:
        # Arrange
        user_with_existing_email = UserCreate(
            username=self.user2.username,
            email=self.user.email,
            password=VALID_PASSWORD,
            first_name=self.user2.first_name,
            last_name=self.user2.last_name
        )
        mock_get_by_username.return_value = None
        mock_get_by_email.return_value = user_with_existing_email

        # Act & Assert
        with self.assertRaises(HTTPException) as exception_ctx:
            user_service.create(user_with_existing_email, self.mock_db)
        
        # Assert
        self.assertEqual(exception_ctx.exception.status_code, 400)
        self.assertIn("Email already exists", str(exception_ctx.exception))

    @patch("forum_system_api.services.user_service.hash_password")
    @patch("forum_system_api.services.user_service.get_by_email")
    @patch("forum_system_api.services.user_service.get_by_username")
    def test_create_returnsCreatedUser(
        self, 
        mock_get_by_username, 
        mock_get_by_email, 
        mock_hash_password
    ) -> None:
        # Arrange
        user_creation_data = UserCreate(
            username=self.user.username,
            email=self.user.email,
            password=VALID_PASSWORD,
            first_name=self.user.first_name,
            last_name=self.user.last_name
        )
        mock_get_by_username.return_value = None
        mock_get_by_email.return_value = None
        mock_hash_password.return_value = self.user.password_hash

        def mock_add(user):
            user.id = self.user.id
            user.created_at = self.user.created_at
            user.token_version = self.user.token_version

        self.mock_db.add.side_effect = mock_add
        self.mock_db.commit.return_value = None
        self.mock_db.refresh.return_value = None

        # Act
        created_user = user_service.create(user_creation_data, self.mock_db)

        # Assert
        self.mock_db.add.assert_called_once()
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once()

        self.assertEqual(created_user.id, self.user.id)
        self.assertEqual(created_user.username, self.user.username)
        self.assertEqual(created_user.password_hash, self.user.password_hash)
        self.assertEqual(created_user.email, self.user.email)
        self.assertEqual(created_user.first_name, self.user.first_name)
        self.assertEqual(created_user.last_name, self.user.last_name)
        self.assertEqual(created_user.token_version, self.user.token_version)
        self.assertEqual(created_user.created_at, self.user.created_at)

    def test_isAdmin_returnsTrue_whenUserIsAdmin(self) -> None:
        # Arrange
        query_mock = self.mock_db.query.return_value
        filter_mock = query_mock.filter.return_value
        filter_mock.first.return_value = self.user

        # Act
        is_admin = user_service.is_admin(self.user_id, self.mock_db)

        # Assert
        self.assertTrue(is_admin)
        self.mock_db.query.assert_called_once_with(Admin)
        assert_filter_called_with(query_mock, Admin.user_id == self.user.id)

    def test_isAdmin_returnsFalse_whenUserIsNotAdmin(self) -> None:
        # Arrange
        query_mock = self.mock_db.query.return_value
        filter_mock = query_mock.filter.return_value
        filter_mock.first.return_value = None

        # Act
        is_admin = user_service.is_admin(self.user_id, self.mock_db)

        # Assert
        self.assertFalse(is_admin)
        self.mock_db.query.assert_called_once_with(Admin)
        assert_filter_called_with(query_mock, Admin.user_id == self.user.id)

    @patch("forum_system_api.services.category_service.get_by_id")
    def test_getPrivilegedUsers_returnsCorrect_whenCategoryIsFound(self, mock_get_category_by_id) -> None:
        # Arrange
        category_id = uuid4()
        user1_category_permission = Mock(
            user=self.user,
            access_level="READ"
        )
        user2_category_permission = Mock(
            user=self.user2,
            access_level="WRITE"
        )
        permissions = [user1_category_permission, user2_category_permission] 
        category = Mock(id=category_id, permissions=permissions)
        mock_get_category_by_id.return_value = category

        # Act
        privileged_users = user_service.get_privileged_users(category_id, self.mock_db)

        # Assert
        self.assertDictEqual(
            privileged_users, 
            {
                self.user: user1_category_permission, 
                self.user2: user2_category_permission
            }
        )
    
    @patch("forum_system_api.services.category_service.get_by_id")
    def test_getPrivilegedUsers_raises404_whenCategoryIsNotFound(self, mock_get_category_by_id) -> None:
        # Arrange
        category_id = uuid4()
        mock_get_category_by_id.return_value = None

        # Act & Assert
        with self.assertRaises(HTTPException) as exception_ctx:
            user_service.get_privileged_users(category_id, self.mock_db)

        # Assert
        self.assertEqual(exception_ctx.exception.status_code, 404)
        self.assertIn("Category not found", str(exception_ctx.exception))

    @patch("forum_system_api.services.user_service.get_by_id")
    def test_getUserPermissions_returnsCorrect_whenUserIsFound(self, mock_get_by_id) -> None:
        # Arrange
        self.user.permissions = [
            UserCategoryPermission(
                user_id=self.user.id, 
                category_id=uuid4(),
                access_level="READ"
            ),
            UserCategoryPermission(
                user_id=self.user.id, 
                category_id=uuid4(),
                access_level="WRITE"
            )
        ]
        mock_get_by_id.return_value = self.user

        # Act
        user_permissions = user_service.get_user_permissions(self.user.id, self.mock_db)

        # Assert
        self.assertListEqual(user_permissions, self.user.permissions)
        self.assertEqual(len(user_permissions), 2)
        self.assertIn("READ", user_permissions[0].access_level)
        self.assertIn("WRITE", user_permissions[1].access_level)

    @patch("forum_system_api.services.user_service.get_by_id")
    def test_getUserPermissions_raises404_whenUserIsNotFound(self, mock_get_by_id) -> None:
        # Arrange
        mock_get_by_id.return_value = None

        # Act & Assert
        with self.assertRaises(HTTPException) as exception_ctx:
            user_service.get_user_permissions(self.user_id, self.mock_db)

        # Assert
        self.assertEqual(exception_ctx.exception.status_code, 404)
        self.assertIn("User not found", str(exception_ctx.exception))
