from datetime import datetime
from typing import Optional
from pydantic import Field, ConfigDict, field_serializer
from app.core.schemas import SchemaModel, to_timestamp


class ChannelModel(SchemaModel):
    id: str
    name: str
    team: str = Field(alias="team_id")
    creator: str = Field(alias="creator_id")
    updater: Optional[str] = Field(alias="updater_id", default="")
    created: datetime
    updated: datetime

    is_im: bool
    is_mpim: bool
    is_channel: bool

    is_general: bool
    is_random: bool
    is_archived: bool
    is_frozen: bool
    is_private: bool
    is_shared: bool
    is_read_only: bool

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("created", "updated")
    def serializer_dt(self, dt: datetime):
        return to_timestamp(dt)
