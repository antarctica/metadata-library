import pytest
from app import create_app
from flask import Flask
from flask.testing import FlaskClient
from lxml.etree import ElementTree, fromstring


@pytest.fixture(autouse=True)
def _change_test_dir(request, monkeypatch) -> None:
    monkeypatch.chdir(request.fspath.dirname)


@pytest.fixture
def app() -> Flask:
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def app_runner(app: Flask):
    return app.test_cli_runner()


@pytest.fixture
def app_client(app: Flask) -> FlaskClient:
    with app.test_client() as client:
        return client


@pytest.fixture
def get_record_response(client: FlaskClient) -> ElementTree():
    def _get_record_response_for_config(standard: str, config: str):
        response = client.get(f"/standards/{standard}/{config}")
        return fromstring(response.data)

    return _get_record_response_for_config
