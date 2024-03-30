import factory
from app.client.models import User

from tests.factory import HistoryFactory, FactoryMeta, fake
from tests.utils import shortid


class UserFactory(HistoryFactory):
    class Meta(FactoryMeta):
        model = User

    id = factory.LazyAttribute(lambda _: shortid("U"))
    auth_id = factory.LazyAttribute(lambda _: shortid("A"))
    team_id = factory.LazyAttribute(lambda _: shortid("T"))
    name = factory.LazyAttribute(lambda _: fake.name())
