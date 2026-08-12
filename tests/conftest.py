import fastapi.testclient
import pytest

from app import main


@pytest.fixture(scope='session')
def client():
    return fastapi.testclient.TestClient(main.api)
