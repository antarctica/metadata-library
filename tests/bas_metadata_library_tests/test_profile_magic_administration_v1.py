import json
import pickle
from copy import deepcopy
from datetime import datetime, timezone
from http import HTTPStatus
from pathlib import Path
from typing import Callable, Optional

import cattrs
import pytest
from flask.testing import FlaskClient
from jsonschema.exceptions import ValidationError
from lxml.etree import tostring, Element, fromstring
from cryptography.hazmat.primitives.keywrap import InvalidUnwrap
from jwskate import InvalidClaim, InvalidSignature, Jwk, JwtSigner

from bas_metadata_library.standards.iso_19115_2 import (
    MetadataRecord,
    MetadataRecordConfigV4,
    Namespaces,
)
from bas_metadata_library.standards.magic_administration.v1 import Permission, AdministrationMetadata
from bas_metadata_library.standards.magic_administration.v1.utils import get_kv, set_kv, AdministrationKeys, \
    AdministrationWrapper, \
    AdministrationMetadataIntegrityError, get_admin, AdministrationMetadataSubjectMismatchError, set_admin
from tests.conftest import clean_dict
from tests.resources.configs.magic_administration_profile import encoding_configs_v1_all
from tests.resources.configs.iso19115_0_standard import configs_v4_all as iso_configs_all

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

    @staticmethod
    def _normalise_record(record: str) -> str:
        xpath = ("/gmi:MI_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:supplementalInformation"
                 "/gco:CharacterString/text()")
        record = fromstring(record.encode())
        sup_element = record.xpath(xpath[:-len("/text()")], namespaces=namespaces.nsmap())[0]
        sup_element.text = "..."
        record_normalised = tostring(record, xml_declaration=True, encoding="utf-8").decode()
        return record_normalised

    @pytest.mark.parametrize("config_name", list(encoding_configs_v1_all.keys()))
    def test_complete_record(self, app_client: FlaskClient, fx_admin_meta_keys: AdministrationKeys, config_name: str):
        """
        Check encoded records match known good examples.

        Normalises admin metadata in records as each are unique.
        """
        with Path().resolve().parent.joinpath(f"resources/records/{profile}/{config_name}-record.xml").open() as expected_contents_file:
            reference_raw = expected_contents_file.read()
        candidate_raw = app_client.get(f"/profiles/{profile}/{config_name}")
        reference_normalised = self._normalise_record(reference_raw)
        candidate_normalised = self._normalise_record(candidate_raw.data.decode())

        assert reference_normalised == candidate_normalised

    @pytest.mark.parametrize("config_name", list(encoding_configs_v1_all.keys()))
    def test_parse_existing_record(self, config_name: str):
        """Can decode a record to a record config."""
        reference_config = encoding_configs_v1_all[config_name]
        with Path().resolve().parent.joinpath(f"resources/records/{profile}/{config_name}-record.xml").open() as record_file:
            record_data = record_file.read()
        record = MetadataRecord(record=record_data)
        configuration = record.make_config()
        candidate_config = configuration.config

        # normalise admin metadata in config as each are unique
        candidate_config['identification']['supplemental_information'] = "..."
        reference_config['identification']['supplemental_information'] = "..."

        assert candidate_config == reference_config

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

class TestMagicAdministrationProfileKeys:
    signing_key_private = Jwk.generate(alg="ES256", kid="signing_key")
    signing_key_public = signing_key_private.public_jwk()
    encryption_key_private = Jwk.generate(alg="ECDH-ES+A128KW", crv="P-256", kid="encryption_key")

    @pytest.mark.parametrize(
        ("signing_private", "signing_public"),
        [(signing_key_private, None), (None, signing_key_public), (signing_key_private, signing_key_public)],
    )
    def test_init(self, signing_private: Optional[Jwk], signing_public: Optional[Jwk]):
        """Can create administrative key's container."""
        result = AdministrationKeys(
            signing_public=signing_public,
            signing_private=signing_private,
            encryption_private=self.encryption_key_private,
        )
        assert result.encryption_private == self.encryption_key_private
        assert result.signing_private == signing_private
        assert result.signing_public == signing_public if signing_public else self.signing_key_public

    def test_init_no_signing(self):
        """Cannot create administrative key's container without a signing key."""
        with pytest.raises(TypeError, match=r"Public or private signing_key must be provided."):
            AdministrationKeys(
                signing_public=None,
                signing_private=None,
                encryption_private=self.encryption_key_private,
            )

    @pytest.mark.parametrize("signing_private", [signing_key_private, None])
    def test_pickle(self, signing_private: Optional[Jwk]):
        """Can pickle/unpickle keys to JSON."""
        public = self.signing_key_public if signing_private is None else None
        keys = AdministrationKeys(
            signing_private=signing_private,
            signing_public=public,
            encryption_private=self.encryption_key_private,
        )

        pickled = pickle.dumps(keys, pickle.HIGHEST_PROTOCOL)
        result: AdministrationKeys = pickle.loads(pickled)  # noqa: S301
        assert result.encryption_private == keys.encryption_private
        assert result.signing_private == keys.signing_private
        assert result.signing_public == keys.signing_public

    @pytest.mark.cov()
    def test_not_eq(self, fx_admin_meta_keys: AdministrationKeys):
        """Cannot compare if non-keys instances are equal."""
        assert fx_admin_meta_keys != 1

