from fastapi import HTTPException, status

from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

from .consts import (
    SECRET_KEY_ACCESS,
    SECRET_KEY_REFRESH,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its hashed version.

    Params:
        - plain_password (str): The plain text password provided by the user.
        - hashed_password (str): The hashed password stored in the database.

    Returns:
        - bool: True if the plain password matches the hashed password, otherwise False.
    """

    return bcrypt_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a plain text password using bcrypt.

    Params:
        - password (str): The plain text password to hash.

    Returns:
        - str: The hashed version of the password.
    """

    return bcrypt_context.hash(password)


def create_access_token(data: dict) -> str:
    """
    Create a JWT access token with an expiration time.

    Params:
        - data (dict): The data to include in the token's payload.

    Returns:
        - str: The encoded JWT access token.
    """

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_ACCESS, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Create a JWT refresh token with an expiration time.

    Params:
        - data (dict): The data to include in the token's payload.

    Returns:
        - str: The encoded JWT refresh token.
    """

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_REFRESH, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str, key: str) -> dict | None:
    """
    Decode a JWT token to retrieve its payload.

    Params:
        - token (str): The encoded JWT token to decode.
        - key (str): The secret key to verify the token.

    Returns:
        - dict | None: The decoded payload if the token is valid.

    Raises:
        - HTTPException: If the token has expired, raises a 403 Forbidden error with the message 'Token expired!'.
        - HTTPException: If the token is invalid or cannot be decoded, raises a 401 Unauthorized error with the message 'Could not validate user'.
    """

    try:
        payload = jwt.decode(token, key, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Token expired!'
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user'
        )
