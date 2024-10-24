from pydantic import constr


Username = constr(
    min_length=3, 
    max_length=30, 
    strip_whitespace=True, 
    pattern=r'^[a-zA-Z0-9]+$'
)

Name = constr(
    min_length=2, 
    max_length=30, 
    strip_whitespace=True, 
    pattern=r'^[a-zA-Z]+$'
) 

Password = constr(
    min_length=8, 
    max_length=30, 
    strip_whitespace=True
)
