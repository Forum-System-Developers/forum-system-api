import unittest
from unittest.mock import patch, MagicMock

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from forum_system_api.persistence.database import get_db, create_tables, Base


class TestDatabase(unittest.TestCase):
        @classmethod
        def setUpClass(cls) -> None:
            cls.engine = create_engine('sqlite:///:memory:')
            cls.SessionLocal = sessionmaker(
                autocommit=False, 
                autoflush=False, 
                bind=cls.engine
            )
            Base.metadata.create_all(bind=cls.engine)

        @classmethod
        def tearDownClass(cls) -> None:
            Base.metadata.drop_all(bind=cls.engine)
            cls.engine.dispose()

        def test_get_db_returnsSession_onSuccess(self) -> None:
            # Arrange
            db_gen = get_db()

            # Act
            db = next(db_gen)
            
            # Assert
            self.assertIsNotNone(db)
            db.close()

        def test_createTables_createsAllTables_onSuccess(self) -> None:
            # Arrange
            create_tables()
            
            # Act
            inspector = inspect(self.engine)
            tables = inspector.get_table_names()

            # Assert
            self.assertEqual(9, len(tables))
            self.assertIn('admins', tables)
            self.assertIn('users', tables)
            self.assertIn('categories', tables)
            self.assertIn('user_category_permissions', tables)
            self.assertIn('messages', tables)
            self.assertIn('conversations', tables)
            self.assertIn('replies', tables)
            self.assertIn('reply_reactions', tables)
            self.assertIn('topics', tables)

        @patch('forum_system_api.persistence.database.session_local')
        def test_get_db_closesSession_onExit(self, mock_session_local) -> None:
            # Arrange
            mock_session = MagicMock()
            mock_session_local.return_value = mock_session
            db_gen = get_db()
            next(db_gen)
            
            # Act
            with self.assertRaises(StopIteration):
                next(db_gen)
            
            # Assert
            mock_session.close.assert_called_once()

        def test_get_db_raisesStopIteration_onMultipleCalls(self) -> None:
            # Arrange
            db_gen = get_db()
            next(db_gen)

            # Act & Assert
            with self.assertRaises(StopIteration):
                next(db_gen)
