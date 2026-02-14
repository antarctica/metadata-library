from typing import Optional, Union

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
    return app.test_client()


@pytest.fixture
def fx_get_record_response(app_client: FlaskClient) -> ElementTree():
    """Get a generated record for a given standard/profile and config."""

    def _get_record_response_for_config(kind: str, standard_profile: str, config: str) -> etree:
        response = app_client.get(f"/{kind}/{standard_profile}/{config}")
        return fromstring(response.data)

    return _get_record_response_for_config


def _clean_val(value: Union[dict, list, str, float]) -> Optional[Union[dict, list, str, int, float]]:
    if isinstance(value, dict):
        cleaned_dict = {k: _clean_val(v) for k, v in value.items() if v not in (None, [], {})}
        return {k: v for k, v in cleaned_dict.items() if v not in (None, [], {})}
    if isinstance(value, list):
        cleaned_list = [_clean_val(v) for v in value if v not in (None, [], {})]
        return cleaned_list if cleaned_list else None
    return value


def clean_dict(d: dict) -> dict:
    """Remove any None or empty list/dict values from a dict."""
    cleaned = _clean_val(d)
    if not isinstance(cleaned, dict):
        msg = "Value must be a dict"
        raise TypeError(msg) from None
    return {k: v for k, v in cleaned.items() if v not in (None, [], {})}
