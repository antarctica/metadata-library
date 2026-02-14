import json
from copy import deepcopy
from datetime import datetime, timezone
from http import HTTPStatus
from pathlib import Path
from typing import Callable

import cattrs
import pytest
from flask.testing import FlaskClient
from jsonschema.exceptions import ValidationError
from lxml.etree import tostring, Element

from bas_metadata_library.standards.iso_19115_2 import (
    MetadataRecord,
    MetadataRecordConfigV4,
    Namespaces,
)
from bas_metadata_library.standards.magic_administration.v1 import Permission, AdministrationMetadata
from tests.conftest import clean_dict
from tests.resources.configs.magic_administration_profile import encoding_configs_v1_all

profile = "magic-administration"
namespaces = Namespaces()

class TestMagicAdministrationProfilePermission:
    """Test permission element."""

    @pytest.mark.parametrize(
        "values",
        [
            {"directory": "x", "group": "x"},
            {"directory": "x", "group": "x", "expiry": datetime(2014, 6, 30, 14, 30, second=45, tzinfo=timezone.utc)},
            {"directory": "x", "group": "x", "comment": "x"},
            {"directory": "x", "group": "x", "expiry": datetime(2014, 6, 30, 14, 30, second=45, tzinfo=timezone.utc), 'comment': "x"},
        ],
    )
    def test_init(self, values: dict):
        """Can create a Permission element from directly assigned properties."""
        permission = Permission(**values)

        assert permission.directory == values["directory"]
        assert permission.group == values["group"]
        assert permission.expiry == values["expiry"] if "expiry" in values else datetime.max.replace(tzinfo=timezone.utc)
        if "comment" in values:
            assert permission.comment == values["comment"]
        else:
            assert permission.comment is None

    @pytest.mark.parametrize(
        ("a", "b", "expected"),
        [
            (Permission(directory="x", group="x"), Permission(directory="x", group="x"), True),
            (Permission(directory="x", group="x"), Permission(directory="x", group="y"), False),
            (Permission(directory="x", group="x"), Permission(directory="y", group="x"), False),
            (Permission(directory="x", group="x", comment="x"), Permission(directory="x", group="x"), True),
            (
                Permission(directory="x", group="x", comment="x"),
                Permission(directory="x", group="x", comment="y"),
                True,
            ),
        ],
    )
    def test_eq(self, a: Permission, b: Permission, expected: bool):
        """Can compare two Permission elements."""
        result = a == b
        assert result == expected

    @pytest.mark.cov()
    def test_eq_invalid(self):
        """Cannot compare non-Permission elements."""
        with pytest.raises(TypeError):
            _ = Permission(directory="x", group="x") == "x"

class TestMagicAdministrationProfileContent:
    """Test administration element."""

    _schema = (
        "https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/magic-administration-content-v1.json"
    )

    @pytest.mark.parametrize(
        "values",
        [
            {"id": "x"},
            {"id": "x", "gitlab_issues": ["https://gitlab.com/group/project/-/issues/1"]},
            {"id": "x", "metadata_permissions": [Permission(directory="x", group="x")]},
            {"id": "x", "resource_permissions": [Permission(directory="x", group="x")]},
            {
                "id": "x",
                "gitlab_issues": ["https://gitlab.com/group/project/-/issues/1"],
                "metadata_permissions": [Permission(directory="x", group="x")],
                "resource_permissions": [Permission(directory="x", group="x")],
            },
        ],
    )
    def test_init(self, values: dict):
        """Can create an AdministrationMetadata element from directly assigned properties."""
        administration = AdministrationMetadata(**values)

        assert administration.id == values["id"]
        if "gitlab_issues" in values:
            assert administration.gitlab_issues == values["gitlab_issues"]
        else:
            assert administration.gitlab_issues == []
        if "metadata_permissions" in values:
            assert administration.metadata_permissions == values["metadata_permissions"]
        else:
            assert administration.metadata_permissions == []
        if "resource_permissions" in values:
            assert administration.resource_permissions == values["resource_permissions"]
        else:
            assert administration.resource_permissions == []

    def test_no_id(self):
        """Cannot create an AdministrationMetadata element without an ID."""
        with pytest.raises(TypeError):
            # noinspection PyTypeChecker
            AdministrationMetadata(id=None)

    def test_invalid_gitlab_issues(self):
        """Cannot create an AdministrationMetadata element with invalid GitLab issue URLs."""
        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            AdministrationMetadata(id='x', gitlab_issues=['x'])

    def test_structure_cattrs(self):
        """Can use Cattrs to create an AdministrationMetadata instance from plain types."""
        expected_date = datetime(2014, 6, 30, 14, 30, second=45, tzinfo=timezone.utc)

        value = {
            "$schema": self._schema,
            "id": "x",
            "gitlab_issues": ["https://gitlab.com/group/project/-/issues/1"],
            "resource_permissions": [{"directory": "x", "group": "x", "expiry": expected_date.isoformat()}],
        }
        expected = AdministrationMetadata(
            id="x",
            gitlab_issues=["https://gitlab.com/group/project/-/issues/1"],
            resource_permissions=[Permission(directory="x", group="x", expiry=expected_date)],
        )

        converter = cattrs.Converter()
        converter.register_structure_hook(AdministrationMetadata, lambda d, t: AdministrationMetadata.structure(d))
        result = converter.structure(value, AdministrationMetadata)

        assert result == expected

    @pytest.mark.cov()
    def test_structure_invalid_schema(self):
        """Cannot create an AdministrationMetadata instance from plain types with the wrong schema."""
        converter = cattrs.Converter()
        converter.register_structure_hook(AdministrationMetadata, lambda d, t: AdministrationMetadata.structure(d))

        with pytest.raises(ValueError, match=r"Unsupported JSON Schema in data."):
            converter.structure({"$schema": "x"}, AdministrationMetadata)

    def test_unstructure_cattrs(self):
        """Can use Cattrs to convert a AdministrationMetadata instance into plain types."""
        expected_date = datetime(2014, 6, 30, 14, 30, second=45, tzinfo=timezone.utc)
        value = AdministrationMetadata(
            id="x",
            gitlab_issues=["https://gitlab.com/group/project/-/issues/1"],
            resource_permissions=[Permission(directory="x", group="x", expiry=expected_date)],
        )
        expected = {
            "id": "x",
            "gitlab_issues": ["https://gitlab.com/group/project/-/issues/1"],
            "resource_permissions": [{"directory": "x", "group": "x", "expiry": expected_date.isoformat()}],
        }

        converter = cattrs.Converter()
        converter.register_unstructure_hook(AdministrationMetadata, lambda d: d.unstructure())
        result = clean_dict(converter.unstructure(value))

        assert result == expected

    def test_json_dumps_loads(self):
        """Can convert an AdministrationMetadata instance to/from a JSON encoded string."""
        expected_date = datetime(2014, 6, 30, 14, 30, second=45, tzinfo=timezone.utc)
        value = AdministrationMetadata(
            id="x",
            gitlab_issues=["https://gitlab.com/group/project/-/issues/1"],
            metadata_permissions=[Permission(directory="x", group="x", expiry=expected_date, comment="x")],
            resource_permissions=[Permission(directory="x", group="x", expiry=expected_date)],
        )

        result = value.dumps_json()
        assert isinstance(result, str)
        parsed = json.loads(result)
        assert parsed["$schema"] == self._schema

        loop = AdministrationMetadata.loads_json(result)
        assert loop == value

