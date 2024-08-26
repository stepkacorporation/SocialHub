import pytest

from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt
from datetime import date, timedelta, datetime, timezone

from app.models.user import User
from app.routers.auth.depends import get_user_by_field, get_current_user
from app.routers.auth.consts import SECRET_KEY_ACCESS, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pytestmark = pytest.mark.anyio


def _create_test_access_token(data: dict = None, expiration_delta: timedelta = None):
    if data is None:
        data = {}
    to_encode = data.copy()
    if expiration_delta:
        to_encode.update({'exp': datetime.now(timezone.utc) + expiration_delta})
    return jwt.encode(to_encode, SECRET_KEY_ACCESS, ALGORITHM)


class TestGetUserByField:

    async def test_get_user_by_valid_field_and_value(self, db_session: AsyncSession):
        user = User(
            email='test@example.com',
            username='testuser',
            password='securepassword',
            phone_number='+1234567890',
            date_of_birth=date(1990, 1, 1)
        )
        db_session.add(user)
        await db_session.commit()

        retrieved_user = await get_user_by_field('email', 'test@example.com', db_session)
        assert retrieved_user is not None
        assert retrieved_user.email == 'test@example.com'
        assert retrieved_user.id == user.id

    async def test_get_user_by_invalid_field(self, db_session: AsyncSession):
        with pytest.raises(ValueError, match='\'invalid_field\' is not a valid attribute of User'):
            await get_user_by_field('invalid_field', 'value', db_session)

    async def test_get_user_by_non_unique_field(self, db_session: AsyncSession):
        user1 = User(
            email='user1@example.com',
            username='user1',
            password='password',
            phone_number='+1234567890',
            date_of_birth=date(1990, 1, 1)
        )
        user2 = User(
            email='user2@example.com',
            username='user2',
            password='password',
            phone_number='+0987654321',
            date_of_birth=date(1990, 1, 1)
        )
        db_session.add_all([user1, user2])
        await db_session.commit()

        with pytest.raises(
                ValueError,
                match=f'Multiple records found for field \'date_of_birth\' with value \'1990-01-01\'.'
        ):
            await get_user_by_field('date_of_birth', date(1990, 1, 1), db_session)

    async def test_get_user_by_non_existing_value(self, db_session: AsyncSession):
        user = await get_user_by_field('email', 'non_existing@example.com', db_session)
        assert user is None


class TestGetCurrentUser:

    async def test_get_current_user_success(self, db_session: AsyncSession, test_user: User):
        token = _create_test_access_token(
            {'id': test_user.id, 'sub': test_user.email},
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        user_response = await get_current_user(token)
        assert user_response.id == test_user.id
        assert user_response.email == test_user.email

    async def test_get_current_user_invalid_token(self):
        invalid_token = 'invalid_token'

        with pytest.raises(HTTPException) as error:
            await get_current_user(invalid_token)
        assert error.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert error.value.detail == 'Could not validate user'

    async def test_get_current_user_token_expired(self, db_session: AsyncSession, test_user: User):
        expired_token = _create_test_access_token(
            {'id': test_user.id, 'sub': test_user.email},
            timedelta(seconds=-1)
        )

        with pytest.raises(HTTPException) as error:
            await get_current_user(expired_token)
        assert error.value.status_code == status.HTTP_403_FORBIDDEN
        assert error.value.detail == 'Token expired!'

    async def test_get_current_user_missing_fields(self, test_user: User):
        incomplete_token = _create_test_access_token(
            {'id': test_user.id},
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        with pytest.raises(HTTPException) as error:
            await get_current_user(incomplete_token)
        assert error.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert error.value.detail == 'Could not validate user'
