import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.monkeypatch import MonkeyPatch
from flask import Flask
from flask.testing import FlaskClient
from lxml import etree
from lxml.etree import ElementTree, fromstring

from tests.app import create_app


@pytest.fixture(autouse=True)
def _change_test_dir(request: FixtureRequest, monkeypatch: MonkeyPatch) -> None:
    """
    Change working directory to `tests/`.

    Not the most elegant solution, but so widely used in tests that refactoring it would be a major undertaking.
    """
    monkeypatch.chdir(request.fspath.dirname)


@pytest.fixture
def app() -> Flask:
    """Test app."""
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def app_runner(app: Flask):
    """Test app runner."""
    return app.test_cli_runner()


@pytest.fixture
def app_client(app: Flask) -> FlaskClient:
    """Test app client."""
    with app.test_client() as client:
        return client


@pytest.fixture
def get_record_response(client: FlaskClient) -> ElementTree():
    """Get a generated record for a given standard and config."""
    def _get_record_response_for_config(standard: str, config: str) -> etree:
        response = client.get(f"/standards/{standard}/{config}")
        return fromstring(response.data)  # noqa: S320

    return _get_record_response_for_config
