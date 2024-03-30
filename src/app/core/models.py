from app.database import Base
from sqlalchemy import Column, DateTime, String, UUID
from sqlalchemy.sql import func
from uuid import uuid4


class UUIDBase(Base):
    __abstract__ = True

    uuid = Column(UUID, unique=True, default=uuid4)


class InteractionBase(Base):
    __abstract__ = True

    created = Column(DateTime, nullable=False, server_default=func.now())
    updated = Column(DateTime, nullable=False, onupdate=func.now())

    creator_id = Column(String, nullable=True)
    updater_id = Column(String, nullable=True)


class HistoryBase(Base):
    __abstract__ = True

    created = Column(DateTime, nullable=False, server_default=func.now())
    updated = Column(DateTime, nullable=False, onupdate=func.now())
    deleted = Column(DateTime, nullable=True)

    creator_id = Column(String, nullable=True)
    updater_id = Column(String, nullable=True)
    deleter_id = Column(String, nullable=True)
