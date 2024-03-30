from sqlalchemy import Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.models import UUIDBase, HistoryBase, InteractionBase


class User(UUIDBase, HistoryBase):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    name = Column(String(255), nullable=False)
    auth_id = Column(String, nullable=False, index=True)
    team_id = Column(String, nullable=False, index=True)

    # Relationship to UserProfile
    profile = relationship("UserProfile", uselist=False, back_populates="user")

    __table_args__ = (UniqueConstraint("auth_id", "team_id"),)


class UserProfile(UUIDBase, InteractionBase):
    __tablename__ = "user_profiles"

    id = Column(String, primary_key=True)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), default="")
    skype = Column(String(255), default="")
    title = Column(String(255), default="")
    real_name = Column(String(255), nullable=False)
    display_name = Column(String(255), default="")
    avatar_hash = Column(String(255), default="")

    # Relationship to User
    user_id = Column(String, ForeignKey("users.id"), unique=True)
    user = relationship("User", back_populates="profile")
