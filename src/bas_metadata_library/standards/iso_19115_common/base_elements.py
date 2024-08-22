from __future__ import annotations

from datetime import date

from lxml.etree import Element, SubElement

from bas_metadata_library import MetadataRecord
from bas_metadata_library.standards.iso_19115_common import CodeListElement, MetadataRecordElement
from bas_metadata_library.standards.iso_19115_common.common_elements import (
    AnchorElement,
    Citation,
    MaintenanceInformation,
    ResponsibleParty,
)
from bas_metadata_library.standards.iso_19115_common.utils import decode_date_string, encode_date_string


class FileIdentifier(MetadataRecordElement):
    def make_config(self) -> str:
        _ = ""

        value = self.record.xpath(
            f"{self.xpath}/gmd:fileIdentifier/gco:CharacterString/text()", namespaces=self.ns.nsmap()
        )
        if len(value) == 1:
            _ = value[0]

        return _

    def make_element(self) -> None:
        if "file_identifier" in self.attributes:
            file_identifier_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}fileIdentifier")
            file_identifier_value = SubElement(file_identifier_element, f"{{{self.ns.gco}}}CharacterString")
            file_identifier_value.text = self.attributes["file_identifier"]


class ScopeCode(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict | None = None,
        xpath: str | None = None,
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes,
            xpath=f"{xpath}/gmd:MD_ScopeCode",
        )
        self.code_list_values = [
            "aggregate",
            "application",
            "attribute",
            "attributeType",
            "collection",
            "collectionHardware",
            "collectionSession",
            "coverage",
            "dataset",
            "dimensionGroup",
            "document",
            "feature",
            "featureType",
            "fieldSession",
            "initiative",
            "metadata",
            "model",
            "nonGeographicDataset",
            "product",
            "propertyType",
            "repository",
            "sample",
            "series",
            "service",
            "software",
            "tile",
        ]
        self.code_list = "https://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_ScopeCode"
        self.element = f"{{{self.ns.gmd}}}level"
        self.element_code = f"{{{self.ns.gmd}}}MD_ScopeCode"
        self.attribute = "hierarchy_level"


class HierarchyLevel(ScopeCode):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict | None = None,
        xpath: str | None = None,
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes,
            xpath=xpath,
        )
        self.element = f"{{{self.ns.gmd}}}hierarchyLevel"

    def make_element(self) -> None:
        super().make_element()
        hierarchy_level_name_element = SubElement(self.record, f"{{{self.ns.gmd}}}hierarchyLevelName")
        if self.attribute in self.attributes and self.attributes[self.attribute] in self.code_list_values:
            hierarchy_level_name_value = SubElement(hierarchy_level_name_element, f"{{{self.ns.gco}}}CharacterString")
            hierarchy_level_name_value.text = self.attributes[self.attribute]


class Contact(MetadataRecordElement):
    @property
    def make_config(self) -> dict:
        responsible_party = ResponsibleParty(record=self.record, attributes=self.attributes, xpath=self.xpath)
        return responsible_party.make_config()

    def make_element(self) -> None:
        contact_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}contact")

        responsible_party = ResponsibleParty(
            record=self.record,
            attributes=self.attributes,
            parent_element=contact_element,
            element_attributes=self.element_attributes,
        )
        responsible_party.make_element()


class DateStamp(MetadataRecordElement):
    def make_config(self) -> date | None:
        _ = None

        value = self.record.xpath(f"{self.xpath}/gmd:dateStamp/gco:Date/text()", namespaces=self.ns.nsmap())
        if len(value) == 1:
            try:
                _ = decode_date_string(date_datetime=value[0])["date"]
            except ValueError:
                msg = "Datestamp could not be parsed as an ISO date value"
                raise RuntimeError(msg) from None

        return _

    def make_element(self) -> None:
        date_stamp_element = SubElement(self.record, f"{{{self.ns.gmd}}}dateStamp")
        date_stamp_value = SubElement(date_stamp_element, f"{{{self.ns.gco}}}Date")
        date_stamp_value.text = encode_date_string(self.attributes["date_stamp"])


class MetadataMaintenance(MetadataRecordElement):
    def make_config(self) -> dict:
        maintenance_information = MaintenanceInformation(
            record=self.record, attributes=self.attributes, xpath=f"{self.xpath}/gmd:metadataMaintenance"
        )
        return maintenance_information.make_config()

    def make_element(self) -> None:
        if "maintenance" in self.attributes["metadata"]:
            metadata_maintenance_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}metadataMaintenance")

            maintenance_information = MaintenanceInformation(
                record=self.record,
                attributes=self.attributes,
                parent_element=metadata_maintenance_element,
                element_attributes=self.attributes["metadata"]["maintenance"],
            )
            maintenance_information.make_element()


