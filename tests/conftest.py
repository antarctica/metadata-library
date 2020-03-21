import pytest

from flask.testing import FlaskClient

# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# This is a testing environment, testing against endpoints that don't themselves allow user input, so the XML returned
# should be safe. In any case the test environment is not exposed and so does not present a risk.
from lxml.etree import ElementTree, fromstring

from app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
@pytest.mark.usefixtures("app")
def app_runner(app):
    return app.test_cli_runner()


@pytest.fixture
@pytest.mark.usefixtures("app")
def app_client(app) -> FlaskClient:
    with app.test_client() as client:
        return client


@pytest.fixture
@pytest.mark.usefixtures("app_client")
def get_record_response(client) -> ElementTree():
    def _get_record_response_for_config(standard: str, config: str):
        response = client.get(f"/standards/{standard}/{config}")
        xml_document = fromstring(response.data)
        return xml_document

    return _get_record_response_for_config
