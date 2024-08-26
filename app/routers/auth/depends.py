from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated
from datetime import datetime, timezone

from app.models.user import User
from app.schemas.auth import UserResponse

from .utils import decode_token
from .consts import SECRET_KEY_ACCESS

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login', scheme_name='JWT')


async def get_user_by_field(field_name: str, value: any, db: AsyncSession) -> User | None:
    """
    Retrieve a user from the database by a specified field and value.

    Params:
        - field_name (str): The name of the field to search by (e.g., 'email', 'username', 'phone_number').
        - value (any): The value to search for in the specified field.
        - db (AsyncSession): The database session dependency.

    Returns:
        - User | None: The User object if found, otherwise None.

    Raises:
        - ValueError: If the field_name does not exist in the User model or if multiple records are found.
    """

    if not hasattr(User, field_name):
        raise ValueError(f'\'{field_name}\' is not a valid attribute of User')

    result = await db.execute(select(User).where(getattr(User, field_name) == value))
    users = result.scalars().all()

    if len(users) > 1:
        raise ValueError(f'Multiple records found for field \'{field_name}\' with value \'{value}\'.')

    return users[0] if users else None


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserResponse:
    """
    Retrieve the current authenticated user from the provided JWT token.

    Params:
        - token (str): The JWT token provided by the user.

    Returns:
        - UserResponse: The current user's ID and email.

    Raises:
        - HTTPException: If the token is invalid, expired, or cannot be decoded.
    """

    payload = decode_token(token, SECRET_KEY_ACCESS)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    id_: str = payload.get('id')
    email: str = payload.get('sub')
    expire: int = payload.get('exp')

    if id_ is None or email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    if expire is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No access token supplied',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    if datetime.now(timezone.utc) > datetime.fromtimestamp(expire, tz=timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Token expired!'
        )

    return UserResponse(id=id_, email=email)
