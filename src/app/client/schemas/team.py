from datetime import datetime
from pydantic import ConfigDict, field_serializer
from app.core.schemas import SchemaModel, ResponseBase, to_timestamp


class TeamModel(SchemaModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    domain: str
    created: datetime
    updated: datetime

    @field_serializer("created", "updated")
    def serializer_dt(self, dt: datetime):
        return to_timestamp(dt)


class TeamData(SchemaModel):
    id: str
    name: str
    domain: str
    creator: str
    active_users: int
    profile_photos: list[str]


class FindTeamsOut(ResponseBase):
    confirmed_email: str
    has_valid_cookie: bool
    current_teams: list[TeamData] = []
    invited_teams: list[TeamData] = []
