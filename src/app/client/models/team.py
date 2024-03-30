from sqlalchemy import Column, String, Boolean
from app.core.models import UUIDBase, HistoryBase


class Team(UUIDBase, HistoryBase):
    __tablename__ = "teams"

    id = Column(String, primary_key=True)
    name = Column(String(255), nullable=False)
    domain = Column(String(255), nullable=False, index=True)
    is_open = Column(Boolean, default=True, index=True)
