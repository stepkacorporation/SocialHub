import pytest

from fastapi import status

from httpx import AsyncClient

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import TokenResponse, UserResponse
from app.schemas.social_profiles import SocialProfileResponse
from app.models.user import User
from app.models.social_profile import SocialProfile

pytestmark = pytest.mark.anyio


class TestGetSocialProfiles:

    async def test_get_social_profiles_success(self, client: AsyncClient, test_user: User, test_social_profiles: list[SocialProfile]):
        payload = {
            'username': test_user.email,
            'password': 'Newpassword1!'
        }
        response = await client.post('/auth/login', data=payload)
        tokens = TokenResponse(**response.json())

        headers = {'Authorization': f'Bearer {tokens.access_token}'}
        response = await client.get('/social_profiles/', headers=headers)
        assert response.status_code == status.HTTP_200_OK

        profiles = response.json()
        assert len(profiles) == len(test_social_profiles)

        profile_ids = {profile['id'] for profile in profiles}
        test_profile_ids = {profile.id for profile in test_social_profiles}
        assert profile_ids == test_profile_ids

    async def test_get_social_profiles_no_auth(self, client: AsyncClient):
        response = await client.get('/social_profiles/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Not authenticated'}


class TestCreateSocialProfile:
    async def test_create_social_profile_success(self, client: AsyncClient, test_user: User):
        payload = {
            'username': test_user.email,
            'password': 'Newpassword1!'
        }
        response = await client.post('/auth/login', data=payload)
        tokens = TokenResponse(**response.json())

        headers = {'Authorization': f'Bearer {tokens.access_token}'}
        profile_data = {
            'platform': 'Twitter',
            'profile_url': 'https://twitter.com/testuser',
            'profile_type': 'personal'
        }
        response = await client.post('/social_profiles/create', json=profile_data, headers=headers)
        assert response.status_code == status.HTTP_201_CREATED

        profile = SocialProfileResponse(**response.json())
        assert profile.platform == profile_data['platform']
        assert str(profile.profile_url) == profile_data['profile_url']
        assert profile.profile_type == profile_data['profile_type']

    async def test_create_social_profile_user_not_found(self, client: AsyncClient):
        headers = {'Authorization': 'Bearer invalidtoken'}
        profile_data = {
            'platform': 'Facebook',
            'profile_url': 'https://facebook.com/testuser',
            'profile_type': 'business'
        }
        response = await client.post('/social_profiles/create', json=profile_data, headers=headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate user'}


class TestUpdateSocialProfile:

    async def test_update_social_profile_success(self, client: AsyncClient, test_user: User, test_social_profile: SocialProfile):
        payload = {
            'username': test_user.email,
            'password': 'Newpassword1!'
        }
        response = await client.post('/auth/login', data=payload)
        tokens = TokenResponse(**response.json())

        headers = {'Authorization': f'Bearer {tokens.access_token}'}
        update_data = {
            'platform': 'LinkedIn',
            'profile_url': 'https://linkedin.com/in/testuser',
            'profile_type': 'professional'
        }
        response = await client.put(f'/social_profiles/{test_social_profile.id}', headers=headers, json=update_data)
        assert response.status_code == status.HTTP_200_OK

        updated_profile = SocialProfileResponse(**response.json())
        print(updated_profile)
        assert updated_profile.platform == update_data['platform']
        assert str(updated_profile.profile_url) == update_data['profile_url']
        assert updated_profile.profile_type == update_data['profile_type']

    async def test_update_social_profile_not_found(self, client: AsyncClient, test_user: User):
        payload = {
            'username': test_user.email,
            'password': 'Newpassword1!'
        }
        response = await client.post('/auth/login', data=payload)
        tokens = TokenResponse(**response.json())

        headers = {'Authorization': f'Bearer {tokens.access_token}'}
        update_data = {
            'platform': 'LinkedIn',
            'profile_url': 'https://linkedin.com/in/testuser',
            'profile_type': 'professional'
        }
        response = await client.put('/social_profiles/9999', headers=headers, json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {'detail': 'Profile not found'}


class TestDeleteSocialProfile:

    async def test_delete_social_profile_success(self, client: AsyncClient, test_user: User, test_social_profile: SocialProfile):
        payload = {
            'username': test_user.email,
            'password': 'Newpassword1!'
        }
        response = await client.post('/auth/login', data=payload)
        tokens = TokenResponse(**response.json())

        headers = {'Authorization': f'Bearer {tokens.access_token}'}
        response = await client.delete(f'/social_profiles/{test_social_profile.id}', headers=headers)
        assert response.status_code == status.HTTP_200_OK

        deleted_profile = SocialProfileResponse(**response.json())
        assert deleted_profile.id == test_social_profile.id

        result = await client.get('/social_profiles/', headers=headers)
        profiles = result.json()
        assert all(profile['id'] != test_social_profile.id for profile in profiles)

    async def test_delete_social_profile_not_found(self, client: AsyncClient, test_user: User):
        payload = {
            'username': test_user.email,
            'password': 'Newpassword1!'
        }
        response = await client.post('/auth/login', data=payload)
        tokens = TokenResponse(**response.json())

        headers = {'Authorization': f'Bearer {tokens.access_token}'}
        response = await client.delete('/social_profiles/9999', headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {'detail': 'Profile not found'}
