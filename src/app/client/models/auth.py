from sqlalchemy import Column, String
from app.core.models import UUIDBase


class Auth(UUIDBase):
    __tablename__ = "auths"

    id = Column(String, primary_key=True)
    email = Column(String, nullable=False, index=True)
