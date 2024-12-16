def expression_matches(expected_expr):
    def matcher(arg):
        return str(arg) == str(expected_expr)

    return matcher


def assert_filter_called_with(mock_query, expected_expression):
    """
    Utility function to assert that the SQLAlchemy filter was called with a specific expression.
    """
    mock_query.filter.assert_called_once()
    filter_call_arg = mock_query.filter.call_args[0][0]
    assert expression_matches(expected_expression)(
        filter_call_arg
    ), f"Expected filter to be called with: {expected_expression}, but got: {filter_call_arg}"
