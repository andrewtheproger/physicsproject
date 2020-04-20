import os
import tempfile
import shutil

import pytest
from pathlib import Path

from .. import server


root = Path(os.path.dirname(os.path.realpath(__file__)))


def get_expected(predicate):
    expected = next((x for x in snapshot if predicate(x)), None)

    if not expected:
        raise Exception('Cant find item in test database snapshot')

    return expected


def check_not_exists(predicate):
    expected = next((x for x in snapshot if predicate(x)), None)

    if expected:
        raise Exception('Should not find an item in test database snapshot, but found it')


def init_db():
    original_test_db = root/'test.db'
    current_db = root/'test.copy.db'

    if not original_test_db.is_file():
        raise Exception('Cant find original test db')

    shutil.copy(original_test_db, current_db)

    server.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(current_db)
    server.app.config['TESTING'] = True

    with server.app.test_client() as client:
        yield client

    current_db.unlink()


# this is a test.db snapshot
snapshot = [
    {
        "body": {
            "image_hrefs": [
                "href1",
                "href2"
            ],
            "latex": "long latex"
        },
        "created_date": 1587122819969,
        "hints": [
            {
                "body": {
                    "image_hrefs": [
                        "href12",
                        "href13"
                    ],
                    "latex": "latex here"
                },
                "created_date": 1587122821889,
                "id": 1,
                "status": "pending",
                "task_id": 1,
                "updated_date": 1587122821889
            }
        ],
        "id": 1,
        "number": "2.15",
        "updated_date": 1587122819969
    },
    {
        "body": {
            "image_hrefs": [
                "href1",
                "href2"
            ],
            "latex": "long latex"
        },
        "created_date": 1587144488815,
        "hints": [
            {
                "body": {
                    "image_hrefs": [
                        "href12",
                        "href13"
                    ],
                    "latex": "latex here"
                },
                "created_date": 1587144507547,
                "id": 2,
                "status": "pending",
                "task_id": 2,
                "updated_date": 1587144507547
            },
            {
                "body": {
                    "image_hrefs": [
                        "href12",
                        "href13"
                    ],
                    "latex": "latex here"
                },
                "created_date": 1587144511858,
                "id": 3,
                "status": "approved",
                "task_id": 2,
                "updated_date": 1587144522055
            }
        ],
        "id": 2,
        "number": "4.4",
        "updated_date": 1587144488815
    }]