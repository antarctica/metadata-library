from __future__ import annotations

import contextlib
import json
from hashlib import sha1
from json import JSONDecodeError

from lxml.etree import Element, SubElement

from bas_metadata_library import MetadataRecord
from bas_metadata_library.standards.iso_19115_common import CodeListElement, MetadataRecordElement
from bas_metadata_library.standards.iso_19115_common.common_elements import (
    AnchorElement,
    CharacterSet,
    Citation,
    Format,
    Identifier,
    Language,
    MaintenanceInformation,
    ResponsibleParty,
)
from bas_metadata_library.standards.iso_19115_common.utils import (
    decode_date_string,
    encode_date_string,
    format_numbers_consistently,
)


class DataIdentification(MetadataRecordElement):
    """gmd:identificationInfo."""

    def make_config(  # noqa: C901 see uk-pdc/metadata-infrastructure/metadata-library#175 for more information
        self,
    ) -> dict:
        """Decode to Python."""
        _ = {}

        citation = Citation(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation",
        )
        _citation = citation.make_config()
        if bool(_citation):
            _ = {**_, **_citation}

        abstract = Abstract(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:abstract",
        )
        _abstract = abstract.make_config()
        if _abstract != "":
            _["abstract"] = _abstract

        purpose = Purpose(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:purpose",
        )
        _purpose = purpose.make_config()
        if _purpose != "":
            _["purpose"] = _purpose

        credit = Credit(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:credit",
        )
        _credit = credit.make_config()
        if _credit != "":
            _["credit"] = _credit

        status = Status(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:status",
        )
        _status = status.make_config()
        if _status != "":
            _["status"] = _status

        _contacts = []
        contacts_length = int(
            self.record.xpath(
                f"count({self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact)",
                namespaces=self.ns.nsmap(),
            )
        )
        for contact_index in range(1, contacts_length + 1):
            contact = PointOfContact(
                record=self.record,
                attributes=self.attributes,
                xpath=f"({self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact)"
                f"[{contact_index}]",
            )
            _contact = contact.make_config()
            if bool(_contact):
                _contacts.append(_contact)
        if len(_contacts) > 0:
            _["contacts"] = _contacts

        identification_maintenance = ResourceMaintenance(
            record=self.record, attributes=self.attributes, xpath=f"{self.xpath}"
        )
        _identification_maintenance = identification_maintenance.make_config()
        if bool(_identification_maintenance):
            _["maintenance"] = _identification_maintenance

        _graphic_overviews = []
        graphics_length = int(
            self.record.xpath(
                f"count({self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:graphicOverview)",
                namespaces=self.ns.nsmap(),
            )
        )
        for graphic_index in range(1, graphics_length + 1):
            graphic_overview = GraphicOverview(
                record=self.record,
                attributes=self.attributes,
                xpath=f"({self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/"
                f"gmd:graphicOverview)[{graphic_index}]",
            )
            _graphic_overview = graphic_overview.make_config()
            if bool(_graphic_overview):
                _graphic_overviews.append(_graphic_overview)
        if len(_graphic_overviews) > 0:
            _["graphic_overviews"] = _graphic_overviews

        _resource_formats = []
        resources_formats_length = int(
            self.record.xpath(
                f"count({self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceFormat)",
                namespaces=self.ns.nsmap(),
            )
        )
        for resource_format_index in range(1, resources_formats_length + 1):
            resource_option_format = ResourceFormat(
                record=self.record,
                attributes=self.attributes,
                xpath=f"({self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceFormat)"
                f"[{resource_format_index}]",
            )
            _resource_option_format = resource_option_format.make_config()
            if bool(_resource_option_format):
                _resource_formats.append(_resource_option_format)
        if len(_resource_formats) > 0:
            _["resource_formats"] = _resource_formats

        _descriptive_keywords = []
        keywords_length = int(
            self.record.xpath(
                f"count({self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords)",
                namespaces=self.ns.nsmap(),
            )
        )
        for keyword_index in range(1, keywords_length + 1):
            keywords = DescriptiveKeywords(
                record=self.record,
                attributes=self.attributes,
                xpath=f"({self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords)"
                f"[{keyword_index}]",
            )
            _keywords = keywords.make_config()
            if bool(_keywords):
                _descriptive_keywords.append(_keywords)
        if len(_descriptive_keywords) > 0:
            _["keywords"] = _descriptive_keywords

        _resource_constraints = []
        constraints_length = int(
            self.record.xpath(
                f"count({self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints)",
                namespaces=self.ns.nsmap(),
            )
        )
        for constraint_index in range(1, constraints_length + 1):
            constraint = ResourceConstraint(
                record=self.record,
                attributes=self.attributes,
                xpath=f"({self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints)"
                f"[{constraint_index}]",
            )
            _constraint = constraint.make_config()
            if bool(_constraint):
                _resource_constraints.append(_constraint)
        if len(_resource_constraints) > 0:
            _["constraints"] = _resource_constraints

        _resource_aggregations = []
        aggregations_length = int(
            self.record.xpath(
                f"count({self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:aggregationInfo)",
                namespaces=self.ns.nsmap(),
            )
        )
        for aggregate_index in range(1, aggregations_length + 1):
            aggregation = Aggregation(
                record=self.record,
                attributes=self.attributes,
                xpath=f"({self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:aggregationInfo)"
                f"[{aggregate_index}]",
            )
            _aggregation = aggregation.make_config()
            if bool(_aggregation):
                _resource_aggregations.append(_aggregation)
        if len(_resource_aggregations) > 0:
            _["aggregations"] = _resource_aggregations

        spatial_representation_type = SpatialRepresentationType(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialRepresentationType",
        )
        _spatial_representation_type = spatial_representation_type.make_config()
        if _spatial_representation_type != "":
            _["spatial_representation_type"] = _spatial_representation_type

        spatial_resolution = SpatialResolution(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution",
        )
        _spatial_resolution = spatial_resolution.make_config()
        if _spatial_resolution != "":
            _["spatial_resolution"] = _spatial_resolution

        language = Language(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:language",
        )
        _language = language.make_config()
        if _language != "":
            _["language"] = _language

        character_set = CharacterSet(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:characterSet",
        )
        _character_set = character_set.make_config()
        if _character_set != "":
            _["character_set"] = _character_set

        _topic_categories = []
        topics_length = int(
            self.record.xpath(
                f"count({self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:topicCategory)",
                namespaces=self.ns.nsmap(),
            )
        )
        for topic_index in range(1, topics_length + 1):
            topic = TopicCategory(
                record=self.record,
                attributes=self.attributes,
                xpath=f"({self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:topicCategory)"
                f"[{topic_index}]",
            )
            _topic = topic.make_config()
            if _topic != "":
                _topic_categories.append(_topic)
        if len(_topic_categories) > 0:
            _["topics"] = _topic_categories

        _extents = []
        extents_length = int(
            self.record.xpath(
                f"count({self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent)",
                namespaces=self.ns.nsmap(),
            )
        )
        for extent_index in range(1, extents_length + 1):
            extent = Extent(
                record=self.record,
                attributes=self.attributes,
                xpath=f"({self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent)" f"[{extent_index}]",
            )
            _extent = extent.make_config()
            if _extent != "":
                _extents.append(_extent)
        if len(_extents) > 0:
            _["extents"] = _extents

        supplemental_information = SupplementalInformation(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:supplementalInformation",
        )
        _supplemental_information = supplemental_information.make_config()
        if _supplemental_information != "":
            _["supplemental_information"] = _supplemental_information

        return _

    def make_element(self) -> None:  # noqa: C901 see uk-pdc/metadata-infrastructure/metadata-library#175 for more information
        """Encode as XML."""
        data_identification_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}identificationInfo")
        data_identification_element = SubElement(data_identification_wrapper, f"{{{self.ns.gmd}}}MD_DataIdentification")

        citation_wrapper = SubElement(data_identification_element, f"{{{self.ns.gmd}}}citation")
        citation = Citation(
            record=self.record,
            attributes=self.attributes,
            parent_element=citation_wrapper,
            element_attributes=self.element_attributes["identification"],
        )
        citation.make_element()

        abstract = Abstract(
            record=self.record,
            attributes=self.attributes,
            parent_element=data_identification_element,
            element_attributes=self.attributes["identification"],
        )
        abstract.make_element()

        if "purpose" in self.attributes["identification"]:
            purpose = Purpose(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=self.attributes["identification"],
            )
            purpose.make_element()

        if "credit" in self.attributes["identification"]:
            credit = Credit(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=self.attributes["identification"],
            )
            credit.make_element()

        if "status" in self.attributes["identification"]:
            status = Status(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=self.attributes["identification"],
            )
            status.make_element()

        if "contacts" in self.attributes["identification"]:
            for point_of_contact_attributes in self.attributes["identification"]["contacts"]:
                for role in point_of_contact_attributes["role"]:
                    if role != "distributor":
                        _point_of_contact = point_of_contact_attributes.copy()
                        _point_of_contact["role"] = role

                        point_of_contact = PointOfContact(
                            record=self.record,
                            attributes=self.attributes,
                            parent_element=data_identification_element,
                            element_attributes=_point_of_contact,
                        )
                        point_of_contact.make_element()

        if "maintenance" in self.attributes["identification"]:
            identification_maintenance = ResourceMaintenance(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=self.element_attributes["identification"]["maintenance"],
            )
            identification_maintenance.make_element()

        if "graphic_overviews" in self.attributes["identification"]:
            for graphic_overview_attributes in self.attributes["identification"]["graphic_overviews"]:
                graphic_overview = GraphicOverview(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=data_identification_element,
                    element_attributes=graphic_overview_attributes,
                )
                graphic_overview.make_element()

        if "resource_formats" in self.attributes["identification"]:
            for resource_format_attributes in self.attributes["identification"]["resource_formats"]:
                resource_format = ResourceFormat(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=data_identification_element,
                    element_attributes=resource_format_attributes,
                )
                resource_format.make_element()

        if "keywords" in self.attributes["identification"]:
            for keyword_attributes in self.attributes["identification"]["keywords"]:
                descriptive_keywords = DescriptiveKeywords(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=data_identification_element,
                    element_attributes=keyword_attributes,
                )
                descriptive_keywords.make_element()

        if "constraints" in self.attributes["identification"]:
            for constraint_attributes in self.attributes["identification"]["constraints"]:
                constraint = ResourceConstraint(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=data_identification_element,
                    element_attributes=constraint_attributes,
                )
                constraint.make_element()

        if "aggregations" in self.attributes["identification"]:
            for aggregation_attributes in self.attributes["identification"]["aggregations"]:
                aggregation = Aggregation(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=data_identification_element,
                    element_attributes=aggregation_attributes,
                )
                aggregation.make_element()

        if "spatial_representation_type" in self.attributes["identification"]:
            spatial_representation_type = SpatialRepresentationType(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=self.attributes["identification"],
            )
            spatial_representation_type.make_element()

        if "spatial_resolution" in self.attributes["identification"]:
            spatial_resolution = SpatialResolution(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=self.attributes["identification"],
            )
            spatial_resolution.make_element()

        language = Language(
            record=self.record,
            attributes=self.attributes,
            parent_element=data_identification_element,
            element_attributes=self.attributes["identification"],
        )
        language.make_element()

        if "character_set" in self.attributes["identification"]:
            character_set = CharacterSet(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=self.attributes["identification"],
            )
            character_set.make_element()

        if "topics" in self.attributes["identification"]:
            for topic_attribute in self.attributes["identification"]["topics"]:
                topic = TopicCategory(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=data_identification_element,
                    element_attributes={"topic": topic_attribute},
                )
                topic.make_element()

        if "extents" in self.attributes["identification"]:
            for extent_attribute in self.attributes["identification"]["extents"]:
                extent = Extent(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=data_identification_element,
                    element_attributes={"extent": extent_attribute},
                )
                extent.make_element()

        if "supplemental_information" in self.attributes["identification"]:
            supplemental_information = SupplementalInformation(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=self.attributes["identification"],
            )
            supplemental_information.make_element()


