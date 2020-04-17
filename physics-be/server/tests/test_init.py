import os
import tempfile
import shutil

import pytest
from pathlib import Path

from .. import server


root = Path(os.path.dirname(os.path.realpath(__file__)))


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