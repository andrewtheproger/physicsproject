import os
import tempfile
import shutil

import pytest
from pathlib import Path

from .. import server


root = Path(os.path.dirname(os.path.realpath(__file__)))


def exec_crossplatform(command):
    if os.name == 'nt':
        os.system(f'cmd /c {command}')
    elif os.name == 'posix':
        os.system(cmd)
    else:
        raise Exception('Cant determinate os')


def find_git_root():
    current_dir = root
    while current_dir.parent != current_dir:
        for item in current_dir.iterdir():
            if item.name == '.git':
                return current_dir

        current_dir = current_dir.parent

    raise Exception(f'Cant find a git repository parent from {root}')


@pytest.fixture
def client():
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
    

def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/api/tasks')
    print(rv.json)

    assert len(rv.json) == 1