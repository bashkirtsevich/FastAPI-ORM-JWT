from fastapi import HTTPException, status

DEFAULT_HEADERS = {"WWW-Authenticate": "Bearer"}

invalid_token_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers=DEFAULT_HEADERS,
)

invalid_representation_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect user representation",
    headers=DEFAULT_HEADERS,
)

invalid_credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers=DEFAULT_HEADERS,
)

inactive_user_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Inactive user",
    headers=DEFAULT_HEADERS,
)

already_exists_user_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User already exists",
    headers=DEFAULT_HEADERS,
)