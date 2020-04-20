from .test_init import init_db, snapshot, get_expected
import pytest


@pytest.fixture
def client():
    for i in init_db():
        yield i


valid_propertiers = [
    'number'
]


def test_get_all(client):
    response = client.get('/api/tasks')

    assert len(response.json) == 2


def test_get_by_valid_filter_number(client):
    number = '2.15'
    expected = get_expected(lambda x: x['number'] == number)
    data = {
        'filter_by_number': number
    }

    response = client.get('/api/tasks', query_string=data)

    assert len(response.json) == 1
    actual = response.json[0]

    assert actual['id'] == expected['id']


def test_get_by_valid_id(client):
    id = 1
    expected = get_expected(lambda x: x['id'] == id)

    response = client.get(f'/api/tasks/{id}')
    task = response.json

    assert task['id'] == expected['id']


def test_delete_by_valid_id(client):
    id = 1
    expected = get_expected(lambda x: x['id'] == id)

    response = client.delete(f'/api/tasks/{id}')
    task = response.json

    assert task['id'] == expected['id']


def test_get_valid_page(client):
    data = {
        'page': 0
    }

    response = client.get('/api/tasks', query_string=data)

    assert response.status_code == 200


def test_get_valid_count(client):
    data = {
        'count': 1
    }

    response = client.get('/api/tasks', query_string=data)

    assert response.status_code == 200


@pytest.mark.parametrize('property', valid_propertiers)
def test_get_valid_order(client, property):
    data = {
        'order': property
    }

    response = client.get('/api/tasks', query_string=data)

    assert response.status_code == 200


@pytest.mark.parametrize('direction', ['asc', 'desc'])
def test_get_valid_order_direction(client, direction):
    data = {
        'order_direction': direction
    }

    response = client.get('/api/tasks', query_string=data)

    assert response.status_code == 200