from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from app.backend.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    date_of_birth = Column(Date, nullable=False)

    social_profiles = relationship('SocialProfile', back_populates='owner')
