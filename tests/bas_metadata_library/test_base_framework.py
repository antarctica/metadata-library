# noinspection PyUnresolvedReferences
import pytest

from bas_metadata_library import MetadataRecordConfig, MetadataRecord, MetadataRecordElement

_config = {"foo": "bar"}


def test_config_class():
    configuration = MetadataRecordConfig(**_config)
    assert configuration.schema is None


def test_record_class_configuration():
    configuration = MetadataRecordConfig(**_config)
    record = MetadataRecord(configuration=configuration)
    element = record.make_element()
    assert element is None


def test_record_class_record():
    with open(f"tests/resources/records/test-standard-v1/minimal-record.xml") as record_file:
        record_data = record_file.read()

    record = MetadataRecord(record=record_data)
    config = record.make_config()
    assert config.config == {}


def test_element_class_config():
    configuration = MetadataRecordConfig(**_config)
    record = MetadataRecord(configuration=configuration)
    element = MetadataRecordElement(record=record, attributes={})
    element.make_element()


def test_element_class_record():
    with open(f"tests/resources/records/test-standard-v1/minimal-record.xml") as record_file:
        record_data = record_file.read()
    record = MetadataRecord(record=record_data)
    element = MetadataRecordElement(record=record, attributes={})
    element.make_config()