class Abstract(MetadataRecordElement):
    def make_config(self) -> str:
        _ = ""

        abstract_value = self.record.xpath(f"{self.xpath}/gco:CharacterString/text()", namespaces=self.ns.nsmap())
        if len(abstract_value) == 1:
            _ = abstract_value[0]

        return _

    def make_element(self) -> None:
        abstract_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}abstract")
        abstract_value = SubElement(abstract_element, f"{{{self.ns.gco}}}CharacterString")
        abstract_value.text = self.element_attributes["abstract"]


class Purpose(MetadataRecordElement):
    def make_config(self) -> str:
        _ = ""

        purpose_value = self.record.xpath(f"{self.xpath}/gco:CharacterString/text()", namespaces=self.ns.nsmap())
        if len(purpose_value) == 1:
            _ = purpose_value[0]

        return _

    def make_element(self) -> None:
        purpose_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}purpose")
        purpose_value = SubElement(purpose_element, f"{{{self.ns.gco}}}CharacterString")
        purpose_value.text = self.element_attributes["purpose"]


class Credit(MetadataRecordElement):
    def make_config(self) -> str:
        _ = ""

        credit_value = self.record.xpath(f"{self.xpath}/gco:CharacterString/text()", namespaces=self.ns.nsmap())
        if len(credit_value) == 1:
            _ = credit_value[0]

        return _

    def make_element(self) -> None:
        credit_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}credit")
        credit_value = SubElement(credit_element, f"{{{self.ns.gco}}}CharacterString")
        credit_value.text = self.element_attributes["credit"]


