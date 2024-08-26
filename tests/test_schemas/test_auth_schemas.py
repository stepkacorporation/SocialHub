import pytest

from pydantic import ValidationError

from datetime import date

from app.schemas.auth import UserCreate, UserResponse, TokenResponse


class TestUserCreateSchema:

    def test_valid_user_create(self):
        valid_data = {
            'email': 'test@example.com',
            'username': 'validusername',
            'password': 'Valid123!',
            'password_repeat': 'Valid123!',
            'phone_number': '+12345678901',
            'date_of_birth': date(2000, 1, 1)
        }
        user = UserCreate(**valid_data)

        assert user.email == valid_data['email']
        assert user.username == valid_data['username']
        assert user.password == valid_data['password']
        assert user.password_repeat == valid_data['password_repeat']
        assert user.phone_number == valid_data['phone_number']

    def test_invalid_email(self):
        invalid_data = {
            'email': 'invalidemail',
            'username': 'validusername',
            'password': 'Valid123!',
            'password_repeat': 'Valid123!',
            'phone_number': '+12345678901',
            'date_of_birth': date(2000, 1, 1)
        }
        with pytest.raises(ValidationError):
            UserCreate(**invalid_data)

    def test_short_username(self):
        invalid_data = {
            'email': 'test@example.com',
            'username': 'abcd',
            'password': 'Valid123!',
            'password_repeat': 'Valid123!',
            'phone_number': '+12345678901',
            'date_of_birth': date(2000, 1, 1)
        }
        with pytest.raises(ValidationError):
            UserCreate(**invalid_data)

    def test_long_username(self):
        invalid_data = {
            'email': 'test@example.com',
            'username': 'a' * 21,
            'password': 'Valid123!',
            'password_repeat': 'Valid123!',
            'phone_number': '+12345678901',
            'date_of_birth': date(2000, 1, 1)
        }
        with pytest.raises(ValidationError):
            UserCreate(**invalid_data)

    def test_invalid_username_pattern(self):
        invalid_data = {
            'email': 'test@example.com',
            'username': 'Invalid_Username',
            'password': 'Valid123!',
            'password_repeat': 'Valid123!',
            'phone_number': '+12345678901',
            'date_of_birth': date(2000, 1, 1)
        }
        with pytest.raises(ValidationError):
            UserCreate(**invalid_data)

    def test_passwords_do_not_match(self):
        invalid_data = {
            'email': 'test@example.com',
            'username': 'validusername',
            'password': 'Valid123!',
            'password_repeat': 'Invalid123!',
            'phone_number': '+12345678901',
            'date_of_birth': date(2000, 1, 1)
        }
        with pytest.raises(ValidationError):
            UserCreate(**invalid_data)

    def test_password_without_uppercase(self):
        invalid_data = {
            'email': 'test@example.com',
            'username': 'validusername',
            'password': 'valid123!',
            'password_repeat': 'valid123!',
            'phone_number': '+12345678901',
            'date_of_birth': date(2000, 1, 1)
        }
        with pytest.raises(ValidationError):
            UserCreate(**invalid_data)

    def test_password_without_digit(self):
        invalid_data = {
            'email': 'test@example.com',
            'username': 'validusername',
            'password': 'Validabc!',
            'password_repeat': 'Validabc!',
            'phone_number': '+12345678901',
            'date_of_birth': date(2000, 1, 1)
        }
        with pytest.raises(ValidationError):
            UserCreate(**invalid_data)

    def test_password_without_special_character(self):
        invalid_data = {
            'email': 'test@example.com',
            'username': 'validusername',
            'password': 'Valid123',
            'password_repeat': 'Valid123',
            'phone_number': '+12345678901',
            'date_of_birth': date(2000, 1, 1)
        }
        with pytest.raises(ValidationError):
            UserCreate(**invalid_data)

    def test_invalid_phone_number(self):
        invalid_data = {
            'email': 'test@example.com',
            'username': 'validusername',
            'password': 'Valid123!',
            'password_repeat': 'Valid123!',
            'phone_number': '12345',
            'date_of_birth': date(2000, 1, 1)
        }
        with pytest.raises(ValidationError):
            UserCreate(**invalid_data)

    def test_missing_email(self):
        invalid_data = {
            'username': 'validusername',
            'password': 'Valid123!',
            'password_repeat': 'Valid123!',
            'phone_number': '12345',
            'date_of_birth': date(2000, 1, 1)
        }
        with pytest.raises(ValidationError):
            UserCreate(**invalid_data)

    def test_missing_username(self):
        invalid_data = {
            'email': 'test@example.com',
            'password': 'Valid123!',
            'password_repeat': 'Valid123!',
            'phone_number': '12345',
            'date_of_birth': date(2000, 1, 1)
        }
        with pytest.raises(ValidationError):
            UserCreate(**invalid_data)

    def test_missing_password(self):
        invalid_data = {
            'email': 'test@example.com',
            'username': 'validusername',
            'password_repeat': 'Valid123!',
            'phone_number': '12345',
            'date_of_birth': date(2000, 1, 1)
        }
        with pytest.raises(ValidationError):
            UserCreate(**invalid_data)

    def test_missing_password_repeat(self):
        invalid_data = {
            'email': 'test@example.com',
            'username': 'validusername',
            'password': 'Valid123!',
            'phone_number': '12345',
            'date_of_birth': date(2000, 1, 1)
        }
        with pytest.raises(ValidationError):
            UserCreate(**invalid_data)

    def test_missing_phone_number(self):
        invalid_data = {
            'email': 'test@example.com',
            'username': 'validusername',
            'password': 'Valid123!',
            'password_repeat': 'Valid123!',
            'date_of_birth': date(2000, 1, 1)
        }
        with pytest.raises(ValidationError):
            UserCreate(**invalid_data)

    def test_missing_date_of_birth(self):
        invalid_data = {
            'email': 'test@example.com',
            'username': 'validusername',
            'password': 'Valid123!',
            'password_repeat': 'Valid123!',
            'phone_number': '12345',
        }
        with pytest.raises(ValidationError):
            UserCreate(**invalid_data)


