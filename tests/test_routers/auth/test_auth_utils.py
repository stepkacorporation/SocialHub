import pytest

from fastapi import HTTPException, status

from jose import jwt
from datetime import datetime, timedelta, timezone

from app.routers.auth.utils import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.routers.auth.consts import (
    SECRET_KEY_ACCESS,
    SECRET_KEY_REFRESH,
)


class TestVerifyPasswordFunction:

    def test_verify_passwrd_correct(self):
        password = 'my_secret_password'
        hashed_password = get_password_hash(password)
        assert verify_password(password, hashed_password) is True

    def test_verify_password_incorrect(self):
        password = 'my_secret_password'
        wrong_password = 'wrong_password'
        hashed_password = get_password_hash(password)
        assert verify_password(wrong_password, hashed_password) is False

    def test_verify_password_empty_password(self):
        password = ''
        hashed_password = get_password_hash(password)
        assert verify_password(password, hashed_password) is True

    def test_verify_password_empty_hashed_password(self):
        password = 'my_secret_password'
        hashed_password = get_password_hash('')
        assert verify_password(password, hashed_password) is False


class TestGetPasswordHashFunction:

    def test_get_password_hash(self):
        password = 'my_secret_password'
        hashed_password = get_password_hash(password)
        assert isinstance(hashed_password, str)
        assert hashed_password != password
        assert len(hashed_password) > 0

    def test_get_password_hash_empty_password(self):
        password = ''
        hashed_password = get_password_hash(password)
        assert isinstance(hashed_password, str)
        assert hashed_password != password
        assert len(hashed_password) > 0


class TestCreateAccessTokenFunction:

    def test_create_access_token(self):
        data = {'user_id': 123}
        token = create_access_token(data)
        decoded_data = decode_token(token, SECRET_KEY_ACCESS)
        assert decoded_data['user_id'] == 123
        assert 'exp' in decoded_data
        assert datetime.now(timezone.utc) < datetime.fromtimestamp(decoded_data['exp'], tz=timezone.utc)


class TestCreateRefreshTokenFunction:

    def test_create_refresh_token(self):
        data = {'user_id': 123}
        token = create_refresh_token(data)
        decoded_data = decode_token(token, SECRET_KEY_REFRESH)
        assert decoded_data['user_id'] == 123
        assert 'exp' in decoded_data
        assert datetime.now(timezone.utc) < datetime.fromtimestamp(decoded_data['exp'], tz=timezone.utc)


class TestDecodeTokenFunction:

    def test_decode_token_valid_access_token(self):
        data = {'user_id': 123}
        token = create_access_token(data)
        decoded_data = decode_token(token, SECRET_KEY_ACCESS)
        assert decoded_data['user_id'] == 123

    def test_decode_token_valid_refresh_token(self):
        data = {'user_id': 123}
        token = create_refresh_token(data)
        decoded_data = decode_token(token, SECRET_KEY_REFRESH)
        assert decoded_data['user_id'] == 123

    def test_decode_token_invalid_key_for_access_token(self):
        data = {'user_id': 123}
        token = create_access_token(data)
        with pytest.raises(HTTPException) as error:
            decode_token(token, 'wrong_key')
        assert error.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert error.value.detail == 'Could not validate user'

    def test_decode_token_invalid_key_for_refresh_token(self):
        data = {'user_id': 123}
        token = create_refresh_token(data)
        with pytest.raises(HTTPException) as error:
            decode_token(token, 'wrong_key')
        assert error.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert error.value.detail == 'Could not validate user'

    def test_decode_token_expired_token(self):
        data = {'user_id': 123}
        expired_token = jwt.encode(
            {**data, 'exp': datetime.now(timezone.utc) - timedelta(seconds=1)},
            SECRET_KEY_ACCESS,
            algorithm='HS256'
        )
        with pytest.raises(HTTPException) as error:
            decode_token(expired_token, SECRET_KEY_ACCESS)
        assert error.value.status_code == status.HTTP_403_FORBIDDEN
        assert error.value.detail == 'Token expired!'

    def test_decode_token_invalid_token(self):
        invalid_token = 'invalid_token'

        with pytest.raises(HTTPException) as error:
            decode_token(invalid_token, SECRET_KEY_ACCESS)
        assert error.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert error.value.detail == 'Could not validate user'

        with pytest.raises(HTTPException) as error:
            decode_token(invalid_token, SECRET_KEY_REFRESH)
        assert error.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert error.value.detail == 'Could not validate user'