class Status(CodeListElement):
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
            xpath=f"{xpath}/gmd:MD_ProgressCode",
        )
        self.code_list_values = [
            "completed",
            "historicalArchive",
            "obsolete",
            "onGoing",
            "planned",
            "required",
            "underDevelopment",
        ]
        self.code_list = (
            "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/"
            "codelist/gmxCodelists.xml#MD_ProgressCode"
        )
        self.element = f"{{{self.ns.gmd}}}status"
        self.element_code = f"{{{self.ns.gmd}}}MD_ProgressCode"
        self.attribute = "status"


class PointOfContact(MetadataRecordElement):
    def make_config(self) -> dict:
        responsible_party = ResponsibleParty(record=self.record, attributes=self.attributes, xpath=self.xpath)
        return responsible_party.make_config()

    def make_element(self) -> None:
        point_of_contact_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}pointOfContact")

        responsible_party = ResponsibleParty(
            record=self.record,
            attributes=self.attributes,
            parent_element=point_of_contact_element,
            element_attributes=self.element_attributes,
        )
        responsible_party.make_element()


class ResourceMaintenance(MetadataRecordElement):
    def make_config(self) -> dict:
        maintenance_information = MaintenanceInformation(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceMaintenance",
        )
        return maintenance_information.make_config()

    def make_element(self) -> None:
        resource_maintenance_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}resourceMaintenance")
        maintenance_information = MaintenanceInformation(
            record=self.record,
            attributes=self.attributes,
            parent_element=resource_maintenance_element,
            element_attributes=self.element_attributes,
        )
        maintenance_information.make_element()


