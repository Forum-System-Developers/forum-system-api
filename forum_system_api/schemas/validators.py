from pydantic import constr


class UsernameType(constr):
    strip_whitespace = True
    min_length = 3
    max_length = 30
    regex = r'^[a-zA-Z0-9]+$'


class NameType(constr):
    strip_whitespace = True
    min_length = 2
    max_length = 30
    regex = r'^[a-zA-Z]+$'


class PasswordType(constr):
    strip_whitespace = True
    min_length = 8
    max_length = 30
