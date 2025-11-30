import pytest
from flask.testing import FlaskCliRunner


@pytest.mark.usefixtures("app_runner")
def test_validate_schemas(app_runner: FlaskCliRunner):
    result = app_runner.invoke(args=["validate-schemas"])
    assert result.exit_code == 0
