import unittest
from unittest.mock import MagicMock
from uuid import uuid4

from sqlalchemy.orm import Session
from fastapi import HTTPException

from forum_system_api.persistence.models.category import Category
from forum_system_api.schemas.category import CategoryResponse, CreateCategory
from forum_system_api.services import category_service
from tests.services.test_data import CATEGORY_1, CATEGORY_2
from tests.services.utils import assert_filter_called_with


class CategoryService_Should(unittest.TestCase):
    
    def setUp(self):
        self.mock_db = MagicMock(spec=Session)
        self.category_id = uuid4()
        self.category = Category(**CATEGORY_1)
        self.category2 = Category(**CATEGORY_2)

    def test_createCategory_returnsCategoryResponse(self) -> None:
        # Arrange & Act
        category_response = category_service.create_category(
            CreateCategory(
                name=self.category.name, 
                is_private=self.category.is_private, 
                is_locked=self.category.is_locked), self.mock_db)

        # Assert
        self.assertEqual(category_response.name, self.category.name)
        self.assertEqual(category_response.is_private, self.category.is_private)
        self.assertEqual(category_response.is_locked, self.category.is_locked)

    def test_getAll_returnsAllCategories(self) -> None:
        # Arrange
        query_mock = self.mock_db.query.return_value
        query_mock.all.return_value = [self.category, self.category2]

        # Act
        categories = category_service.get_all(self.mock_db)

        # Assert
        self.assertListEqual(categories, [
            CategoryResponse(**CATEGORY_1),
            CategoryResponse(**CATEGORY_2)
        ])
        self.mock_db.query.assert_called_once_with(Category)
        query_mock.all.assert_called_once()
