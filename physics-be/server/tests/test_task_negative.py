from .test_init import init_db, check_not_exists
import pytest


@pytest.fixture
def client():
    for i in init_db():
        yield i

wrong_task_numbers = [
    '7.8',
    'random string'
]

wrong_task_ids = [
    5,
    'random string'
]

wrong_counts = [
    0,
    -17
]


@pytest.mark.parametrize('number', wrong_task_numbers)
def test_get_by_invalid_filter_number(client, number):
    check_not_exists(lambda x: x['number'] == number)

    data = {
        'filter_by_number': number
    }

    response = client.get('/api/tasks', query_string=data)

    assert len(response.json) == 0


@pytest.mark.parametrize('id', wrong_task_ids)
def test_get_by_invalid_id(client, id):
    check_not_exists(lambda x: x['id'] == id)

    response = client.get(f'/api/tasks/{id}')

    assert response.status_code == 404


@pytest.mark.parametrize('id', wrong_task_ids)
def test_delete_by_invalid_id(client, id):
    check_not_exists(lambda x: x['id'] == id)

    response = client.delete(f'/api/tasks/{id}')

    assert response.status_code == 404


def test_get_invalid_page(client):
    data = {
        'page': -17
    }

    response = client.get('/api/tasks', query_string=data)

    assert response.status_code == 400


@pytest.mark.parametrize('count', wrong_counts)
def test_get_invalid_count(client, count):
    data = {
        'count': count
    }

    response = client.get('/api/tasks', query_string=data)

    assert response.status_code == 400


def test_get_invalid_order(client):
    data = {
        'order': 'invalid'
    }

    response = client.get('/api/tasks', query_string=data)

    assert response.status_code == 400


def test_get_invalid_order_direction(client):
    data = {
        'order_direction': 'invalid'
    }

    response = client.get('/api/tasks', query_string=data)

    assert response.status_code == 400