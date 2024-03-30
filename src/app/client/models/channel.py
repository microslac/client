from sqlalchemy import Column, String, Boolean, Integer
from app.core.models import UUIDBase, HistoryBase, Base


class Channel(UUIDBase, HistoryBase):
    __tablename__ = "channels"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, index=True)
    team_id = Column(String, nullable=False, index=True)

    is_im = Column(Boolean, default=False)
    is_mpim = Column(Boolean, default=False)
    is_channel = Column(Boolean, default=True)

    is_general = Column(Boolean, default=False)
    is_random = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)
    is_frozen = Column(Boolean, default=False)
    is_private = Column(Boolean, default=False)
    is_shared = Column(Boolean, default=False)
    is_read_only = Column(Boolean, default=False)


class ChannelMember(Base):
    __tablename__ = "channel_members"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    channel_id = Column(String, nullable=False, index=True)
