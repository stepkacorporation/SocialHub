import pytest

from pydantic import ValidationError
from pydantic.networks import HttpUrl

from app.schemas.social_profiles import SocialProfileCreate, SocialProfileUpdate, SocialProfileResponse


class TestSocialProfileCreateSchema:

    def test_valid_social_profile_create(self):
        valid_data = {
            'platform': 'Facebook',
            'profile_url': 'https://www.facebook.com/group/123456789',
            'profile_type': 'group',
        }
        profile = SocialProfileCreate(**valid_data)
        assert profile.platform == 'Facebook'
        assert profile.profile_url == HttpUrl('https://www.facebook.com/group/123456789')
        assert profile.profile_type == 'group'

    def test_invalid_profile_type(self):
        invalid_data = {
            'platform': 'Facebook',
            'profile_url': 'https://www.facebook.com/group/123456789',
            'profile_type': 'unknown_type',
        }
        with pytest.raises(ValidationError):
            SocialProfileCreate(**invalid_data)

    def test_missing_profile_type(self):
        valid_data = {
            'platform': 'Facebook',
            'profile_url': 'https://www.facebook.com/group/123456789',
        }
        with pytest.raises(ValidationError):
            SocialProfileCreate(**valid_data)

    def test_missing_profile_url(self):
        invalid_data = {
            'platform': 'Facebook',
            'profile_type': 'group',
        }
        with pytest.raises(ValidationError):
            SocialProfileCreate(**invalid_data)

    def test_missing_platform(self):
        invalid_data = {
            'profile_url': 'https://www.facebook.com/group/123456789',
            'profile_type': 'unknown_type',
        }
        with pytest.raises(ValidationError):
            SocialProfileCreate(**invalid_data)

    def test_invalid_profile_url(self):
        invalid_data = {
            'platform': 'Facebook',
            'profile_url': 'not_a_url',
            'profile_type': 'group',
        }
        with pytest.raises(ValidationError):
            SocialProfileCreate(**invalid_data)

    def test_short_platform_name(self):
        invalid_data = {
            'platform': 'ab',
            'profile_url': 'https://www.facebook.com/group/123456789',
            'profile_type': 'group',
        }
        with pytest.raises(ValidationError):
            SocialProfileCreate(**invalid_data)

    def test_capitalize_platform_name(self):
        valid_data = {
            'platform': 'linkedIn',
            'profile_url': 'https://www.facebook.com/group/123456789',
            'profile_type': 'group',
        }
        profile = SocialProfileCreate(**valid_data)
        assert profile.platform == valid_data['platform'][0].upper() + valid_data['platform'][1:]


class TestSocialProfileUpdateSchema:

    def test_valid_social_profile_update_with_all_fields(self):
        valid_data = {
            'platform': 'Twitter',
            'profile_url': 'https://twitter.com/some_profile',
            'profile_type': 'personal',
        }
        profile = SocialProfileUpdate(**valid_data)
        assert profile.platform == 'Twitter'
        assert profile.profile_url == HttpUrl('https://twitter.com/some_profile')
        assert profile.profile_type == 'personal'

    def test_valid_social_profile_update_with_some_fields(self):
        valid_data = {
            'platform': 'LinkedIn',
            'profile_type': 'professional',
        }
        profile = SocialProfileUpdate(**valid_data)
        assert profile.platform == 'LinkedIn'
        assert profile.profile_type == 'professional'
        assert profile.profile_url is None

    def test_missing_optional_fields(self):
        valid_data = {
            'platform': None,
            'profile_url': None,
            'profile_type': None,
        }
        profile = SocialProfileUpdate(**valid_data)
        assert profile.platform is None
        assert profile.profile_url is None
        assert profile.profile_type is None

    def test_invalid_profile_url_in_update(self):
        invalid_data = {
            'profile_url': 'not_a_url',
        }
        with pytest.raises(ValidationError):
            SocialProfileUpdate(**invalid_data)

    def test_invalid_profile_type_in_update(self):
        invalid_data = {
            'profile_type': 'unknown_type',
        }
        with pytest.raises(ValidationError):
            SocialProfileUpdate(**invalid_data)

    def test_short_platform_name_in_update(self):
        invalid_data = {
            'platform': 'ab',
        }
        with pytest.raises(ValidationError):
            SocialProfileUpdate(**invalid_data)


class TestSocialProfileResponseSchema:

    def test_valid_social_profile_response(self):
        valid_data = {
            'id': 1,
            'platform': 'Instagram',
            'profile_url': 'https://www.instagram.com/some_profile',
            'profile_type': 'personal',
        }
        profile = SocialProfileResponse(**valid_data)
        assert profile.id == 1
        assert profile.platform == 'Instagram'
        assert profile.profile_url == HttpUrl('https://www.instagram.com/some_profile')
        assert profile.profile_type == 'personal'

    def test_missing_id_in_response(self):
        invalid_data = {
            'platform': 'Instagram',
            'profile_url': 'https://www.instagram.com/some_profile',
            'profile_type': 'personal',
        }
        with pytest.raises(ValidationError):
            SocialProfileResponse(**invalid_data)

    def test_invalid_id_in_response(self):
        invalid_data = {
            'id': 'invalid_id',
            'platform': 'Instagram',
            'profile_url': 'https://www.instagram.com/some_profile',
            'profile_type': 'personal',
        }
        with pytest.raises(ValidationError):
            SocialProfileResponse(**invalid_data)

    def test_invalid_profile_url_in_response(self):
        invalid_data = {
            'id': 1,
            'platform': 'Instagram',
            'profile_url': 'not_a_url',
            'profile_type': 'personal',
        }
        with pytest.raises(ValidationError):
            SocialProfileResponse(**invalid_data)

    def test_invalid_profile_type_in_response(self):
        invalid_data = {
            'id': 1,
            'platform': 'Instagram',
            'profile_url': 'https://www.instagram.com/some_profile',
            'profile_type': 'unknown_type',
        }
        with pytest.raises(ValidationError):
            SocialProfileResponse(**invalid_data)

    def test_short_platform_name_in_response(self):
        invalid_data = {
            'id': 1,
            'platform': 'df',
            'profile_url': 'https://www.instagram.com/some_profile',
            'profile_type': 'unknown_type',
        }
        with pytest.raises(ValidationError):
            SocialProfileResponse(**invalid_data)