class GraphicOverview(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        identifier_value = self.record.xpath(f"{self.xpath}/gmd:MD_BrowseGraphic/@id", namespaces=self.ns.nsmap())
        if len(identifier_value) == 1:
            _["identifier"] = identifier_value[0]

        href_value = self.record.xpath(
            f"{self.xpath}/gmd:MD_BrowseGraphic/gmd:fileName/gco:CharacterString/text()", namespaces=self.ns.nsmap()
        )
        if len(href_value) == 1:
            _["href"] = href_value[0]

        description_value = self.record.xpath(
            f"{self.xpath}/gmd:MD_BrowseGraphic/gmd:fileDescription/gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(description_value) == 1:
            _["description"] = description_value[0]

        mime_type_value = self.record.xpath(
            f"{self.xpath}/gmd:MD_BrowseGraphic/gmd:fileType/gco:CharacterString/text()", namespaces=self.ns.nsmap()
        )
        if len(mime_type_value) == 1:
            _["mime_type"] = mime_type_value[0]

        return _

    def make_element(self) -> None:
        graphic_wrapper = SubElement(
            self.parent_element,
            f"{{{self.ns.gmd}}}graphicOverview",
        )
        graphic_element = SubElement(
            graphic_wrapper,
            f"{{{self.ns.gmd}}}MD_BrowseGraphic",
            attrib={"id": self.element_attributes["identifier"]},
        )

        href_element = SubElement(graphic_element, f"{{{self.ns.gmd}}}fileName")
        href_value = SubElement(href_element, f"{{{self.ns.gco}}}CharacterString")
        href_value.text = self.element_attributes["href"]

        if "description" in self.element_attributes:
            description_element = SubElement(graphic_element, f"{{{self.ns.gmd}}}fileDescription")
            description_value = SubElement(description_element, f"{{{self.ns.gco}}}CharacterString")
            description_value.text = self.element_attributes["description"]

        if "mime_type" in self.element_attributes:
            mime_type_element = SubElement(graphic_element, f"{{{self.ns.gmd}}}fileType")
            mime_type_value = SubElement(mime_type_element, f"{{{self.ns.gco}}}CharacterString")
            mime_type_value.text = self.element_attributes["mime_type"]


class DescriptiveKeywords(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        _terms = []
        terms_values = self.record.xpath(
            f"{self.xpath}/gmd:MD_Keywords/gmd:keyword/gco:CharacterString/text()", namespaces=self.ns.nsmap()
        )
        for term in terms_values:
            _terms.append({"term": term})
        terms_links = self.record.xpath(
            f"{self.xpath}/gmd:MD_Keywords/gmd:keyword/gmx:Anchor", namespaces=self.ns.nsmap()
        )
        for term in terms_links:
            _term = {}
            _term_value = term.xpath("./text()", namespaces=self.ns.nsmap())
            if len(_term_value) > 0:
                _term["term"] = _term_value[0]
            _term_href = term.xpath("./@xlink:href", namespaces=self.ns.nsmap())
            if len(_term_href) > 0:
                _term["href"] = _term_href[0]
            if bool(_term):
                _terms.append(_term)
        if bool(_terms):
            _["terms"] = _terms

        descriptive_keywords_type = DescriptiveKeywordsType(
            record=self.record, attributes=self.attributes, xpath=f"{self.xpath}/gmd:MD_Keywords/gmd:type"
        )
        _descriptive_keywords_type = descriptive_keywords_type.make_config()
        if _descriptive_keywords_type != "":
            _["type"] = _descriptive_keywords_type

        thesaurus = Thesaurus(
            record=self.record, attributes=self.attributes, xpath=f"{self.xpath}/gmd:MD_Keywords/gmd:thesaurusName"
        )
        _thesaurus = thesaurus.make_config()
        if bool(_thesaurus):
            _["thesaurus"] = _thesaurus

        return _

    def make_element(self) -> None:
        keywords_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}descriptiveKeywords")
        keywords_element = SubElement(keywords_wrapper, f"{{{self.ns.gmd}}}MD_Keywords")

        for term in self.element_attributes["terms"]:
            term_element = SubElement(keywords_element, f"{{{self.ns.gmd}}}keyword")
            if "href" in term:
                anchor = AnchorElement(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=term_element,
                    element_attributes=term,
                    element_value=term["term"],
                )
                anchor.make_element()
            else:
                term_value = SubElement(term_element, f"{{{self.ns.gco}}}CharacterString")
                term_value.text = term["term"]

        if "type" in self.element_attributes:
            keyword_type = DescriptiveKeywordsType(
                record=self.record,
                attributes=self.attributes,
                parent_element=keywords_element,
                element_attributes=self.element_attributes,
            )
            keyword_type.make_element()

        if "thesaurus" in self.element_attributes:
            thesaurus = Thesaurus(
                record=self.record,
                attributes=self.attributes,
                parent_element=keywords_element,
                element_attributes=self.element_attributes["thesaurus"],
            )
            thesaurus.make_element()


class DescriptiveKeywordsType(CodeListElement):
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
            xpath=f"{xpath}/gmd:MD_KeywordTypeCode",
        )
        self.code_list_values = ["discipline", "place", "stratum", "temporal", "theme"]
        self.code_list = (
            "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/"
            "codelist/gmxCodelists.xml#MD_KeywordTypeCode"
        )
        self.element = f"{{{self.ns.gmd}}}type"
        self.element_code = f"{{{self.ns.gmd}}}MD_KeywordTypeCode"
        self.attribute = "type"


class Thesaurus(MetadataRecordElement):
    def make_config(self) -> dict:
        citation = Citation(record=self.record, attributes=self.attributes, xpath=self.xpath)
        return citation.make_config()

    def make_element(self) -> None:
        thesaurus_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}thesaurusName")

        citation = Citation(
            record=self.record,
            attributes=self.attributes,
            parent_element=thesaurus_element,
            element_attributes=self.element_attributes,
        )
        citation.make_element()


class ResourceConstraint(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        access_constraint = AccessConstraint(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:MD_LegalConstraints/gmd:accessConstraints",
        )
        _access_constraint = access_constraint.make_config()
        if _access_constraint != "":
            _["type"] = "access"
            _["restriction_code"] = _access_constraint

        use_constraint = UseConstraint(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:MD_LegalConstraints/gmd:useConstraints",
        )
        _use_constraint = use_constraint.make_config()
        if _use_constraint != "":
            _["type"] = "usage"
            _["restriction_code"] = _use_constraint

        other_constraint = OtherConstraints(
            record=self.record, attributes=self.attributes, xpath=f"{self.xpath}/gmd:MD_LegalConstraints"
        )
        _other_constraint = other_constraint.make_config()
        if len(_other_constraint) > 0:
            _ = {**_, **_other_constraint}

        # detect permissions statements
        constraint_id = self.record.xpath(f"{self.xpath}/gmd:MD_LegalConstraints/@id", namespaces=self.ns.nsmap())
        if len(constraint_id) == 1 and "permissions" in constraint_id[0] and "statement" in _:
            _["permissions"] = _["statement"]
            del _["statement"]
            with contextlib.suppress(JSONDecodeError):
                _["permissions"] = json.loads(_["permissions"])

        return _

    def make_element(self) -> None:
        constraints_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}resourceConstraints")
        constraints_element = SubElement(constraints_wrapper, f"{{{self.ns.gmd}}}MD_LegalConstraints")

        if self.element_attributes["type"] == "access":
            access_constraint = AccessConstraint(
                record=self.record,
                attributes=self.attributes,
                parent_element=constraints_element,
                element_attributes=self.element_attributes,
            )
            access_constraint.make_element()

        if self.element_attributes["type"] == "usage":
            usage_constraint = UseConstraint(
                record=self.record,
                attributes=self.attributes,
                parent_element=constraints_element,
                element_attributes=self.element_attributes,
            )
            usage_constraint.make_element()

        if "statement" in self.element_attributes or "href" in self.element_attributes:
            other_constraint = OtherConstraints(
                record=self.record,
                attributes=self.attributes,
                parent_element=constraints_element,
                element_attributes=self.element_attributes,
            )
            other_constraint.make_element()

        if "permissions" in self.element_attributes:
            # Bandit S324 warning is exempted as these hashes are not used for any security related purposes
            _id = sha1(json.dumps(self.element_attributes["permissions"]).encode()).hexdigest()  # noqa: S324
            constraints_element.attrib["id"] = f"bml-permissions-{_id}"

            _statement = self.element_attributes["permissions"]
            if not isinstance(_statement, str):
                _statement = json.dumps(_statement)

            other_constraint = OtherConstraints(
                record=self.record,
                attributes=self.attributes,
                parent_element=constraints_element,
                element_attributes={"statement": _statement},
            )
            other_constraint.make_element()


