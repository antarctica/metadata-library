from http import HTTPStatus

import pytest
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner


@pytest.mark.usefixtures("app")
def test_app(app: Flask):
    assert app is not None
    assert isinstance(app, Flask)


@pytest.mark.usefixtures("app")
def test_app_environment(app: Flask):
    print(app.config)
    assert app.config["TESTING"] is True


@pytest.mark.usefixtures("app_runner")
def test_cli_help(app_runner: FlaskCliRunner):
    result = app_runner.invoke(args=["--help"])
    assert "Show this message and exit." in result.output


@pytest.mark.usefixtures("app_client")
def test_app_root(app_client: FlaskClient):
    expected_response = {"meta": "Root endpoint for Metadata Library internal API"}
    response = app_client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.mimetype == "application/json"
    assert response.json == expected_response
