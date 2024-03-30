import json
import pytest
from types import SimpleNamespace
from fastapi.testclient import TestClient
from tests.common import Session
from app.main import app
from app.database import db_session


class TestBase:
    client: TestClient
    session: Session

    @pytest.fixture(autouse=True)
    def setup(self, request, settings):
        self.client = TestClient(
            app, headers={"Authorization": f"Token {settings.access_token}"}
        )
        self.session = Session()

        def override_db_session():
            try:
                yield self.session
            finally:
                self.session.close()

        app.dependency_overrides[db_session] = override_db_session  # noqa

        def teardown():
            self.session.rollback()
            Session.remove()

        request.addfinalizer(teardown)

    def objectify(
        self, *dicts: dict, default=None
    ) -> SimpleNamespace | list[SimpleNamespace]:
        def convert(data: dict):
            return json.loads(
                json.dumps(data), object_hook=lambda d: SimpleNamespace(**d)
            )

        objects = [convert(d) for d in dicts]
        if len(objects) == 1:
            return next(iter(objects), default)
        return objects