class AccessConstraint(CodeListElement):
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
            xpath=f"{xpath}/gmd:MD_RestrictionCode",
        )
        self.code_list_values = [
            "confidential",
            "copyright",
            "inConfidence",
            "intellectualPropertyRights",
            "licenceDistributor",
            "licenceEndUser",
            "licenceUnrestricted",
            "license",
            "otherRestrictions",
            "patent",
            "patentPending",
            "private",
            "restricted",
            "SBU",
            "statutory",
            "trademark",
            "unrestricted",
        ]
        self.code_list = "https://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_RestrictionCode"
        self.element = f"{{{self.ns.gmd}}}accessConstraints"
        self.element_code = f"{{{self.ns.gmd}}}MD_RestrictionCode"
        self.attribute = "restriction_code"


class UseConstraint(CodeListElement):
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
            xpath=f"{xpath}/gmd:MD_RestrictionCode",
        )
        self.code_list_values = [
            "confidential",
            "copyright",
            "inConfidence",
            "intellectualPropertyRights",
            "licenceDistributor",
            "licenceEndUser",
            "licenceUnrestricted",
            "license",
            "otherRestrictions",
            "patent",
            "patentPending",
            "private",
            "restricted",
            "SBU",
            "statutory",
            "trademark",
            "unrestricted",
        ]
        self.code_list = "https://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_RestrictionCode"
        self.element = f"{{{self.ns.gmd}}}useConstraints"
        self.element_code = f"{{{self.ns.gmd}}}MD_RestrictionCode"
        self.attribute = "restriction_code"


class OtherConstraints(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        other_constraint_value = self.record.xpath(
            f"{self.xpath}/gmd:otherConstraints/gco:CharacterString/text() | "
            f"{self.xpath}/gmd:otherConstraints/gmx:Anchor/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(other_constraint_value) == 1:
            _["statement"] = other_constraint_value[0]

        other_constraint_href = self.record.xpath(
            f"{self.xpath}/gmd:otherConstraints/gmx:Anchor/@xlink:href", namespaces=self.ns.nsmap()
        )
        if len(other_constraint_href) == 1:
            _["href"] = other_constraint_href[0]
            # account for constraints that use a URL only,
            # as the text value will repeat the URL, so it can encoded properly
            if "statement" in _ and _["statement"] == _["href"]:
                del _["statement"]

        return _

    def make_element(self) -> None:
        other_constraints_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}otherConstraints")

        if "href" in self.element_attributes:
            # where a constraint only has a URL, use this as a text value as well
            # when decoded, this fake value/statement value will be removed
            element_value = self.element_attributes["href"]
            if "statement" in self.element_attributes:
                element_value = self.element_attributes["statement"]

            anchor = AnchorElement(
                record=self.record,
                attributes=self.attributes,
                parent_element=other_constraints_element,
                element_attributes=self.element_attributes,
                element_value=element_value,
            )
            anchor.make_element()
        else:
            other_constraints_value = SubElement(other_constraints_element, f"{{{self.ns.gco}}}CharacterString")
            other_constraints_value.text = self.element_attributes["statement"]


class Aggregation(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        association_type = AssociationType(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:MD_AggregateInformation/gmd:associationType",
        )
        _association_type = association_type.make_config()
        if _association_type != "":
            _["association_type"] = _association_type

        initiative_type = InitiativeType(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:MD_AggregateInformation/gmd:initiativeType",
        )
        _initiative_type = initiative_type.make_config()
        if _initiative_type != "":
            _["initiative_type"] = _initiative_type

        identifier = Identifier(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:MD_AggregateInformation/gmd:aggregateDataSetIdentifier",
        )
        _identifier = identifier.make_config()
        if bool(_identifier):
            _["identifier"] = _identifier

        return _

    def make_element(self) -> None:
        aggregation_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}aggregationInfo")
        aggregation_element = SubElement(aggregation_wrapper, f"{{{self.ns.gmd}}}MD_AggregateInformation")

        identifier = Identifier(
            record=self.record,
            attributes=self.attributes,
            parent_element=aggregation_element,
            element_attributes=self.element_attributes["identifier"],
            identifier_container=f"{{{self.ns.gmd}}}aggregateDataSetIdentifier",
        )
        identifier.make_element()

        association_type = AssociationType(
            record=self.record,
            attributes=self.attributes,
            parent_element=aggregation_element,
            element_attributes=self.element_attributes,
        )
        association_type.make_element()

        if "initiative_type" in self.element_attributes:
            initiative_type = InitiativeType(
                record=self.record,
                attributes=self.attributes,
                parent_element=aggregation_element,
                element_attributes=self.element_attributes,
            )
            initiative_type.make_element()


class AssociationType(CodeListElement):
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
            xpath=f"{xpath}/gmd:DS_AssociationTypeCode",
        )
        self.code_list_values = [
            "collectiveTitle",
            "crossReference",
            "dependency",
            "isComposedOf",
            "largerWorkCitation",
            "partOfSeamlessDatabase",
            "revisionOf",
            "series",
            "stereoMate",
            "physicalReverseOf",
        ]
        self.code_list = (
            "https://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#DS_AssociationTypeCode"
        )
        self.element = f"{{{self.ns.gmd}}}associationType"
        self.element_code = f"{{{self.ns.gmd}}}DS_AssociationTypeCode"
        self.attribute = "association_type"


