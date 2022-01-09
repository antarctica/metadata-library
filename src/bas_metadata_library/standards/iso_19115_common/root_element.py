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
from bas_metadata_library.standards.iso_19115_common.utils import contacts_condense_roles


class ISOMetadataRecord(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {"metadata": {}, "identification": {}, "distribution": []}

        file_identifier = FileIdentifier(record=self.record, attributes=self.attributes, xpath=f"{self.xpath}")
        _file_identifier = file_identifier.make_config()
        if _file_identifier != "":
            # noinspection PyTypeChecker
            _["file_identifier"] = _file_identifier

        language = Language(record=self.record, attributes=self.attributes, xpath=f"{self.xpath}/gmd:language")
        _language = language.make_config()
        if _language != "":
            # noinspection PyTypeChecker
            _["metadata"]["language"] = _language

        character_set = CharacterSet(
            record=self.record, attributes=self.attributes, xpath=f"{self.xpath}/gmd:characterSet"
        )
        _character_set = character_set.make_config()
        if _character_set != "":
            # noinspection PyTypeChecker
            _["metadata"]["character_set"] = _character_set

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
            _["metadata"]["contacts"] = _contacts

        date_stamp = DateStamp(record=self.record, attributes=self.attributes, xpath=f"{self.xpath}")
        _date_stamp = date_stamp.make_config()
        if _date_stamp is not None:
            # noinspection PyTypeChecker
            _["metadata"]["date_stamp"] = _date_stamp

        metadata_standard = MetadataStandard(record=self.record, attributes=self.attributes, xpath=f"{self.xpath}")
        _metadata_standard = metadata_standard.make_config()
        if bool(_metadata_standard):
            _["metadata"]["metadata_standard"] = _metadata_standard

        reference_system_identifier = ReferenceSystemInfo(
            record=self.record, attributes=self.attributes, xpath=f"{self.xpath}"
        )
        _reference_system_identifier = reference_system_identifier.make_config()
        if bool(_reference_system_identifier):
            # noinspection PyTypeChecker
            _["reference_system_info"] = _reference_system_identifier

        data_identification = DataIdentification(record=self.record, attributes=self.attributes, xpath=f"{self.xpath}")
        _data_identification = data_identification.make_config()
        if bool(_data_identification):
            _["identification"] = {**_["identification"], **_data_identification}

        data_distribution = DataDistribution(record=self.record, attributes=self.attributes, xpath=f"{self.xpath}")
        _data_distribution = data_distribution.make_config()
        if len(_data_distribution) > 0:
            _["distribution"] = _data_distribution

        data_quality = DataQuality(record=self.record, attributes=self.attributes, xpath=f"{self.xpath}")
        _data_quality = data_quality.make_config()
        if bool(_data_quality):
            _["identification"] = {**_["identification"], **_data_quality}

        metadata_maintenance = MetadataMaintenance(
            record=self.record, attributes=self.attributes, xpath=f"{self.xpath}"
        )
        _metadata_maintenance = metadata_maintenance.make_config()
        if bool(_metadata_maintenance):
            # noinspection PyTypeChecker
            _["metadata"]["maintenance"] = _metadata_maintenance

        if "identification" in _.keys() and "contacts" in _["identification"].keys():
            _["identification"]["contacts"] = contacts_condense_roles(contacts=_["identification"]["contacts"])

        if not _["distribution"]:
            del _["distribution"]

        return _

    def make_element(self):
        if "file_identifier" in self.attributes:
            identifier = FileIdentifier(record=self.record, attributes=self.attributes, parent_element=self.record)
            identifier.make_element()

        if "metadata" in self.attributes and "language" in self.attributes["metadata"]:
            language = Language(record=self.record, attributes=self.attributes["metadata"])
            language.make_element()

        if "metadata" in self.attributes and "character_set" in self.attributes["metadata"]:
            character_set = CharacterSet(
                record=self.record, attributes=self.attributes["metadata"], xpath=f"{self.xpath}"
            )
            character_set.make_element()

        if "hierarchy_level" in self.attributes:
            hierarchy_level = HierarchyLevel(record=self.record, attributes=self.attributes)
            hierarchy_level.make_element()

        if "metadata" in self.attributes and "contacts" in self.attributes["metadata"]:
            for contact_attributes in self.attributes["metadata"]["contacts"]:
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

        if "metadata" in self.attributes and "date_stamp" in self.attributes["metadata"]:
            date_stamp = DateStamp(record=self.record, attributes=self.attributes["metadata"])
            date_stamp.make_element()

        if "metadata" in self.attributes and "metadata_standard" in self.attributes["metadata"]:
            metadata_standard = MetadataStandard(
                record=self.record,
                attributes=self.attributes,
                parent_element=self.record,
                element_attributes=self.attributes["metadata"]["metadata_standard"],
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

        if "identification" in self.attributes:
            data_identification = DataIdentification(record=self.record, attributes=self.attributes)
            data_identification.make_element()

        if "distribution" in self.attributes:
            data_distribution = DataDistribution(
                record=self.record, attributes=self.attributes, element_attributes=self.attributes["distribution"]
            )
            data_distribution.make_element()

        # if
        #   [hierarchy_level] or
        #   [identification][measures] or
        #   [identification][lineage]
        if ("hierarchy_level" in self.attributes) or (
            "identification" in self.attributes
            and ("measures" in self.attributes["identification"] or "lineage" in self.attributes["identification"])
        ):
            data_quality = DataQuality(record=self.record, attributes=self.attributes)
            data_quality.make_element()

        if "metadata" in self.attributes and "maintenance" in self.attributes["metadata"]:
            metadata_maintenance = MetadataMaintenance(
                record=self.record,
                attributes=self.attributes,
                parent_element=self.record,
                element_attributes=self.attributes["metadata"]["maintenance"],
            )
            metadata_maintenance.make_element()

        return self.record
