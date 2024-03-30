import pytest
from app.settings.test import TestSettings

test_settings = TestSettings()


@pytest.fixture()
def settings() -> TestSettings:
    return test_settings
