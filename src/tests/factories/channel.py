import factory
from app.client.models import Channel

from tests.factory import HistoryFactory, FactoryMeta, fake
from tests.utils import shortid


class ChannelFactory(HistoryFactory):
    class Meta(FactoryMeta):
        model = Channel

    id = factory.LazyAttribute(lambda _: shortid("C"))
    creator_id = factory.LazyAttribute(lambda _: shortid("U"))
    name = factory.LazyAttribute(lambda _: fake.company().split().pop(0).lower())
