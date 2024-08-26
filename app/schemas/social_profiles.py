from pydantic import BaseModel, constr, Field, HttpUrl, field_validator, ConfigDict

MIN_LENGTH_PLATFORM = 3

VALID_PROFILE_TYPES = {
    'personal', 'business', 'creator', 'brand', 'organization', 'public_figure',
    'group', 'page', 'channel', 'nonprofit', 'artist', 'support', 'event',
    'media', 'forum', 'educational', 'professional'
}


class SocialProfileBase(BaseModel):
    platform: constr(strip_whitespace=True, min_length=MIN_LENGTH_PLATFORM) = Field(..., description='Platform for the social profile')
    profile_url: HttpUrl = Field(..., description='URL of the social profile')
    profile_type: constr(strip_whitespace=True, to_lower=True) = Field(..., description='Type of the social profile')

    @field_validator('platform', mode='before')
    @classmethod
    def capitalize_platform(cls, v: str | None) -> str | None:
        if v is not None:
            return v[0].upper() + v[1:]
        return v

    @field_validator('profile_type')
    @classmethod
    def validate_profile_type(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.lower()
            if v not in VALID_PROFILE_TYPES:
                raise ValueError(f'Invalid profile type. Valid options are: {", ".join(VALID_PROFILE_TYPES)}')
        return v


class SocialProfileCreate(SocialProfileBase):
    pass


class SocialProfileUpdate(SocialProfileBase):
    platform: constr(strip_whitespace=True, min_length=MIN_LENGTH_PLATFORM) | None = Field(None, description='Platform for the social profile')
    profile_url: HttpUrl | None = Field(None, description='URL of the social profile')
    profile_type: constr(strip_whitespace=True, to_lower=True) | None = Field(None,
                                                                              description='Type of the social profile')


class SocialProfileResponse(SocialProfileBase):
    id: int = Field(..., description='Unique identifier of the social profile')

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example': {
                'id': 1,
                'platform': 'Facebook',
                'profile_url': 'https://www.facebook.com/group/123456789',
                'profile_type': 'group',
            }
        }
    )
