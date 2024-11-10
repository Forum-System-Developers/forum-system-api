from pydantic import constr


Username = constr(
    min_length=3, max_length=30, strip_whitespace=True, pattern=r"^[a-zA-Z0-9_]+$"
)

Name = constr(
    min_length=2,
    max_length=30,
    strip_whitespace=True,
    pattern=r"^[a-zA-Z]+(?:-[a-zA-Z]+)*$",
)

"""
The string must contain at least one lowercase letter, 
one uppercase letter, one digit, one special character, 
and be between 8 and 30 characters long.
"""
Password = constr(min_length=8, max_length=30, strip_whitespace=True)

Title = constr(min_length=5, max_length=50)

Content = constr(min_length=5, max_length=999)

Title_for_category = constr(min_length=2, max_length=30, pattern=r"^[a-zA-Z0-9 ]+$")

TopicContent = constr(min_length=5, max_length=999)

MessageContent = constr(min_length=1, max_length=10000)
