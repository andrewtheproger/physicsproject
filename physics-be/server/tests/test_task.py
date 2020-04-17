from .test_init import init_db
import pytest


@pytest.fixture
def client():
    for i in init_db():
        yield i


def test_empty_db(client):
    rv = client.get('/api/tasks')

    assert len(rv.json) == 1