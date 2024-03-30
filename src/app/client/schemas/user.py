from datetime import datetime
from typing import Optional
from pydantic import Field, ConfigDict, field_serializer
from app.core.schemas import SchemaModel, to_timestamp


class UserProfileModel(SchemaModel):
    model_config = ConfigDict(from_attributes=True)

    user: str = Field(alias="user_id")
    email: str
    phone: Optional[str] = Field(default="")
    skype: Optional[str] = Field(default="")
    title: Optional[str] = Field(default="")
    real_name: Optional[str] = Field(default="")
    display_name: Optional[str] = Field(default="")
    avatar_hash: Optional[str] = Field(default="")
    created: datetime
    updated: datetime

    @field_serializer("created", "updated")
    def serializer_dt(self, dt: datetime):
        return to_timestamp(dt)


class UserModel(SchemaModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    team: str = Field(alias="team_id")
    profile: Optional[UserProfileModel]
    created: datetime
    updated: datetime

    @field_serializer("created", "updated")
    def serializer_dt(self, dt: datetime):
        return to_timestamp(dt)