class TestUserResponseSchema:

    def test_valid_user_response(self):
        valid_data = {
            'id': 1,
            'email': 'test@example.com',
        }
        user = UserResponse(**valid_data)
        assert user.id == valid_data['id']
        assert user.email == valid_data['email']

    def test_invalid_id(self):
        invalid_data = {
            'id': 'invalid_id',
            'email': 'test@example.com',
        }
        with pytest.raises(ValidationError):
            UserResponse(**invalid_data)

    def test_invalid_email_in_response(self):
        invalid_data = {
            'id': 1,
            'email': 'invalidemail',
        }
        with pytest.raises(ValidationError):
            UserResponse(**invalid_data)

    def test_missing_id(self):
        invalid_data = {
            'email': 'invalidemail',
        }
        with pytest.raises(ValidationError):
            UserResponse(**invalid_data)

    def test_missing_email(self):
        invalid_data = {
            'id': 1,
        }
        with pytest.raises(ValidationError):
            UserResponse(**invalid_data)


class TestTokenResponseSchema:

    def test_valid_token_response(self):
        valid_data = {
            'access_token': 'validaccesstoken',
            'refresh_token': 'validrefreshtoken',
            'token_type': 'bearer',
        }
        token = TokenResponse(**valid_data)
        assert token.access_token == valid_data['access_token']
        assert token.refresh_token == valid_data['refresh_token']
        assert token.token_type == valid_data['token_type']

    def test_missing_access_token(self):
        invalid_data = {
            'refresh_token': 'validrefreshtoken',
            'token_type': 'bearer',
        }
        with pytest.raises(ValidationError):
            TokenResponse(**invalid_data)

    def test_missing_refresh_token(self):
        invalid_data = {
            'access_token': 'validaccesstoken',
            'token_type': 'bearer',
        }
        with pytest.raises(ValidationError):
            TokenResponse(**invalid_data)

    def test_missing_token_type(self):
        valid_data = {
            'access_token': 'validaccesstoken',
            'refresh_token': 'validrefreshtoken',
        }
        token = TokenResponse(**valid_data)
        assert token.access_token == valid_data['access_token']
        assert token.refresh_token == valid_data['refresh_token']
        assert token.token_type == 'bearer'