class TestMagicAdministrationProfileSeal:
    def test_init(self, fx_admin_meta_keys: AdministrationKeys):
        """Can create administrative metadata wrapper."""
        seal = AdministrationWrapper(fx_admin_meta_keys)
        assert seal._keys == fx_admin_meta_keys

    def test_encode(self, fx_admin_wrapper: AdministrationWrapper, fx_admin_meta_element: AdministrationMetadata):
        """Can sign and encrypt administrative metadata."""
        result = fx_admin_wrapper.encode(fx_admin_meta_element)
        assert isinstance(result, str)

    @pytest.mark.cov()
    def test_encode_no_keys(
        self, fx_admin_wrapper: AdministrationWrapper, fx_admin_meta_element: AdministrationMetadata
    ):
        """Cannot sign administrative metadata without private signing key."""
        wrapper = AdministrationWrapper(
            keys=AdministrationKeys(
                encryption_private=fx_admin_wrapper._keys.encryption_private,
                signing_public=fx_admin_wrapper._keys.signing_public,
            )
        )
        with pytest.raises(ValueError, match=r"Private signing key is required for writing metadata."):
            wrapper.encode(fx_admin_meta_element)

    def test_decode(self, fx_admin_wrapper: AdministrationWrapper, fx_admin_meta_element: AdministrationMetadata):
        """Can sign and encrypt administrative metadata."""
        value = fx_admin_wrapper.encode(fx_admin_meta_element)

        result = fx_admin_wrapper.decode(value)
        assert isinstance(result, AdministrationMetadata)

    def test_decode_bad_encryption(
        self, fx_admin_wrapper: AdministrationWrapper, fx_admin_meta_element: AdministrationMetadata
    ):
        """Cannot decrypt administrative metadata with the wrong encryption key."""
        alt_encryption_key = Jwk.generate(alg="ECDH-ES+A128KW", crv="P-256", kid="alt_encryption_key")
        alt_keys = AdministrationKeys(
            signing_public=fx_admin_wrapper._keys.signing_public,
            signing_private=fx_admin_wrapper._keys.signing_private,
            encryption_private=alt_encryption_key,
        )
        alt_wrapper = AdministrationWrapper(alt_keys)
        value = alt_wrapper.encode(fx_admin_meta_element)

        with pytest.raises(InvalidUnwrap):
            fx_admin_wrapper.decode(value)

    def test_decode_bad_validate_key(
        self, fx_admin_wrapper: AdministrationWrapper, fx_admin_meta_element: AdministrationMetadata
    ):
        """Cannot validate administrative metadata with the wrong public signing key."""
        value = fx_admin_wrapper.encode(fx_admin_meta_element)

        alt_verify_key = Jwk.generate(alg="ES256", kid="alt_signing_key").public_jwk()
        alt_keys = AdministrationKeys(
            signing_public=alt_verify_key,
            signing_private=None,
            encryption_private=fx_admin_wrapper._keys.encryption_private,
        )
        alt_wrapper = AdministrationWrapper(alt_keys)

        with pytest.raises(InvalidSignature):
            alt_wrapper.decode(value)

    def test_decode_bad_issuer(
        self, fx_admin_wrapper: AdministrationWrapper, fx_admin_meta_element: AdministrationMetadata
    ):
        """Cannot validate administrative metadata with the wrong issuer."""
        alt_signer = JwtSigner(issuer="x", key=fx_admin_wrapper._keys.signing_private)
        value = str(
            alt_signer.sign(
                subject=fx_admin_meta_element.id,
                audience=fx_admin_wrapper._audience,
                extra_claims={"pyd": fx_admin_meta_element.dumps_json()},
            ).encrypt(key=fx_admin_wrapper._keys.encryption_private.public_jwk(), enc=fx_admin_wrapper._enc_alg)
        )

        with pytest.raises(InvalidClaim) as e:
            fx_admin_wrapper.decode(value)
        assert e.value.args[1] == "iss"

    def test_decode_bad_audience(
        self, fx_admin_wrapper: AdministrationWrapper, fx_admin_meta_element: AdministrationMetadata
    ):
        """Cannot validate administrative metadata with the wrong audience."""
        alt_signer = JwtSigner(issuer=fx_admin_wrapper._issuer, key=fx_admin_wrapper._keys.signing_private)
        value = str(
            alt_signer.sign(
                subject=fx_admin_meta_element.id,
                audience="x",
                extra_claims={"pyd": fx_admin_meta_element.dumps_json()},
            ).encrypt(key=fx_admin_wrapper._keys.encryption_private.public_jwk(), enc=fx_admin_wrapper._enc_alg)
        )

        with pytest.raises(InvalidClaim) as e:
            fx_admin_wrapper.decode(value)
        assert e.value.args[1] == "aud"

    def test_decode_bad_subject(
        self, fx_admin_wrapper: AdministrationWrapper, fx_admin_meta_element: AdministrationMetadata
    ):
        """Cannot validate administrative metadata with the wrong audience."""
        signer = JwtSigner(issuer=fx_admin_wrapper._issuer, key=fx_admin_wrapper._keys.signing_private)
        value = str(
            signer.sign(
                subject="invalid",
                audience=fx_admin_wrapper._audience,
                extra_claims={"pyd": fx_admin_meta_element.dumps_json()},
            ).encrypt(key=fx_admin_wrapper._keys.encryption_private.public_jwk(), enc=fx_admin_wrapper._enc_alg)
        )

        with pytest.raises(AdministrationMetadataIntegrityError):
            fx_admin_wrapper.decode(value)

