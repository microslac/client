import factory
from app.client.models import Auth

from tests.factory import BaseFactory, FactoryMeta, fake
from tests.utils import shortid


class AuthFactory(BaseFactory):
    class Meta(FactoryMeta):
        model = Auth

    id = factory.LazyAttribute(lambda _: shortid("A"))
    email = factory.LazyAttribute(lambda _: fake.email())
