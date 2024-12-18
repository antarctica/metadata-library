# noinspection PyUnresolvedReferences
from pathlib import Path

from bas_metadata_library import MetadataRecord, MetadataRecordConfig, MetadataRecordElement

_config = {"foo": "bar"}


def test_config_class():
    configuration = MetadataRecordConfig(**_config)
    assert configuration.schema == {}


def test_record_class_configuration():
    configuration = MetadataRecordConfig(**_config)
    record = MetadataRecord(configuration=configuration)
    element = record.make_element()
    assert element is None


def test_record_class_record():
    with open(
        Path().resolve().parent.joinpath(f"resources/records/test-standard/minimal-record.xml"), mode="r"
    ) as record_file:
        record_data = record_file.read()

    record = MetadataRecord(record=record_data)
    config = record.make_config()
    assert config.config == {"$schema": ""}


def test_element_class_config():
    configuration = MetadataRecordConfig(**_config)
    record = MetadataRecord(configuration=configuration)
    element = MetadataRecordElement(record=record, attributes={})
    element.make_element()


def test_element_class_record():
    with open(
        Path().resolve().parent.joinpath(f"resources/records/test-standard/minimal-record.xml"), mode="r"
    ) as record_file:
        record_data = record_file.read()
    record = MetadataRecord(record=record_data)
    element = MetadataRecordElement(record=record, attributes={})
    element.make_config()