class TestMagicAdministrationProfileEncoding:
    @pytest.mark.parametrize("config_name", list(encoding_configs_v1_all.keys()))
    def test_config_schema_validation_valid(self, config_name: str):
        """Can validate minimal record encoding configs against schema."""
        config = MetadataRecordConfigV4(**encoding_configs_v1_all[config_name])
        config.validate()
        assert True is True

    def test_config_schema_validation_invalid_profile(self):
        """Cannot validate record encoding configs that don't match schema."""
        config = deepcopy(MetadataRecordConfigV4(**encoding_configs_v1_all["minimal_v1"]))
        del config.config["file_identifier"]
        with pytest.raises(ValidationError) as e:
            config.validate()
        assert "'file_identifier' is a required property" in str(e.value)

    @pytest.mark.parametrize("config_name", list(encoding_configs_v1_all.keys()))
    def test_response(self, app_client: FlaskClient, config_name: str):
        """Can encode records for schema configs."""
        response = app_client.get(f"/profiles/{profile}/{config_name}")
        assert response.status_code == HTTPStatus.OK
        assert response.mimetype == "text/xml"

    @pytest.mark.parametrize("config_name", list(encoding_configs_v1_all.keys()))
    def test_complete_record(self, app_client: FlaskClient, config_name: str):
        """Check encoded records match known good examples."""
        with Path().resolve().parent.joinpath(f"resources/records/{profile}/{config_name}-record.xml").open() as expected_contents_file:
            expected_contents = expected_contents_file.read()

        response = app_client.get(f"/profiles/{profile}/{config_name}")
        assert response.data.decode() == expected_contents

    @pytest.mark.parametrize("config_name", list(encoding_configs_v1_all.keys()))
    def test_parse_existing_record(self, config_name: str):
        """Can decode a record to a record config."""
        with Path().resolve().parent.joinpath(f"resources/records/{profile}/{config_name}-record.xml").open() as record_file:
            record_data = record_file.read()

        record = MetadataRecord(record=record_data)
        configuration = record.make_config()
        config = configuration.config
        assert config == encoding_configs_v1_all[config_name]

    @pytest.mark.parametrize("config_name", list(encoding_configs_v1_all.keys()))
    def test_lossless_conversion(self, fx_get_record_response: Callable[..., Element], config_name: str):
        """Can encode then decode a record config without loss of information."""
        _record = tostring(
            fx_get_record_response(kind="profiles", standard_profile=profile, config=config_name),
            pretty_print=True,
            xml_declaration=True,
            encoding="utf-8",
        ).decode()
        _config = encoding_configs_v1_all[config_name]

        record = MetadataRecord(record=_record)
        config_ = record.make_config().config

        config = MetadataRecordConfigV4(**config_)
        record_ = MetadataRecord(configuration=config).generate_xml_document().decode()
        assert _record == record_
        assert _config == config_
