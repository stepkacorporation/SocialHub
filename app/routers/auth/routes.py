from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated

from app.backend.db_depends import get_db
from app.schemas.auth import UserCreate, TokenResponse, UserResponse
from app.models.user import User

from .depends import get_current_user, get_user_by_field
from .utils import get_password_hash, create_access_token, create_refresh_token, verify_password, decode_token
from .consts import SECRET_KEY_REFRESH

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
    summary='Register a new user',
    description='This endpoint registers a new user by accepting email, username, password, and other details. '
                'If successful, it returns an access token and a refresh token for authentication.'
)
async def register_user(
        db: Annotated[AsyncSession, Depends(get_db)],
        user_data: UserCreate
) -> TokenResponse:
    _fields_to_check = {
        'email': user_data.email,
        'username': user_data.username,
        'phone_number': user_data.phone_number
    }

    for field, value in _fields_to_check.items():
        existing_user = await get_user_by_field(field, value, db)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'{" ".join(field.split("_")).capitalize()} already registered'
            )

    result = await db.execute(insert(User).values(
        email=user_data.email,
        username=user_data.username,
        password=get_password_hash(user_data.password),
        phone_number=user_data.phone_number,
        date_of_birth=user_data.date_of_birth
    ).returning(User.id))
    await db.commit()

    new_user_id = result.scalar_one()

    access_token = create_access_token(data={'sub': user_data.email, 'id': new_user_id})
    refresh_token = create_refresh_token(data={'sub': user_data.email, 'id': new_user_id})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type='bearer'
    )


@router.post(
    '/login',
    summary='Log in a user',
    description='This endpoint allows users to authenticate by providing their email and password. '
                'Upon successful authentication, it returns an access token and a refresh token.'
)
async def login_user(
        db: Annotated[AsyncSession, Depends(get_db)],
        user_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> TokenResponse:
    user = await get_user_by_field('email', user_data.username, db)
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect email or password'
        )

    access_token = create_access_token(data={'sub': user.email, 'id': user.id})
    refresh_token = create_refresh_token(data={'sub': user.email, 'id': user.id})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type='bearer'
    )


@router.post(
    '/refresh',
    summary='Refresh access and refresh tokens',
    description='This endpoint allows users to refresh their access and refresh tokens using a valid refresh token. '
                'If the provided token is valid, new tokens are returned.'
)
async def refresh_user_token(token: str) -> TokenResponse:
    payload = decode_token(token, SECRET_KEY_REFRESH)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token'
        )

    id_: str = payload.get('id')
    email: str = payload.get('sub')
    if id_ is None or email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token'
        )

    access_token = create_access_token(data={'sub': email, 'id': id_})
    refresh_token = create_refresh_token(data={'sub': email, 'id': id_})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type='bearer'
    )


@router.get(
    '/me',
    summary='Get current user information',
    description='This endpoint retrieves the current authenticated user\'s information using their access token. '
                'It returns the user\'s details.'
)
async def read_current_user(user: Annotated[UserResponse, Depends(get_current_user)]) -> UserResponse:
    return user
