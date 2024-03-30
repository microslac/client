import factory
from uuid import uuid4
from datetime import datetime
from factory.alchemy import SQLAlchemyModelFactory
from tests.common import Session
from faker import Faker

fake = Faker()


class BaseFactory(SQLAlchemyModelFactory):
    uuid = factory.LazyAttribute(lambda _: uuid4())


class HistoryFactory(BaseFactory):
    created = factory.LazyAttribute(lambda _: datetime.utcnow().isoformat())
    updated = factory.LazyAttribute(lambda _: datetime.utcnow().isoformat())
    deleted = None

    creator_id = ""
    updater_id = ""
    deleter_id = ""


class FactoryMeta:
    sqlalchemy_session = Session
