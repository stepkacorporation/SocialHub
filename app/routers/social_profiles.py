from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated

from app.backend.db_depends import get_db
from app.routers.auth.depends import get_current_user, get_user_by_field
from app.schemas.social_profiles import SocialProfileCreate, SocialProfileResponse, SocialProfileUpdate
from app.schemas.auth import UserResponse
from app.models.social_profile import SocialProfile

router = APIRouter(prefix='/social_profiles', tags=['social_profiles'])


@router.get(
    '/',
    summary='Get all social profiles',
    description='This endpoint retrieves all social profiles associated with the current authenticated user. '
                'It returns a list of social profiles.',
    response_model=list[SocialProfileResponse]
)
async def get_social_profiles(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[UserResponse, Depends(get_current_user)]
):
    profiles = await db.scalars(select(SocialProfile).where(SocialProfile.user_id == user.id))
    return profiles.all()


@router.post(
    '/create',
    summary='Create a new social profile',
    description='This endpoint creates a new social profile for the current authenticated user. '
                'It requires the profile data and returns the created social profile.',
    status_code=status.HTTP_201_CREATED,
    response_model=SocialProfileResponse
)
async def create_social_profile(
        db: Annotated[AsyncSession, Depends(get_db)],
        user: Annotated[UserResponse, Depends(get_current_user)],
        profile_data: SocialProfileCreate
):
    user = await get_user_by_field('email', user.email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )

    new_profile = SocialProfile(
        user_id=user.id,
        platform=profile_data.platform,
        profile_url=str(profile_data.profile_url),
        profile_type=profile_data.profile_type
    )
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)
    return new_profile


@router.put(
    '/{profile_id}',
    summary='Update a social profile',
    description='This endpoint updates an existing social profile belonging to the current authenticated user. '
                'It requires the profile ID and updated data, and returns the updated social profile.',
    response_model=SocialProfileResponse
)
async def update_social_profile(
        db: Annotated[AsyncSession, Depends(get_db)],
        user: Annotated[UserResponse, Depends(get_current_user)],
        profile_id: int,
        profile_data: SocialProfileUpdate
):
    profile = await db.get(SocialProfile, profile_id)
    if profile is None or profile.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Profile not found'
        )

    if profile_data.platform is not None:
        profile.platform = profile_data.platform
    if profile_data.profile_url is not None:
        profile.profile_url = str(profile_data.profile_url)
    if profile_data.profile_type is not None:
        profile.profile_type = profile_data.profile_type

    await db.commit()
    await db.refresh(profile)
    return profile


@router.delete(
    '/{profile_id}',
    summary='Delete a social profile',
    description='This endpoint deletes an existing social profile belonging to the current authenticated user. '
                'It requires the profile ID and returns the deleted social profile.',
    response_model=SocialProfileResponse
)
async def delete_social_profile(
        db: Annotated[AsyncSession, Depends(get_db)],
        user: Annotated[UserResponse, Depends(get_current_user)],
        profile_id: int
):
    profile = await db.get(SocialProfile, profile_id)
    if profile is None or profile.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Profile not found'
        )

    await db.delete(profile)
    await db.commit()
    return profile
