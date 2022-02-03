import pytest

from app import create_app


@pytest.fixture
def app():
    """app fixture"""
    return create_app('test')


@pytest.fixture
def client(app):
    """client fixture"""
    return app.test_client()


@pytest.fixture
def db(app):
    """db fixture"""
    from app import db

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield db
        db.close_all_sessions()
        db.drop_all()
        db.session.commit()
