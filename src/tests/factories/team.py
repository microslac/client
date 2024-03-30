import factory
from app.client.models import Team

from tests.factory import HistoryFactory, FactoryMeta, fake
from tests.utils import shortid


class TeamFactory(HistoryFactory):
    class Meta(FactoryMeta):
        model = Team

    id = factory.LazyAttribute(lambda _: shortid("T"))
    name = factory.LazyAttribute(lambda _: fake.company())
    domain = factory.LazyAttribute(lambda _: fake.email().split("@", 1).pop())
