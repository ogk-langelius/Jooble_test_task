from .test.fixtures import app


def test_app_creates(app):
    assert app
