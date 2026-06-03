import pytest
from app import create_app, db as _db

TEST_CONFIG = {
    "TESTING": True,
    "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    "SECRET_KEY": "test-secret",
    "GREEN_API_INSTANCE_ID": "",
    "GREEN_API_TOKEN": "",
    "GOOGLE_AI_API_KEY": "",
}


@pytest.fixture(scope="session")
def app():
    test_app = create_app(test_config=TEST_CONFIG)
    with test_app.app_context():
        yield test_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_db(app):
    with app.app_context():
        yield
        _db.session.rollback()
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()
