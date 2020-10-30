from bas_metadata_library.standards.iso_19115_common import MetadataRecordElement
from bas_metadata_library.standards.iso_19115_common.base_elements import (
    FileIdentifier,
    HierarchyLevel,
    Contact,
    DateStamp,
    MetadataStandard,
    ReferenceSystemInfo,
    MetadataMaintenance,
)
from bas_metadata_library.standards.iso_19115_common.common_elements import Language, CharacterSet
from bas_metadata_library.standards.iso_19115_common.data_distribution_elements import DataDistribution
from bas_metadata_library.standards.iso_19115_common.data_identification_elements import DataIdentification
from bas_metadata_library.standards.iso_19115_common.data_quality_elements import DataQuality
from bas_metadata_library.standards.iso_19115_common.utils import contacts_have_role, contacts_condense_roles


class ISOMetadataRecord(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        file_identifier = FileIdentifier(record=self.record, attributes=self.attributes, xpath=f"{self.xpath}")
        _file_identifier = file_identifier.make_config()
        if _file_identifier != "":
            # noinspection PyTypeChecker
            _["file_identifier"] = _file_identifier

        language = Language(record=self.record, attributes=self.attributes, xpath=f"{self.xpath}/gmd:language")
        _language = language.make_config()
        if _language != "":
            # noinspection PyTypeChecker
            _["language"] = _language

        character_set = CharacterSet(
            record=self.record, attributes=self.attributes, xpath=f"{self.xpath}/gmd:characterSet"
        )
        _character_set = character_set.make_config()
        if _character_set != "":
            # noinspection PyTypeChecker
            _["character_set"] = _character_set

        hierarchy_level = HierarchyLevel(
            record=self.record, attributes=self.attributes, xpath=f"/{self.xpath}/gmd:hierarchyLevel"
        )
        _hierarchy_level = hierarchy_level.make_config()
        if _hierarchy_level != "":
            # noinspection PyTypeChecker
            _["hierarchy_level"] = _hierarchy_level

        _contacts = []
        contacts_length = int(
            self.record.xpath(
                f"count({self.xpath}/gmd:contact)",
                namespaces=self.ns.nsmap(),
            )
        )
        for contact_index in range(1, contacts_length + 1):
            contact = Contact(
                record=self.record, attributes=self.attributes, xpath=f"({self.xpath}/gmd:contact)[{contact_index}]"
            )
            _contact = contact.make_config()
            if bool(_contact):
                _contacts.append(_contact)
        if len(_contacts) > 0:
            # noinspection PyTypeChecker
            _["contacts"] = _contacts

        date_stamp = DateStamp(record=self.record, attributes=self.attributes, xpath=f"{self.xpath}")
        _date_stamp = date_stamp.make_config()
        if _date_stamp is not None:
            # noinspection PyTypeChecker
            _["date_stamp"] = _date_stamp

        metadata_standard = MetadataStandard(record=self.record, attributes=self.attributes, xpath=f"{self.xpath}")
        _metadata_standard = metadata_standard.make_config()
        if bool(_metadata_standard):
            _["metadata_standard"] = _metadata_standard

        reference_system_identifier = ReferenceSystemInfo(
            record=self.record, attributes=self.attributes, xpath=f"{self.xpath}"
        )
        _reference_system_identifier = reference_system_identifier.make_config()
        if bool(_reference_system_identifier):
            # noinspection PyTypeChecker
            _["reference_system_info"] = _reference_system_identifier

        _resource = {}

        data_identification = DataIdentification(record=self.record, attributes=self.attributes, xpath=f"{self.xpath}")
        _data_identification = data_identification.make_config()
        if bool(_data_identification):
            _resource = {**_resource, **_data_identification}

        data_distribution = DataDistribution(record=self.record, attributes=self.attributes, xpath=f"{self.xpath}")
        _data_distribution = data_distribution.make_config()
        if bool(_data_distribution):
            # detach distributors and merge into main contacts list
            if "distributors" in _data_distribution.keys():
                if "contacts" not in _resource.keys():  # pragma: no cover
                    _resource["contacts"] = []
                _resource["contacts"] = _resource["contacts"] + _data_distribution["distributors"]
                del _data_distribution["distributors"]
            _resource = {**_resource, **_data_distribution}

        data_quality = DataQuality(record=self.record, attributes=self.attributes, xpath=f"{self.xpath}")
        _data_quality = data_quality.make_config()
        if bool(_data_quality):
            _resource = {**_resource, **_data_quality}

        metadata_maintenance = MetadataMaintenance(
            record=self.record, attributes=self.attributes, xpath=f"{self.xpath}"
        )
        _metadata_maintenance = metadata_maintenance.make_config()
        if bool(_metadata_maintenance):
            # noinspection PyTypeChecker
            _["maintenance"] = _metadata_maintenance

        if "contacts" in _resource.keys():
            _resource["contacts"] = contacts_condense_roles(contacts=_resource["contacts"])
        if bool(_resource):
            _["resource"] = _resource
        return _

    def make_element(self):
        identifier = FileIdentifier(record=self.record, attributes=self.attributes, parent_element=self.record)
        identifier.make_element()

        if "language" in self.attributes:
            language = Language(record=self.record, attributes=self.attributes)
            language.make_element()

        if "character_set" in self.attributes:
            character_set = CharacterSet(record=self.record, attributes=self.attributes, xpath=f"{self.xpath}")
            character_set.make_element()

        if "hierarchy_level" in self.attributes:
            hierarchy_level = HierarchyLevel(record=self.record, attributes=self.attributes)
            hierarchy_level.make_element()

        for contact_attributes in self.attributes["contacts"]:
            for role in contact_attributes["role"]:
                _contact = contact_attributes.copy()
                _contact["role"] = role

                contact = Contact(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=self.record,
                    element_attributes=_contact,
                )
                contact.make_element()

        date_stamp = DateStamp(record=self.record, attributes=self.attributes)
        date_stamp.make_element()

        if "metadata_standard" in self.attributes:
            metadata_standard = MetadataStandard(
                record=self.record,
                attributes=self.attributes,
                parent_element=self.record,
                element_attributes=self.attributes["metadata_standard"],
            )
            metadata_standard.make_element()

        if "reference_system_info" in self.attributes:
            reference_system_info = ReferenceSystemInfo(
                record=self.record,
                attributes=self.attributes,
                parent_element=self.record,
                element_attributes=self.attributes["reference_system_info"],
            )
            reference_system_info.make_element()

        data_identification = DataIdentification(record=self.record, attributes=self.attributes)
        data_identification.make_element()

        if (
            "formats" in self.attributes["resource"]
            or "transfer_options" in self.attributes["resource"]
            or (
                "contacts" in self.attributes["resource"]
                and contacts_have_role(contacts=self.attributes["resource"]["contacts"], role="distributor")
            )
        ):
            data_distribution = DataDistribution(record=self.record, attributes=self.attributes)
            data_distribution.make_element()

        if (
            "hierarchy_level" in self.attributes
            or "measures" in self.attributes["resource"]
            or "lineage" in self.attributes["resource"]
        ):
            data_quality = DataQuality(record=self.record, attributes=self.attributes)
            data_quality.make_element()

        if "maintenance" in self.attributes:
            metadata_maintenance = MetadataMaintenance(
                record=self.record,
                attributes=self.attributes,
                parent_element=self.record,
                element_attributes=self.attributes["maintenance"],
            )
            metadata_maintenance.make_element()

        return self.record