class InitiativeType(CodeListElement):
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
            xpath=f"{xpath}/gmd:DS_InitiativeTypeCode",
        )
        self.code_list_values = [
            "campaign",
            "collection",
            "exercise",
            "experiment",
            "investigation",
            "mission",
            "operation",
            "platform",
            "process",
            "program",
            "project",
            "sensor",
            "study",
            "task",
            "trial",
            "dataDictionary",
            "sciencePaper",
            "userGuide",
        ]
        self.code_list = (
            "https://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#DS_InitiativeTypeCode"
        )
        self.element = f"{{{self.ns.gmd}}}initiativeType"
        self.element_code = f"{{{self.ns.gmd}}}DS_InitiativeTypeCode"
        self.attribute = "initiative_type"


class SupplementalInformation(MetadataRecordElement):
    def make_config(self) -> str:
        _ = ""

        supplemental_value = self.record.xpath(f"{self.xpath}/gco:CharacterString/text()", namespaces=self.ns.nsmap())
        if len(supplemental_value) == 1:
            _ = supplemental_value[0]

        return _

    def make_element(self) -> None:
        if "supplemental_information" in self.element_attributes:
            supplemental_info_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}supplementalInformation")
            supplemental_info_value = SubElement(supplemental_info_element, f"{{{self.ns.gco}}}CharacterString")
            supplemental_info_value.text = self.element_attributes["supplemental_information"]


class SpatialRepresentationType(CodeListElement):
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
            xpath=f"{xpath}/gmd:MD_SpatialRepresentationTypeCode",
        )
        self.code_list_values = ["vector", "grid", "textTable", "tin", "stereoModel", "video"]
        self.code_list = (
            "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/"
            "codelist/gmxCodelists.xml#MD_SpatialRepresentationTypeCode"
        )
        self.element = f"{{{self.ns.gmd}}}spatialRepresentationType"
        self.element_code = f"{{{self.ns.gmd}}}MD_SpatialRepresentationTypeCode"
        self.attribute = "spatial_representation_type"


class SpatialResolution(MetadataRecordElement):
    def make_config(self) -> str:
        _ = ""

        spatial_resolution_value = self.record.xpath(
            f"{self.xpath}/gmd:MD_Resolution/gmd:equivalentScale/gmd:MD_RepresentativeFraction/gmd:denominator/"
            f"gco:Integer/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(spatial_resolution_value) == 1:
            _ = format_numbers_consistently(spatial_resolution_value[0])

        return _

    def make_element(self) -> None:
        if self.element_attributes["spatial_resolution"] is None:
            SubElement(
                self.parent_element,
                f"{{{self.ns.gmd}}}spatialResolution",
                attrib={f"{{{self.ns.gco}}}nilReason": "inapplicable"},
            )
        else:
            resolution_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}spatialResolution")
            resolution_element = SubElement(resolution_wrapper, f"{{{self.ns.gmd}}}MD_Resolution")
            equivalent_scale_wrapper = SubElement(resolution_element, f"{{{self.ns.gmd}}}equivalentScale")
            equivalent_scale_element = SubElement(
                equivalent_scale_wrapper, f"{{{self.ns.gmd}}}MD_RepresentativeFraction"
            )
            denominator_element = SubElement(equivalent_scale_element, f"{{{self.ns.gmd}}}denominator")
            denominator_value = SubElement(denominator_element, f"{{{self.ns.gco}}}Integer")
            denominator_value.text = str(self.element_attributes["spatial_resolution"])


class TopicCategory(MetadataRecordElement):
    def make_config(self) -> str:
        _ = ""

        topic_category_value = self.record.xpath(
            f"{self.xpath}/gmd:MD_TopicCategoryCode/text()", namespaces=self.ns.nsmap()
        )
        if len(topic_category_value) == 1:
            _ = topic_category_value[0]

        return _

    def make_element(self) -> None:
        topic_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}topicCategory")
        topic_value = SubElement(topic_element, f"{{{self.ns.gmd}}}MD_TopicCategoryCode")
        topic_value.text = self.element_attributes["topic"]


class Extent(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        identifier_value = self.record.xpath(
            f"{self.xpath}/gmd:EX_Extent/@id",
            namespaces=self.ns.nsmap(),
        )
        if len(identifier_value) == 1:
            _["identifier"] = identifier_value[0]

        geographic_extent = GeographicExtent(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:EX_Extent",
        )
        _geographic_extent = geographic_extent.make_config()
        if bool(_geographic_extent):
            _["geographic"] = _geographic_extent

        temporal_extent = TemporalExtent(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:EX_Extent",
        )
        _temporal_extent = temporal_extent.make_config()
        if bool(_temporal_extent):
            _["temporal"] = _temporal_extent

        vertical_extent = VerticalExtent(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:EX_Extent/" f"gmd:verticalElement",
        )
        _vertical_extent = vertical_extent.make_config()
        if bool(_vertical_extent):
            _["vertical"] = _vertical_extent

        return _

    def make_element(self) -> None:
        extent_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}extent")
        extent_element = SubElement(
            extent_wrapper,
            f"{{{self.ns.gmd}}}EX_Extent",
            attrib={"id": self.element_attributes["extent"]["identifier"]},
        )

        for extent_item in self.element_attributes.values():
            if "geographic" in extent_item:
                geographic_extent = GeographicExtent(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=extent_element,
                    element_attributes=extent_item["geographic"],
                )
                geographic_extent.make_element()

            if "temporal" in extent_item:
                temporal_extent = TemporalExtent(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=extent_element,
                    element_attributes=extent_item["temporal"],
                )
                temporal_extent.make_element()

            if "vertical" in extent_item:
                vertical_extent = VerticalExtent(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=extent_element,
                    element_attributes=extent_item["vertical"],
                )
                vertical_extent.make_element()


