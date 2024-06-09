import os
import tempfile
import pytest
from sports import create_app
from sports.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), "test.sql"), "rb") as f:
    test_sql = f.read().decode("utf-8")
    
@pytest.fixture()
def app():
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app({"TESTING":True, "DATABASE": db_path,})
    
    with app.app_context():
        init_db()
        get_db().executescript(test_sql)
    
    yield app
    
    os.close(db_fd)
    os.unlink(db_path)
    
@pytest.fixture()
def client(app):
    return app.test_client()
