from datetime import datetime
from typing import List
from pydantic import BaseModel
from app.database import Base


class SchemaModel(BaseModel):
    @classmethod
    def dump(
        cls, instance: List[Base] | Base, /, many: bool = False, **kwargs
    ) -> List[dict] | dict:
        def dump(ins):
            return cls.model_validate(ins).model_dump(**kwargs)

        if many:
            return [dump(ins) for ins in instance]
        return dump(instance)


class ResponseBase(BaseModel):
    ok: bool


def to_timestamp(dt: datetime):
    return round(dt.timestamp() * 1e3)