class GeographicExtent(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        bounding_box = BoundingBox(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:geographicElement",
        )
        _bounding_box = bounding_box.make_config()
        if bool(_bounding_box):
            _["bounding_box"] = _bounding_box

        identifier = Identifier(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:geographicElement/gmd:EX_GeographicDescription/gmd:geographicIdentifier",
        )
        _identifier = identifier.make_config()
        if bool(_identifier):
            _["identifier"] = _identifier

        return _

    def make_element(self) -> None:
        geographic_extent_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}geographicElement")

        if "bounding_box" in self.element_attributes:
            bounding_box = BoundingBox(
                record=self.record,
                attributes=self.attributes,
                parent_element=geographic_extent_element,
                element_attributes=self.element_attributes["bounding_box"],
            )
            bounding_box.make_element()
        elif "identifier" in self.element_attributes:
            geographic_description_element = SubElement(
                geographic_extent_element, f"{{{self.ns.gmd}}}EX_GeographicDescription"
            )
            identifier = Identifier(
                record=self.record,
                attributes=self.attributes,
                parent_element=geographic_description_element,
                element_attributes=self.element_attributes["identifier"],
            )
            identifier.identifier_container = f"{{{self.ns.gmd}}}geographicIdentifier"
            identifier.make_element()


class BoundingBox(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        west_element_value = self.record.xpath(
            f"{self.xpath}/gmd:EX_GeographicBoundingBox/gmd:westBoundLongitude/gco:Decimal/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(west_element_value) == 1:
            _["west_longitude"] = float(west_element_value[0])

        east_element_value = self.record.xpath(
            f"{self.xpath}/gmd:EX_GeographicBoundingBox/gmd:eastBoundLongitude/gco:Decimal/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(east_element_value) == 1:
            _["east_longitude"] = float(east_element_value[0])

        south_element_value = self.record.xpath(
            f"{self.xpath}/gmd:EX_GeographicBoundingBox/gmd:southBoundLatitude/gco:Decimal/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(south_element_value) == 1:
            _["south_latitude"] = float(south_element_value[0])

        north_element_value = self.record.xpath(
            f"{self.xpath}/gmd:EX_GeographicBoundingBox/gmd:northBoundLatitude/gco:Decimal/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(north_element_value) == 1:
            _["north_latitude"] = float(north_element_value[0])

        return _

    def make_element(self) -> None:
        bounding_box_element = SubElement(
            self.parent_element,
            f"{{{self.ns.gmd}}}EX_GeographicBoundingBox",
        )

        west_element = SubElement(bounding_box_element, f"{{{self.ns.gmd}}}westBoundLongitude")
        west_value = SubElement(west_element, f"{{{self.ns.gco}}}Decimal")
        west_value.text = str(self.element_attributes["west_longitude"])

        east_element = SubElement(bounding_box_element, f"{{{self.ns.gmd}}}eastBoundLongitude")
        east_value = SubElement(east_element, f"{{{self.ns.gco}}}Decimal")
        east_value.text = str(self.element_attributes["east_longitude"])

        south_element = SubElement(bounding_box_element, f"{{{self.ns.gmd}}}southBoundLatitude")
        south_value = SubElement(south_element, f"{{{self.ns.gco}}}Decimal")
        south_value.text = str(self.element_attributes["south_latitude"])

        north_element = SubElement(bounding_box_element, f"{{{self.ns.gmd}}}northBoundLatitude")
        north_value = SubElement(north_element, f"{{{self.ns.gco}}}Decimal")
        north_value.text = str(self.element_attributes["north_latitude"])


class VerticalExtent(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        minimum_value = self.record.xpath(
            f"{self.xpath}/gmd:EX_VerticalExtent/gmd:minimumValue/gco:Real/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(minimum_value) == 1:
            _["minimum"] = float(minimum_value[0])

        maximum_value = self.record.xpath(
            f"{self.xpath}/gmd:EX_VerticalExtent/gmd:maximumValue/gco:Real/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(maximum_value) == 1:
            _["maximum"] = float(maximum_value[0])

        vertical_crs = VerticalCRS(
            record=self.record, attributes=self.attributes, xpath=f"{self.xpath}/gmd:EX_VerticalExtent"
        )
        _vertical_crs = vertical_crs.make_config()
        if bool(_vertical_crs):
            _ = {**_, **_vertical_crs}

        return _

    def make_element(self) -> None:
        vertical_extent_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}verticalElement")
        vertical_extent_element = SubElement(vertical_extent_wrapper, f"{{{self.ns.gmd}}}EX_VerticalExtent")

        if "minimum" in self.element_attributes:
            minimum_element = SubElement(vertical_extent_element, f"{{{self.ns.gmd}}}minimumValue")
            minimum_value = SubElement(minimum_element, f"{{{self.ns.gco}}}Real")
            minimum_value.text = str(self.element_attributes["minimum"])

        if "maximum" in self.element_attributes:
            maximum_element = SubElement(vertical_extent_element, f"{{{self.ns.gmd}}}maximumValue")
            maximum_value = SubElement(maximum_element, f"{{{self.ns.gco}}}Real")
            maximum_value.text = str(self.element_attributes["maximum"])

        if "code" in self.element_attributes:
            vertical_crs = VerticalCRS(
                record=self.record,
                attributes=self.attributes,
                parent_element=vertical_extent_element,
                element_attributes=self.element_attributes,
            )
            vertical_crs.make_element()


class VerticalCRS(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        identifier_value = self.record.xpath(
            f"{self.xpath}/gmd:verticalCRS/gml:VerticalCRS/@gml:id",
            namespaces=self.ns.nsmap(),
        )
        if len(identifier_value) == 1:
            _["identifier"] = identifier_value[0]

        code_value = self.record.xpath(
            f"{self.xpath}/gmd:verticalCRS/gml:VerticalCRS/gml:identifier/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(code_value) == 1:
            _["code"] = code_value[0]

        name_value = self.record.xpath(
            f"{self.xpath}/gmd:verticalCRS/gml:VerticalCRS/gml:name/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(name_value) == 1:
            _["name"] = name_value[0]

        remarks_value = self.record.xpath(
            f"{self.xpath}/gmd:verticalCRS/gml:VerticalCRS/gml:remarks/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(remarks_value) == 1:
            _["remarks"] = remarks_value[0]

        domain_of_validity_href = self.record.xpath(
            f"{self.xpath}/gmd:verticalCRS/gml:VerticalCRS/gml:domainOfValidity/@xlink:href",
            namespaces=self.ns.nsmap(),
        )
        if len(domain_of_validity_href) == 1:
            _["domain_of_validity"] = {"href": domain_of_validity_href[0]}

        scope_value = self.record.xpath(
            f"{self.xpath}/gmd:verticalCRS/gml:VerticalCRS/gml:scope/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(scope_value) == 1:
            _["scope"] = scope_value[0]

        vertical_cs_href = self.record.xpath(
            f"{self.xpath}/gmd:verticalCRS/gml:VerticalCRS/gml:verticalCS/@xlink:href",
            namespaces=self.ns.nsmap(),
        )
        if len(vertical_cs_href) == 1:
            _["vertical_cs"] = {"href": vertical_cs_href[0]}

        vertical_datum_href = self.record.xpath(
            f"{self.xpath}/gmd:verticalCRS/gml:VerticalCRS/gml:verticalDatum/@xlink:href",
            namespaces=self.ns.nsmap(),
        )
        if len(vertical_datum_href) == 1:
            _["vertical_datum"] = {"href": vertical_datum_href[0]}

        return _

    def make_element(self) -> None:
        vertical_crs_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}verticalCRS")
        vertical_crs_element = SubElement(
            vertical_crs_wrapper,
            f"{{{self.ns.gml}}}VerticalCRS",
            attrib={f"{{{self.ns.gml}}}id": self.element_attributes["identifier"]},
        )
        vertical_crs_code = SubElement(
            vertical_crs_element, f"{{{self.ns.gml}}}identifier", attrib={"codeSpace": "OGP"}
        )
        vertical_crs_code.text = self.element_attributes["code"]

        name = SubElement(vertical_crs_element, f"{{{self.ns.gml}}}name")
        name.text = self.element_attributes["name"]

        remarks = SubElement(vertical_crs_element, f"{{{self.ns.gml}}}remarks")
        remarks.text = self.element_attributes["remarks"]

        SubElement(
            vertical_crs_element,
            f"{{{self.ns.gml}}}domainOfValidity",
            attrib={f"{{{self.ns.xlink}}}href": self.element_attributes["domain_of_validity"]["href"]},
        )

        scope = SubElement(vertical_crs_element, f"{{{self.ns.gml}}}scope")
        scope.text = self.element_attributes["scope"]

        SubElement(
            vertical_crs_element,
            f"{{{self.ns.gml}}}verticalCS",
            attrib={f"{{{self.ns.xlink}}}href": self.element_attributes["vertical_cs"]["href"]},
        )

        SubElement(
            vertical_crs_element,
            f"{{{self.ns.gml}}}verticalDatum",
            attrib={f"{{{self.ns.xlink}}}href": self.element_attributes["vertical_datum"]["href"]},
        )


class TemporalExtent(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        begin_value = self.record.xpath(
            f"{self.xpath}/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:beginPosition/"
            f"text()",
            namespaces=self.ns.nsmap(),
        )
        if len(begin_value) == 1:
            if "period" not in _:
                _["period"] = {}
            try:
                _["period"]["start"] = decode_date_string(date_datetime=begin_value[0])
            except ValueError:
                msg = "Date/datetime could not be parsed as an ISO date value"
                raise RuntimeError(msg) from None

        end_value = self.record.xpath(
            f"{self.xpath}/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:endPosition/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(end_value) == 1:
            if "period" not in _:
                _["period"] = {}
            try:
                _["period"]["end"] = decode_date_string(date_datetime=end_value[0])
            except ValueError:
                msg = "Date/datetime could not be parsed as an ISO date value"
                raise RuntimeError(msg) from None

        return _

    def make_element(self) -> None:
        temporal_extent_container = SubElement(self.parent_element, f"{{{self.ns.gmd}}}temporalElement")
        temporal_extent_wrapper = SubElement(temporal_extent_container, f"{{{self.ns.gmd}}}EX_TemporalExtent")
        temporal_extent_element = SubElement(temporal_extent_wrapper, f"{{{self.ns.gmd}}}extent")

        if "period" in self.element_attributes:
            time_period_element = SubElement(
                temporal_extent_element,
                f"{{{self.ns.gml}}}TimePeriod",
            )

            _date_precision = None
            if "date_precision" in self.element_attributes["period"]["start"]:
                _date_precision = self.element_attributes["period"]["start"]["date_precision"]
            begin_position_element = SubElement(time_period_element, f"{{{self.ns.gml}}}beginPosition")
            begin_position_element.text = encode_date_string(
                date_datetime=self.element_attributes["period"]["start"]["date"],
                date_precision=_date_precision,
            )

            end_position_element = SubElement(time_period_element, f"{{{self.ns.gml}}}endPosition")
            if "end" in self.element_attributes["period"]:
                _date_precision = None
                if "date_precision" in self.element_attributes["period"]["end"]:
                    _date_precision = self.element_attributes["period"]["end"]["date_precision"]
                end_position_element.text = encode_date_string(
                    date_datetime=self.element_attributes["period"]["end"]["date"],
                    date_precision=_date_precision,
                )
            else:
                end_position_element.attrib["indeterminatePosition"] = "unknown"


class ResourceFormat(MetadataRecordElement):
    def make_config(self) -> dict:
        resource_format = Format(record=self.record, attributes=self.attributes, xpath=self.xpath)
        return resource_format.make_config()

    def make_element(self) -> None:
        resource_format_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}resourceFormat")

        resource_format = Format(
            record=self.record,
            attributes=self.attributes,
            parent_element=resource_format_element,
            element_attributes=self.element_attributes,
        )
        resource_format.make_element()