class TestMagicAdministrationProfileGetSet:
    @pytest.mark.parametrize("value", [False, True])
    def test_get(
        self,
        fx_admin_meta_keys: AdministrationKeys,
        fx_admin_meta_element: AdministrationMetadata,
        fx_admin_wrapper: AdministrationWrapper,
        value: bool,
    ):
        """Can get admin metadata from a record if present."""
        config = deepcopy(MetadataRecordConfigV4(**iso_configs_all["minimal_v4"])).config
        expected = None
        if value:
            config['file_identifier'] = "x"
            fx_admin_meta_element.id = config['file_identifier']
            config['identification']['supplemental_information'] = json.dumps(
                {"admin_metadata": fx_admin_wrapper.encode(fx_admin_meta_element)}
            )
            expected = fx_admin_meta_element

        result = get_admin(keys=fx_admin_meta_keys, config=config)
        assert result == expected

    @pytest.mark.cov()
    def test_get_other(
        self,
        fx_admin_meta_keys: AdministrationKeys,
        fx_admin_meta_element: AdministrationMetadata,
        fx_admin_wrapper: AdministrationWrapper    ):
        """Can get admin metadata from a record alongside other supplemental content."""
        config = deepcopy(MetadataRecordConfigV4(**iso_configs_all["minimal_v4"])).config
        config['file_identifier'] = "x"
        fx_admin_meta_element.id = config['file_identifier']
        config['identification']['supplemental_information'] = json.dumps(
            {"admin_metadata": fx_admin_wrapper.encode(fx_admin_meta_element), 'x': 'x'}
        )
        expected = fx_admin_meta_element

        result = get_admin(keys=fx_admin_meta_keys, config=config)
        assert result == expected

    @pytest.mark.cov()
    def test_get_non_json(self, fx_admin_meta_keys: AdministrationKeys):
        """Cannot get admin metadata but does not fail where non-JSON supplemental content is used."""
        config = deepcopy(MetadataRecordConfigV4(**iso_configs_all["minimal_v4"])).config
        config['identification']['supplemental_information'] = 'x'

        result = get_admin(keys=fx_admin_meta_keys, config=config)
        assert result is None

    @pytest.mark.cov()
    def test_get_non_admin(self, fx_admin_meta_keys: AdministrationKeys):
        """Cannot get admin metadata but does not fail where admin key is missing."""
        config = deepcopy(MetadataRecordConfigV4(**iso_configs_all["minimal_v4"])).config
        config['identification']['supplemental_information'] = json.dumps({"x": "x"})

        result = get_admin(keys=fx_admin_meta_keys, config=config)
        assert result is None

    def test_get_mismatched_subject(
        self,
        fx_admin_meta_keys: AdministrationKeys,
        fx_admin_meta_element: AdministrationMetadata,
        fx_admin_wrapper: AdministrationWrapper,
    ):
        """Cannot get admin metadata that doesn't relate to the record that contains it."""
        config = deepcopy(MetadataRecordConfigV4(**iso_configs_all["minimal_v4"])).config
        config['file_identifier'] = "x"
        fx_admin_meta_element.id = "y"
        config['identification']['supplemental_information'] = json.dumps(
            {"admin_metadata": fx_admin_wrapper.encode(fx_admin_meta_element)}
        )

        with pytest.raises(AdministrationMetadataSubjectMismatchError):
            get_admin(keys=fx_admin_meta_keys, config=config)

    def test_set(
        self,
        fx_admin_meta_keys: AdministrationKeys,
        fx_admin_meta_element: AdministrationMetadata,
        fx_admin_wrapper: AdministrationWrapper,
    ):
        """Can set admin metadata in a record."""
        config = deepcopy(MetadataRecordConfigV4(**iso_configs_all["minimal_v4"])).config
        config['file_identifier'] = "x"
        fx_admin_meta_element.id = config['file_identifier']

        set_admin(keys=fx_admin_meta_keys, config=config, admin_meta=fx_admin_meta_element)
        result = json.loads(config['identification']['supplemental_information'])
        # Can't directly compare tokens as they contain unique headers so check decoded contents.
        assert fx_admin_wrapper.decode(result["admin_metadata"]) == fx_admin_meta_element

    def test_set_mismatched_subject(
        self,
        fx_admin_meta_keys: AdministrationKeys,
        fx_admin_meta_element: AdministrationMetadata,
        fx_admin_wrapper: AdministrationWrapper,
    ):
        """Cannot set administrative metadata that doesn't relate to the record that contains it."""
        config = deepcopy(MetadataRecordConfigV4(**iso_configs_all["minimal_v4"])).config
        config['file_identifier'] = "x"
        fx_admin_meta_element.id = "y"

        with pytest.raises(AdministrationMetadataSubjectMismatchError):
            set_admin(keys=fx_admin_meta_keys, config=config, admin_meta=fx_admin_meta_element)

    @pytest.mark.cov()
    def test_set_non_json(
        self,
        fx_admin_meta_keys: AdministrationKeys,
        fx_admin_meta_element: AdministrationMetadata,
        fx_admin_wrapper: AdministrationWrapper,
    ):
        """Can set admin metadata where an existing non-JSON supplemental content is used."""
        expected = 'x'
        config = deepcopy(MetadataRecordConfigV4(**iso_configs_all["minimal_v4"])).config
        config['file_identifier'] = "x"
        fx_admin_meta_element.id = config['file_identifier']
        config['identification']['supplemental_information'] = expected

        set_admin(keys=fx_admin_meta_keys, config=config, admin_meta=fx_admin_meta_element)
        result = json.loads(config['identification']['supplemental_information'])
        assert 'admin_metadata' in result
        assert result['statement'] == expected


