import pytest

from bas_metadata_library import MetadataRecordConfig, MetadataRecord, MetadataRecordElement

_config = {"foo": "bar"}


def test_config_class():
    configuration = MetadataRecordConfig(**_config)
    # assert configuration.schema() is None


def test_record_class():
    configuration = MetadataRecordConfig(**_config)
    record = MetadataRecord(configuration)
    element = record.make_element()
    assert element is None


def test_element_class():
    configuration = MetadataRecordConfig(**_config)
    record = MetadataRecord(configuration)
    element = MetadataRecordElement(record=record, attributes={})
    element.make_element()
