from .test_init import init_db, snapshot, get_expected
import pytest


@pytest.fixture
def client():
    for i in init_db():
        yield i


def test_get_all(client):
    response = client.get('/api/tasks')

    assert len(response.json) == 2


def test_get_by_existing_filter_number(client):
    number = '2.15'
    expected = get_expected(lambda x: x['number'] == number)
    data = {
        'filter_by_number': number
    }

    response = client.get('/api/tasks', query_string=data)

    assert len(response.json) == 1
    actual = response.json[0]

    assert actual['id'] == expected['id']


def test_get_by_existing_id(client):
    id = 1
    expected = get_expected(lambda x: x['id'] == id)

    response = client.get(f'/api/tasks/{id}')
    task = response.json

    assert task['id'] == expected['id']


def test_delete_by_existing_id(client):
    id = 1
    expected = get_expected(lambda x: x['id'] == id)

    response = client.delete(f'/api/tasks/{id}')
    task = response.json

    assert task['id'] == expected['id']