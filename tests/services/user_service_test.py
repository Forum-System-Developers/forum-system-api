import unittest
from unittest.mock import MagicMock, Mock, patch
from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from forum_system_api.persistence.models.access_level import AccessLevel
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
        self.user = User(**USER_1)
        self.user2 = User(**USER_2)

    def test_getAll_returnsAllUsers(self) -> None:
        # Arrange
        mock_query = self.mock_db.query.return_value
        mock_query.all.return_value = [self.user, self.user2]

        # Act
        users = user_service.get_all(self.mock_db)

        # Assert
        self.assertListEqual(users, [self.user, self.user2])
        self.mock_db.query.assert_called_once_with(User)
        mock_query.all.assert_called_once()

    def test_getAll_returnsEmptyList_whenNoUsers(self) -> None:
        # Arrange
        mock_query = self.mock_db.query.return_value
        mock_query.all.return_value = []

        # Act
        users = user_service.get_all(self.mock_db)

        # Assert
        self.assertListEqual(users, list())
        self.mock_db.query.assert_called_once_with(User)
        mock_query.all.assert_called_once()

    def test_getById_returnsCorrect_whenUserIsFound(self) -> None:
        # Arrange
        mock_query = self.mock_db.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = self.user

        # Act
        user = user_service.get_by_id(self.user.id, self.mock_db)

        # Assert
        self.assertEqual(user, self.user)
        self.mock_db.query.assert_called_once_with(User)
        assert_filter_called_with(mock_query, User.id == self.user.id)

    def test_getById_returnsNone_whenUserIsNotFound(self) -> None:
        # Arrange
        mock_query = self.mock_db.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = None

        # Act
        user = user_service.get_by_id(self.user.id, self.mock_db)

        # Assert
        self.assertIsNone(user)
        self.mock_db.query.assert_called_once_with(User)
        assert_filter_called_with(mock_query, User.id == self.user.id)

    def test_getByUsername_returnsCorrect_whenUserIsFound(self) -> None:
        # Arrange
        mock_query = self.mock_db.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = self.user

        # Act
        user = user_service.get_by_username(self.user.username, self.mock_db)

        # Assert
        self.assertEqual(user, self.user)
        self.mock_db.query.assert_called_once_with(User)
        assert_filter_called_with(mock_query, User.username == self.user.username)

    def test_getByUsername_returnsNone_whenUserIsNotFound(self) -> None:
        # Arrange
        mock_query = self.mock_db.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = None

        # Act
        user = user_service.get_by_username(self.user.username, self.mock_db)

        # Assert
        self.assertIsNone(user)
        self.mock_db.query.assert_called_once_with(User)
        assert_filter_called_with(mock_query, User.username == self.user.username)

    def test_getByEmail_returnsCorrect_whenUserIsFound(self) -> None:
        # Arrange
        mock_query = self.mock_db.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = self.user

        # Act
        user = user_service.get_by_email(self.user.email, self.mock_db)

        # Assert
        self.assertEqual(user, self.user)
        self.mock_db.query.assert_called_once_with(User)
        assert_filter_called_with(mock_query, User.email == self.user.email)
    
    def test_getByEmail_returnsNone_whenUserIsNotFound(self) -> None:
        # Arrange
        mock_query = self.mock_db.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = None

        # Act
        user = user_service.get_by_email(self.user.email, self.mock_db)

        # Assert
        self.assertIsNone(user)
        self.mock_db.query.assert_called_once_with(User)
        assert_filter_called_with(mock_query, User.email == self.user.email)

    @patch("forum_system_api.services.user_service.ensure_unique_username_and_email")
    @patch("forum_system_api.services.user_service.hash_password")
    def test_create_returnsCreatedUser(
        self,
        mock_hash_password,
        mock_ensure_unique_username_and_email
    ) -> None:
        # Arrange
        user_creation_data = UserCreate(
            username=self.user.username,
            email=self.user.email,
            password=VALID_PASSWORD,
            first_name=self.user.first_name,
            last_name=self.user.last_name
        )
        mock_hash_password.return_value = self.user.password_hash
        mock_ensure_unique_username_and_email.return_value = None

        def mock_add(user):
            user.id = self.user.id
            user.created_at = self.user.created_at
            user.token_version = self.user.token_version

        self.mock_db.add.side_effect = mock_add
        self.mock_db.commit.return_value = None
        self.mock_db.refresh.return_value = None

        # Act
        created_user = user_service.create(
            user_data=user_creation_data, 
            db=self.mock_db
        )

        # Assert
        mock_ensure_unique_username_and_email.assert_called_once()
        self.mock_db.add.assert_called_once_with(self.user)
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once_with(self.user)

        self.assertEqual(self.user, created_user)

    def test_isAdmin_returnsTrue_whenUserIsAdmin(self) -> None:
        # Arrange
        mock_query = self.mock_db.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = self.user

        # Act
        is_admin = user_service.is_admin(self.user.id, self.mock_db)

        # Assert
        self.assertTrue(is_admin)
        self.mock_db.query.assert_called_once_with(Admin)
        assert_filter_called_with(mock_query, Admin.user_id == self.user.id)

    def test_isAdmin_returnsFalse_whenUserIsNotAdmin(self) -> None:
        # Arrange
        mock_query = self.mock_db.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = None

        # Act
        is_admin = user_service.is_admin(self.user.id, self.mock_db)

        # Assert
        self.assertFalse(is_admin)
        self.mock_db.query.assert_called_once_with(Admin)
        assert_filter_called_with(mock_query, Admin.user_id == self.user.id)

    @patch("forum_system_api.services.category_service.get_by_id")
    def test_getPrivilegedUsers_returnsCorrect_whenCategoryIsFound(self, mock_get_category_by_id) -> None:
        # Arrange
        category_id = uuid4()
        user1_category_permission = UserCategoryPermission(
            user=self.user,
            category_id=category_id,
            access_level=AccessLevel.READ
        )
        user2_category_permission = UserCategoryPermission(
            user=self.user2,
            category_id=category_id,
            access_level=AccessLevel.WRITE
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

        self.assertEqual(status.HTTP_404_NOT_FOUND, exception_ctx.exception.status_code)
        self.assertIn("Category not found", str(exception_ctx.exception))

    @patch("forum_system_api.services.category_service.get_by_id")
    def test_getPrivilegedUsers_raises400_whenCategoryIsNotPrivate(self, mock_get_category_by_id) -> None:
        # Arrange
        category_id = uuid4()
        category = Mock(id=category_id, is_private=False)
        mock_get_category_by_id.return_value = category

        # Act & Assert
        with self.assertRaises(HTTPException) as exception_ctx:
            user_service.get_privileged_users(category_id, self.mock_db)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, exception_ctx.exception.status_code)
        self.assertIn("Category is not private", str(exception_ctx.exception))

    @patch("forum_system_api.services.user_service.get_by_id")
    def test_getUserPermissions_returnsCorrect_whenUserIsFound(self, mock_get_by_id) -> None:
        # Arrange
        category_id = uuid4()
        self.user.permissions = [
            UserCategoryPermission(
                user_id=self.user.id, 
                category_id=category_id,
                access_level=AccessLevel.READ
            ),
            UserCategoryPermission(
                user_id=self.user.id, 
                category_id=category_id,
                access_level=AccessLevel.WRITE
            )
        ]
        mock_get_by_id.return_value = self.user

        # Act
        user_permissions = user_service.get_user_permissions(self.user.id, self.mock_db)

        # Assert
        self.assertListEqual(self.user.permissions, user_permissions)
        self.assertEqual(2, len(user_permissions))

    @patch("forum_system_api.services.user_service.get_by_id")
    def test_getUserPermissions_raises404_whenUserIsNotFound(self, mock_get_by_id) -> None:
        # Arrange
        mock_get_by_id.return_value = None

        # Act & Assert
        with self.assertRaises(HTTPException) as exception_ctx:
            user_service.get_user_permissions(self.user.id, self.mock_db)

        self.assertEqual(status.HTTP_404_NOT_FOUND, exception_ctx.exception.status_code)
        self.assertIn("User not found", str(exception_ctx.exception))

    @patch("forum_system_api.services.user_service.get_user_category_permission")
    def test_revokeAccess_returnsTrue_whenPermissionIsFound(self, mock_get_user_category_permission) -> None:
        # Arrange
        user_category_permission = Mock()
        mock_get_user_category_permission.return_value = (self.user, None, user_category_permission)

        # Act
        result = user_service.revoke_access(self.user.id, self.user.id, self.mock_db)

        # Assert
        mock_get_user_category_permission.assert_called_once()
        self.mock_db.delete.assert_called_once_with(user_category_permission)
        self.mock_db.commit.assert_called_once()
        self.assertTrue(result)
    
    @patch("forum_system_api.services.user_service.get_user_category_permission")
    def test_revokeAccess_raises404_whenPermissionIsNotFound(self, mock_get_user_category_permission) -> None:
        # Arrange
        mock_get_user_category_permission.return_value = (self.user, None, None)

        # Act & Assert
        with self.assertRaises(HTTPException) as exception_ctx:
            user_service.revoke_access(self.user.id, self.user.id, self.mock_db)
        
        mock_get_user_category_permission.assert_called_once()
        self.mock_db.delete.assert_not_called()
        self.mock_db.commit.assert_not_called()
        self.assertEqual(status.HTTP_404_NOT_FOUND, exception_ctx.exception.status_code)
        self.assertIn("Permission not found", str(exception_ctx.exception))

    @patch("forum_system_api.services.user_service.get_user_category_permission")
    def test_updateAccessLevel_createsNewPermission_whenPermissionIsNotFound(
        self, 
        mock_get_user_category_permission
    ) -> None:
        # Arrange
        category = Mock(id=uuid4(), permissions=[])
        access_level = AccessLevel.WRITE
        mock_get_user_category_permission.return_value = (self.user, category, None)

        # Act
        result = user_service.update_access_level(
            user_id=self.user.id, 
            category_id=category.id, 
            access_level=access_level, 
            db=self.mock_db
        )

        # Assert
        mock_get_user_category_permission.assert_called_once()
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once_with(result)
        self.assertEqual(access_level, result.access_level)
        self.assertListEqual(category.permissions, [result])

    @patch("forum_system_api.services.user_service.get_user_category_permission")
    def test_updateAccessLevel_updatesExistingPermission_whenPermissionIsFound(
        self, 
        mock_get_user_category_permission
    ) -> None:
        # Arrange
        access_level = AccessLevel.WRITE
        user_category_permission = Mock(access_level=AccessLevel.READ)
        mock_get_user_category_permission.return_value = (self.user, None, user_category_permission)

        # Act
        result = user_service.update_access_level(
            user_id=self.user.id, 
            category_id=uuid4(), 
            access_level=access_level, 
            db=self.mock_db
        )

        # Assert
        mock_get_user_category_permission.assert_called_once()
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once_with(result)
        self.assertEqual(access_level, result.access_level)

    @patch("forum_system_api.services.category_service.get_by_id")
    @patch("forum_system_api.services.user_service.get_by_id")
    def test_getUserCategoryPermission_returnsCorrect_whenPermissionIsFound(
        self, 
        mock_get_by_id, 
        mock_get_category_by_id
    ) -> None:
        # Arrange
        permission = Mock(user_id=self.user.id)
        category = Mock(id=uuid4(), permissions=[permission])
        mock_get_by_id.return_value = self.user
        mock_get_category_by_id.return_value = category

        # Act
        result = user_service.get_user_category_permission(
            user_id=self.user.id, 
            category_id=category.id, 
            db=self.mock_db
        )

        # Assert
        self.assertEqual(self.user, result[0])
        self.assertEqual(category, result[1])
        self.assertEqual(permission, result[2])

    @patch("forum_system_api.services.category_service.get_by_id")
    @patch("forum_system_api.services.user_service.get_by_id")
    def test_getUserCategoryPermission_returnsUserAndCategoryWithPermissionAsNone_whenPermissionIsNotFound(
        self, 
        mock_get_by_id, 
        mock_get_category_by_id
    ) -> None:
        # Arrange
        permission = Mock(user_id=self.user2.id)
        category = Mock(id=uuid4(), permissions=[permission])
        mock_get_by_id.return_value = self.user
        mock_get_category_by_id.return_value = category

        # Act
        result = user_service.get_user_category_permission(
            user_id=self.user.id, 
            category_id=category.id, 
            db=self.mock_db
        )

        # Assert
        self.assertEqual(self.user, result[0])
        self.assertEqual(category, result[1])
        self.assertIsNone(result[2])

    @patch("forum_system_api.services.user_service.get_by_id")
    def test_getUserCategoryPermission_raises404_whenUserIsNotFound(
        self, 
        mock_get_by_id
    ) -> None:
        # Arrange
        mock_get_by_id.return_value = None

        # Act & Assert
        with self.assertRaises(HTTPException) as exception_ctx:
            user_service.get_user_category_permission(
                user_id=self.user.id, 
                category_id=uuid4(), 
                db=self.mock_db
            )

        self.assertEqual(status.HTTP_404_NOT_FOUND, exception_ctx.exception.status_code)
        self.assertIn("User not found", str(exception_ctx.exception))

    @patch("forum_system_api.services.category_service.get_by_id")
    @patch("forum_system_api.services.user_service.get_by_id")
    def test_getUserCategoryPermission_raises404_whenCategoryIsNotFound(
        self, 
        mock_get_by_id, 
        mock_get_category_by_id
    ) -> None:
        # Arrange
        mock_get_by_id.return_value = self.user
        mock_get_category_by_id.return_value = None

        # Act & Assert
        with self.assertRaises(HTTPException) as exception_ctx:
            user_service.get_user_category_permission(
                user_id=self.user.id, 
                category_id=uuid4(), 
                db=self.mock_db
            )

        self.assertEqual(status.HTTP_404_NOT_FOUND, exception_ctx.exception.status_code)
        self.assertIn("Category not found", str(exception_ctx.exception))

    @patch("forum_system_api.services.user_service.get_by_username")
    def test_ensureUniqueUsernameAndEmail_raises400_whenUsernameAlreadyExists(
        self, 
        mock_get_by_username
    ) -> None:
        # Arrange
        mock_get_by_username.return_value = self.user

        # Act & Assert
        with self.assertRaises(HTTPException) as exception_ctx:
            user_service.ensure_unique_username_and_email(self.user.username, self.user.email, self.mock_db)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, exception_ctx.exception.status_code)
        self.assertIn("Username already exists", str(exception_ctx.exception))
    
    @patch("forum_system_api.services.user_service.get_by_username")
    @patch("forum_system_api.services.user_service.get_by_email")
    def test_ensureUniqueUsernameAndEmail_raises400_whenEmailAlreadyExists(
        self, 
        mock_get_by_email,
        mock_get_by_username
    ) -> None:
        # Arrange
        mock_get_by_username.return_value = None
        mock_get_by_email.return_value = self.user

        # Act & Assert
        with self.assertRaises(HTTPException) as exception_ctx:
            user_service.ensure_unique_username_and_email(self.user.username, self.user.email, self.mock_db)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, exception_ctx.exception.status_code)
        self.assertIn("Email already exists", str(exception_ctx.exception))