class MetadataStandard(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        standard_name = self.record.xpath(
            f"/{self.xpath}/gmd:metadataStandardName/gco:CharacterString/text()", namespaces=self.ns.nsmap()
        )
        if len(standard_name) == 1:
            _["name"] = standard_name[0]

        standard_version = self.record.xpath(
            f"/{self.xpath}/gmd:metadataStandardVersion/gco:CharacterString/text()", namespaces=self.ns.nsmap()
        )
        if len(standard_version) == 1:
            _["version"] = standard_version[0]

        return _

    def make_element(self) -> None:
        if "name" in self.element_attributes:
            metadata_standard_name_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}metadataStandardName")
            metadata_standard_name_value = SubElement(
                metadata_standard_name_element, f"{{{self.ns.gco}}}CharacterString"
            )
            metadata_standard_name_value.text = self.element_attributes["name"]

        if "version" in self.element_attributes:
            metadata_standard_version_element = SubElement(
                self.parent_element, f"{{{self.ns.gmd}}}metadataStandardVersion"
            )
            metadata_standard_version_value = SubElement(
                metadata_standard_version_element, f"{{{self.ns.gco}}}CharacterString"
            )
            metadata_standard_version_value.text = self.element_attributes["version"]


class ReferenceSystemInfo(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        authority = Citation(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/"
            f"gmd:RS_Identifier/gmd:authority",
        )
        _authority = authority.make_config()
        if bool(_authority):
            _["authority"] = _authority

        code_value = self.record.xpath(
            f"{self.xpath}/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/"
            f"gmd:RS_Identifier/gmd:code/gco:CharacterString/text() | {self.xpath}/gmd:referenceSystemInfo/"
            f"gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gmx:Anchor/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(code_value) == 1:
            if "code" not in _:
                _["code"] = {}
            _["code"]["value"] = code_value[0]

        code_href = self.record.xpath(
            f"{self.xpath}/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/"
            f"gmd:RS_Identifier/gmd:code/gmx:Anchor/@xlink:href",
            namespaces=self.ns.nsmap(),
        )
        if len(code_href) == 1:
            _["code"]["href"] = code_href[0]

        version_value = self.record.xpath(
            f"{self.xpath}/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/"
            f"gmd:RS_Identifier/gmd:version/gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(version_value) == 1:
            _["version"] = version_value[0]

        return _

    def make_element(self) -> None:
        reference_system_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}referenceSystemInfo")
        reference_system_element = SubElement(reference_system_wrapper, f"{{{self.ns.gmd}}}MD_ReferenceSystem")
        reference_system_identifier_wrapper = SubElement(
            reference_system_element, f"{{{self.ns.gmd}}}referenceSystemIdentifier"
        )
        reference_system_identifier_element = SubElement(
            reference_system_identifier_wrapper, f"{{{self.ns.gmd}}}RS_Identifier"
        )

        if "authority" in self.element_attributes:
            reference_system_identifier_authority_element = SubElement(
                reference_system_identifier_element, f"{{{self.ns.gmd}}}authority"
            )
            citation = Citation(
                record=self.record,
                attributes=self.attributes,
                parent_element=reference_system_identifier_authority_element,
                element_attributes=self.element_attributes["authority"],
            )
            citation.make_element()

        if "code" in self.element_attributes:
            reference_system_identifier_code_element = SubElement(
                reference_system_identifier_element, f"{{{self.ns.gmd}}}code"
            )
            if "href" in self.element_attributes["code"]:
                anchor = AnchorElement(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=reference_system_identifier_code_element,
                    element_attributes=self.element_attributes["code"],
                    element_value=self.element_attributes["code"]["value"],
                )
                anchor.make_element()
            else:
                reference_system_identifier_code_value = SubElement(
                    reference_system_identifier_code_element, f"{{{self.ns.gco}}}CharacterString"
                )
                reference_system_identifier_code_value.text = self.element_attributes["code"]["value"]

        if "version" in self.element_attributes:
            reference_system_identifier_version_element = SubElement(
                reference_system_identifier_element, f"{{{self.ns.gmd}}}version"
            )
            reference_system_identifier_version_value = SubElement(
                reference_system_identifier_version_element, f"{{{self.ns.gco}}}CharacterString"
            )
            reference_system_identifier_version_value.text = self.element_attributes["version"]
