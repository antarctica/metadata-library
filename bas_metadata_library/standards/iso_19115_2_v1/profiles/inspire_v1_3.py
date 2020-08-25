import json

from importlib_resources import path as resource_path

from bas_metadata_library import MetadataRecordConfig as _MetadataRecordConfig


# Base classes


class MetadataRecordConfig(_MetadataRecordConfig):
    """
    Overloaded base MetadataRecordConfig class

    Defines the JSON Schema used for this metadata standard
    """

    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)

        self.config = kwargs

        with resource_path(
            "bas_metadata_library.standards_schemas.iso_19115_2_v1.profiles.inspire_v1_3", "configuration-schema.json"
        ) as configuration_schema_file_path:
            with open(configuration_schema_file_path) as configuration_schema_file:
                configuration_schema_data = json.load(configuration_schema_file)
        self.schema = configuration_schema_data
