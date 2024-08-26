import pytest

from fastapi import status

from httpx import AsyncClient

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import TokenResponse, UserResponse
from app.models.user import User

pytestmark = pytest.mark.anyio


class TestRegisterUser:

    async def test_register_success(self, client: AsyncClient, db_session: AsyncSession):
        payload = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'Newpassword1!',
            'password_repeat': 'Newpassword1!',
            'phone_number': '+1234567891',
            'date_of_birth': '2000-01-01'
        }
        response = await client.post('/auth/register', json=payload)
        assert response.status_code == status.HTTP_201_CREATED

        tokens = TokenResponse(**response.json())
        assert tokens.access_token
        assert tokens.refresh_token
        assert tokens.token_type == 'bearer'

        user = await db_session.scalar(select(User).where(User.email == payload['email']))
        assert user is not None

    async def test_register_user_email_already_exists(self, client: AsyncClient, test_user: User):
        payload = {
            'email': test_user.email,
            'username': 'anotheruser',
            'password': 'Newpassword1!',
            'password_repeat': 'Newpassword1!',
            'phone_number': '+1234567892',
            'date_of_birth': '2000-01-01'
        }
        response = await client.post('/auth/register', json=payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'detail': 'Email already registered'}

    async def test_register_user_username_already_exists(self, client: AsyncClient, test_user: User):
        payload = {
            'email': 'another@example.com',
            'username': test_user.username,
            'password': 'Newpassword1!',
            'password_repeat': 'Newpassword1!',
            'phone_number': '+1234567892',
            'date_of_birth': '2000-01-01'
        }
        response = await client.post('/auth/register', json=payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'detail': 'Username already registered'}

    async def test_register_user_phone_number_already_exists(self, client: AsyncClient, test_user: User):
        payload = {
            'email': 'another@example.com',
            'username': 'anotheruser',
            'password': 'Newpassword1!',
            'password_repeat': 'Newpassword1!',
            'phone_number': test_user.phone_number,
            'date_of_birth': '2000-01-01'
        }
        response = await client.post('/auth/register', json=payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'detail': 'Phone number already registered'}


class TestLoginUser:

    async def test_login_user_success(self, client: AsyncClient, test_user: User):
        payload = {
            'username': test_user.email,
            'password': 'Newpassword1!'
        }
        response = await client.post('/auth/login', data=payload)
        assert response.status_code == status.HTTP_200_OK

        tokens = TokenResponse(**response.json())
        assert tokens.access_token
        assert tokens.refresh_token
        assert tokens.token_type == 'bearer'

    async def test_user_login_incorrect_username(self, client: AsyncClient):
        payload = {
            'username': 'wronguser',
            'password': 'Newpassword1!'
        }
        response = await client.post('/auth/login', data=payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'detail': 'Incorrect email or password'}

    async def test_user_login_incorrect_password(self, client: AsyncClient, test_user: User):
        payload = {
            'username': test_user.username,
            'password': 'wrongpassword'
        }
        response = await client.post('/auth/login', data=payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'detail': 'Incorrect email or password'}


class TestRefreshUserToken:

    async def test_refresh_token_success(self, client: AsyncClient, db_session: AsyncSession, test_user: User):
        payload = {
          'username': test_user.email,
          'password': 'Newpassword1!',
        }
        response = await client.post('/auth/login', data=payload)
        tokens = TokenResponse(**response.json())

        refresh_response = await client.post(f'/auth/refresh?token={tokens.refresh_token}')
        assert refresh_response.status_code == status.HTTP_200_OK

        refresh_tokens = TokenResponse(**refresh_response.json())
        assert refresh_tokens.access_token
        assert refresh_tokens.refresh_token
        assert refresh_tokens.token_type == 'bearer'

    async def test_refresh_token_invalid(self, client: AsyncClient):
        response = await client.post('/auth/refresh?token=invalidtoken')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate user'}


class TestReadCurrentUser:
    async def test_read_current_user_success(self, client: AsyncClient, test_user: User):
        payload = {
            'username': test_user.email,
            'password': 'Newpassword1!'
        }
        response = await client.post('/auth/login', data=payload)
        tokens = TokenResponse(**response.json())

        headers = {'Authorization': f'Bearer {tokens.access_token}'}
        me_response = await client.get('/auth/me', headers=headers)
        assert me_response.status_code == status.HTTP_200_OK

        user_data = UserResponse(**me_response.json())
        assert user_data.email == test_user.email
        assert user_data.id == test_user.id

    async def test_read_current_user_no_token(self, client: AsyncClient):
        response = await client.get('/auth/me')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Not authenticated'}

    async def test_read_current_user_invalid_token(self, client: AsyncClient):
        headers = {'Authorization': 'Bearer invalidtoken'}
        response = await client.get('/auth/me', headers=headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate user'}
