import unittest
from unittest.mock import MagicMock, patch

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from forum_system_api.persistence.models.category import Category
from forum_system_api.persistence.models.topic import Topic
from forum_system_api.persistence.models.user import User
from forum_system_api.persistence.models.user_category_permission import (
    UserCategoryPermission,
)
from forum_system_api.services.utils import category_access_utils as utils
from tests.services import test_data_const as td
from tests.services import test_data_obj as tobj


class CategoryAccessUtilsShould(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=Session)
        self.user = User(**tobj.USER_1)
        self.topic = Topic(**tobj.VALID_TOPIC_1)
        self.category = Category(**tobj.VALID_CATEGORY_1)
        self.permission = UserCategoryPermission(
            user_id=self.user.id,
            category_id=self.category.id,
            access_level=td.VALID_ACCESS_LEVEL_1,
        )

    def test_user_permission_categoryNotFound_returns404(self):
        with patch(
            "forum_system_api.services.utils.category_access_utils.get_category_by_id",
            return_value=None,
        ):
            with self.assertRaises(HTTPException) as context:
                utils.user_permission(self.user, self.topic, self.db)

            self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(context.exception.detail, "Category not found")

    def test_user_permission_categoryIsLocked_userIsAdmin_returnsTrue(self):
        self.category.is_locked = True

        with patch(
            "forum_system_api.services.utils.category_access_utils.get_category_by_id",
            return_value=self.category,
        ), patch(
            "forum_system_api.services.utils.category_access_utils.is_admin",
            return_value=True,
        ):
            result = utils.user_permission(self.user, self.topic, self.db)
            self.assertTrue(result)

    def test_user_permission_categoryIsLocked_userIsNotAdmin_returnsFalse(self):
        self.category.is_locked = True

        with patch(
            "forum_system_api.services.utils.category_access_utils.get_category_by_id",
            return_value=self.category,
        ), patch(
            "forum_system_api.services.utils.category_access_utils.is_admin",
            return_value=False,
        ):
            result = utils.user_permission(self.user, self.topic, self.db)
            self.assertFalse(result)

    def test_user_permission_categoryIsPrivate_userHasAccess_returnsTrue(self):
        self.category.is_locked = False
        self.category.is_private = True

        with patch(
            "forum_system_api.services.utils.category_access_utils.get_category_by_id",
            return_value=self.category,
        ), patch(
            "forum_system_api.services.utils.category_access_utils.category_write_permission",
            return_value=True,
        ):
            result = utils.user_permission(self.user, self.topic, self.db)
            self.assertTrue(result)

    def test_user_permission_categoryNotPrivate_returnsTrue(self):
        self.category.is_locked = False
        self.category.is_private = False

        with patch(
            "forum_system_api.services.utils.category_access_utils.get_category_by_id",
            return_value=self.category,
        ):
            result = utils.user_permission(self.user, self.topic, self.db)
            self.assertTrue(result)

    def test_get_access_level_noAccessLevel_returnsNone(self):
        self.user.permissions = []

        result = utils.get_access_level(self.user, self.category.id)
        self.assertIsNone(result)

    def test_get_access_level_returnsAccessLevel(self):
        self.topic.category_id = self.category.id

        self.user.permissions = [self.permission]

        result = utils.get_access_level(self.user, self.category.id)

        self.assertEqual(result, td.VALID_ACCESS_LEVEL_1)

    def test_category_permission_userHasAccessLevel_returnsTrue(self):
        with patch(
            "forum_system_api.services.utils.category_access_utils.get_access_level",
            return_value=td.VALID_ACCESS_LEVEL_1,
        ):
            result = utils.category_write_permission(self.user, self.topic, self.db)
            self.assertTrue(result)

    def test_category_permission_userHasNoAccessLevel_notAdmin_returnsFalse(self):
        with (
            patch(
                "forum_system_api.services.utils.category_access_utils.get_access_level",
                return_value=None,
            ),
            patch(
                "forum_system_api.services.utils.category_access_utils.is_admin",
                return_value=False,
            ),
        ):
            result = utils.category_write_permission(self.user, self.topic, self.db)
            self.assertFalse(result)

    def test_category_permission_userHasNoAccessLevel_isAdmin_returnsTrue(self):
        with (
            patch(
                "forum_system_api.services.utils.category_access_utils.get_access_level",
                return_value=None,
            ),
            patch(
                "forum_system_api.services.utils.category_access_utils.is_admin",
                return_value=True,
            ),
        ):
            result = utils.category_write_permission(self.user, self.topic, self.db)
            self.assertTrue(result)

    def test_verify_topic_permission_categoryIsPrivate_userHasNoAccess_raises403(self):
        self.user.permissions = []

        self.category.is_private = True

        with (
            patch(
                "forum_system_api.services.utils.category_access_utils.get_category_by_id",
                return_value=self.category,
            ),
            patch(
                "forum_system_api.services.utils.category_access_utils.is_admin",
                return_value=False,
            ),
        ):
            with self.assertRaises(HTTPException) as context:
                utils.verify_topic_permission(self.topic, self.user, self.db)

            self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(context.exception.detail, "Unauthorized")

    def test_verify_topic_permission_categoryIsPrivate_userHasAccess_returnsNone(self):
        self.category.is_private = True

        self.user.permissions = [self.permission]

        with (
            patch(
                "forum_system_api.services.utils.category_access_utils.get_category_by_id",
                return_value=self.category,
            ),
            patch(
                "forum_system_api.services.utils.category_access_utils.is_admin",
                return_value=False,
            ),
        ):
            result = utils.verify_topic_permission(self.topic, self.user, self.db)

            self.assertIsNone(result)

    def test_verify_topic_permission_categoryIsPrivate_userHasNoAccess_userIsAdmin_returnsNone(
        self,
    ):
        self.category.is_private = True

        self.user.permissions = []

        with (
            patch(
                "forum_system_api.services.utils.category_access_utils.get_category_by_id",
                return_value=self.category,
            ),
            patch(
                "forum_system_api.services.utils.category_access_utils.is_admin",
                return_value=True,
            ),
        ):
            result = utils.verify_topic_permission(self.topic, self.user, self.db)

            self.assertIsNone(result)
