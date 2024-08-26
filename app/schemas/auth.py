from pydantic import BaseModel, EmailStr, constr, Field, field_validator, model_validator, ConfigDict

from typing import Self
from datetime import date

USERNAME_MIN_LENGTH = 5
USERNAME_MAX_LENGTH = 20
USERNAME_REGEX = r'^[a-z][a-z0-9]*$'

PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 128
SPECIAL_CHARACTERS = r'!@#$%^&*()-_=+[]{}|;:,.<>?/'

PHONE_NUMBER_REGEX = r'^\+\d{10,15}$'


class UserCreate(BaseModel):
    email: EmailStr = Field(..., description='User email address')
    username: constr(min_length=USERNAME_MIN_LENGTH, max_length=USERNAME_MAX_LENGTH, pattern=USERNAME_REGEX)
    password: str = Field(..., description='User password')
    password_repeat: str = Field(..., description='Password confirmation')
    phone_number: constr(pattern=PHONE_NUMBER_REGEX)
    date_of_birth: date = Field(..., description='Date of birth in YYYY-MM-DD format')

    @field_validator('password')
    @classmethod
    def check_password_complexity(cls, v: str) -> str:
        if len(v) < PASSWORD_MIN_LENGTH:
            raise ValueError(f'Password must be at least {PASSWORD_MIN_LENGTH} characters long')
        if len(v) > PASSWORD_MAX_LENGTH:
            raise ValueError(f'Password must not exceed {PASSWORD_MAX_LENGTH} characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c in SPECIAL_CHARACTERS for c in v):
            raise ValueError('Password must contain at least one special character')
        return v

    @model_validator(mode='after')
    def validate_passwords_match(self) -> Self:
        pw1 = self.password
        pw2 = self.password_repeat
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('Passwords do not match')
        return self


class UserResponse(BaseModel):
    id: int = Field(..., description='Unique identifier of the user')
    email: EmailStr = Field(..., description='User email address')

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str = Field(..., description='Access token for authentication')
    refresh_token: str = Field(..., description='Refresh token for generating a new access token')
    token_type: str = Field(default='bearer', description='Type of the token')

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
                'refresh_token': 'dGhpcy1pcy1hLXRva2VuUzI1NiIsInRLXRv1...',
                'token_type': 'bearer',
            }
        }
    )