class TestMagicAdministrationProfileKv:
    @pytest.mark.parametrize(("value", "expected"), [(None, {}), ("", {}), (json.dumps({"x": "x"}), {"x": "x"})])
    def test_get_kv(self, value: Optional[str], expected: dict):
        """Can parse key-values from JSON string."""
        config = deepcopy(MetadataRecordConfigV4(**iso_configs_all["minimal_v4"])).config
        config['identification']['supplemental_information'] = value
        result = get_kv(config)
        assert result == expected

    def test_get_kv_non_json(self):
        """Cannot parse key-values from non-JSON string."""
        config = deepcopy(MetadataRecordConfigV4(**iso_configs_all["minimal_v4"])).config
        config['identification']['supplemental_information'] = 'x'
        with pytest.raises(ValueError, match=r"Supplemental information isn't JSON parsable."):
            get_kv(config)

    def test_get_kv_non_dict(self):
        """Cannot parse key-values from non-dict JSON string."""
        config = deepcopy(MetadataRecordConfigV4(**iso_configs_all["minimal_v4"])).config
        config['identification']['supplemental_information'] = json.dumps(["x"])
        with pytest.raises(TypeError, match=r"Supplemental information isn't parsed as a dict."):
            get_kv(config)

    @pytest.mark.parametrize(
        ("value", "existing_value", "replace", "expected_raw"),
        [
            ({}, None, False, None),
            ({}, json.dumps({}), False, None),
            ({"x": "x"}, json.dumps({"y": "y"}), False, json.dumps({"y": "y", "x": "x"})),
            ({"y": "x"}, json.dumps({"y": "y"}), False, json.dumps({"y": "x"})),
            ({"x": "x"}, json.dumps({"y": "y"}), True, json.dumps({"x": "x"})),
        ],
    )
    def test_set_kv(self, value: dict, existing_value: Optional[None], replace: bool, expected_raw: str):
        """Can encode key-values to a JSON string."""
        config = deepcopy(MetadataRecordConfigV4(**iso_configs_all["minimal_v4"])).config
        if existing_value:
            config['identification']['supplemental_information'] = existing_value
        set_kv(value, config, replace=replace)
        if expected_raw is not None:
            result = config['identification']['supplemental_information']
            assert result == expected_raw
        else:
            assert 'supplemental_information' not in config['identification']
