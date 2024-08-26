from sqlalchemy import Column, Integer, String, ForeignKey, URL
from sqlalchemy.orm import relationship

from app.backend.db import Base


class SocialProfile(Base):
    __tablename__ = 'social_profiles'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    platform = Column(String, nullable=False)
    profile_url = Column(String, nullable=False)
    profile_type = Column(String, nullable=False)

    owner = relationship('User', back_populates='social_profiles')
