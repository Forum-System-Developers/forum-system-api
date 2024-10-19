from unittest.mock import MagicMock

from sqlalchemy import BinaryExpression


def assert_filter_called_with(
        mock_query: MagicMock, 
        expected_expression: BinaryExpression
) -> None:
    """
    Utility function to assert that the SQLAlchemy filter was called with a specific expression.
    """
    mock_query.filter.assert_called_once()
    actual_expression = mock_query.filter.call_args[0][0]
    assert str(expected_expression) == str(actual_expression), (
        f"Expected filter to be called with: {expected_expression}, but got: {actual_expression}"
    )
