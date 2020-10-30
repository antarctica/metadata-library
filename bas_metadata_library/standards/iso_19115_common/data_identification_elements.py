import requests

from copy import deepcopy
from datetime import datetime

# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# We don't currently allow untrusted/user-provided XML so this is not a risk
from lxml.etree import Element, SubElement  # nosec

from bas_metadata_library import MetadataRecord
from bas_metadata_library.standards.iso_19115_common import MetadataRecordElement, CodeListElement
from bas_metadata_library.standards.iso_19115_common.common_elements import (
    Citation,
    ResponsibleParty,
    MaintenanceInformation,
    AnchorElement,
    Language,
    CharacterSet,
)
from bas_metadata_library.standards.iso_19115_common.utils import format_date_string


class DataIdentification(MetadataRecordElement):
    def make_config(self) -> dict:
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

        resource_maintenance = ResourceMaintenance(
            record=self.record, attributes=self.attributes, xpath=f"{self.xpath}"
        )
        _resource_maintenance = resource_maintenance.make_config()
        if bool(_resource_maintenance):
            _["maintenance"] = _resource_maintenance

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

        _resource_constraints = {}
        constraints_length = int(
            self.record.xpath(
                f"count({self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints)",
                namespaces=self.ns.nsmap(),
            )
        )
        for constraint_index in range(1, constraints_length + 1):
            constraint = ResourceConstraints(
                record=self.record,
                attributes=self.attributes,
                xpath=f"({self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints)"
                f"[{constraint_index}]",
            )
            _constraint = constraint.make_config()
            if bool(_constraint):
                if "access" in _constraint.keys():
                    if "access" not in _resource_constraints.keys():
                        _resource_constraints["access"] = []
                    _resource_constraints["access"].append(_constraint["access"])
                elif "usage" in _constraint.keys():
                    if "usage" not in _resource_constraints.keys():
                        _resource_constraints["usage"] = []
                    _resource_constraints["usage"].append(_constraint["usage"])
        if len(_resource_constraints) > 0:
            _["constraints"] = _resource_constraints

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
        if _spatial_resolution != "":  # pragma: no cover
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
        if _character_set != "":  # pragma: no cover
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

        extent = Extent(record=self.record, attributes=self.attributes, xpath=f"{self.xpath}")
        _extent = extent.make_config()
        if bool(_extent):
            _["extent"] = _extent

        supplemental_information = SupplementalInformation(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:supplementalInformation",
        )
        _supplemental_information = supplemental_information.make_config()
        if _supplemental_information != "":
            _["supplemental_information"] = _supplemental_information

        return _

    def make_element(self):
        data_identification_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}identificationInfo")
        data_identification_element = SubElement(data_identification_wrapper, f"{{{self.ns.gmd}}}MD_DataIdentification")

        citation_wrapper = SubElement(data_identification_element, f"{{{self.ns.gmd}}}citation")
        citation = Citation(
            record=self.record,
            attributes=self.attributes,
            parent_element=citation_wrapper,
            element_attributes=self.element_attributes["resource"],
        )
        citation.make_element()

        abstract = Abstract(
            record=self.record,
            attributes=self.attributes,
            parent_element=data_identification_element,
            element_attributes=self.attributes["resource"],
        )
        abstract.make_element()

        if "contacts" in self.attributes["resource"]:
            for point_of_contact_attributes in self.attributes["resource"]["contacts"]:
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

        if "maintenance" in self.attributes["resource"]:
            resource_maintenance = ResourceMaintenance(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=self.element_attributes["resource"]["maintenance"],
            )
            resource_maintenance.make_element()

        if "keywords" in self.attributes["resource"]:
            for keyword_attributes in self.attributes["resource"]["keywords"]:
                descriptive_keywords = DescriptiveKeywords(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=data_identification_element,
                    element_attributes=keyword_attributes,
                )
                descriptive_keywords.make_element()

        if "constraints" in self.attributes["resource"]:
            constraints = ResourceConstraints(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=self.attributes["resource"]["constraints"],
            )
            constraints.make_element()

        if "spatial_representation_type" in self.attributes["resource"]:
            spatial_representation_type = SpatialRepresentationType(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=self.attributes["resource"],
            )
            spatial_representation_type.make_element()

        if "spatial_resolution" in self.attributes["resource"]:  # pragma: no cover
            spatial_resolution = SpatialResolution(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=self.attributes["resource"],
            )
            spatial_resolution.make_element()

        character_set = CharacterSet(
            record=self.record,
            attributes=self.attributes,
            parent_element=data_identification_element,
            element_attributes=self.attributes["resource"],
        )
        character_set.make_element()

        language = Language(
            record=self.record,
            attributes=self.attributes,
            parent_element=data_identification_element,
            element_attributes=self.attributes["resource"],
        )
        language.make_element()

        if "topics" in self.attributes["resource"]:
            for topic_attribute in self.attributes["resource"]["topics"]:
                topic = TopicCategory(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=data_identification_element,
                    element_attributes={"topic": topic_attribute},
                )
                topic.make_element()

        if "extent" in self.attributes["resource"]:
            extent = Extent(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=self.attributes["resource"]["extent"],
            )
            extent.make_element()

        if "supplemental_information" in self.attributes["resource"]:
            supplemental_information = SupplementalInformation(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=self.attributes["resource"],
            )
            supplemental_information.make_element()


class Abstract(MetadataRecordElement):
    def make_config(self) -> str:
        _ = ""

        abstract_value = self.record.xpath(f"{self.xpath}/gco:CharacterString/text()", namespaces=self.ns.nsmap())
        if len(abstract_value) == 1:
            _ = abstract_value[0]

        return _

    def make_element(self):
        abstract_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}abstract")
        abstract_value = SubElement(abstract_element, f"{{{self.ns.gco}}}CharacterString")
        abstract_value.text = self.element_attributes["abstract"]


class PointOfContact(MetadataRecordElement):
    def make_config(self) -> dict:
        responsible_party = ResponsibleParty(record=self.record, attributes=self.attributes, xpath=self.xpath)
        _responsible_party = responsible_party.make_config()

        return _responsible_party

    def make_element(self):
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

    def make_element(self):
        resource_maintenance_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}resourceMaintenance")
        maintenance_information = MaintenanceInformation(
            record=self.record,
            attributes=self.attributes,
            parent_element=resource_maintenance_element,
            element_attributes=self.element_attributes,
        )
        maintenance_information.make_element()


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

    def make_element(self):
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
        element_attributes: dict = None,
        xpath: str = None,
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
        _citation = citation.make_config()

        return _citation

    def make_element(self):
        thesaurus_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}thesaurusName")

        citation = Citation(
            record=self.record,
            attributes=self.attributes,
            parent_element=thesaurus_element,
            element_attributes=self.element_attributes,
        )
        citation.make_element()


class ResourceConstraints(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        _id = self.record.xpath(f"{self.xpath}/gmd:MD_LegalConstraints/@id", namespaces=self.ns.nsmap())
        if len(_id) == 1:
            _id = _id[0]

        access_constraint = AccessConstraint(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:MD_LegalConstraints/gmd:accessConstraints",
        )
        _access_constraint = access_constraint.make_config()
        if _access_constraint != "":
            _["access"] = {"restriction_code": _access_constraint}

            other_constraint = OtherConstraints(
                record=self.record, attributes=self.attributes, xpath=f"{self.xpath}/gmd:MD_LegalConstraints"
            )
            _other_constraint = other_constraint.make_config()
            if _other_constraint != "":
                _["access"]["statement"] = _other_constraint

        use_constraint = UseLimitation(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:MD_LegalConstraints/gmd:useLimitation",
        )
        _usage_constraint = use_constraint.make_config()
        if bool(_usage_constraint):
            _["usage"] = _usage_constraint

            if _id == "copyright":
                _["usage"] = {"copyright_licence": _usage_constraint}
                if (
                    "href" in _usage_constraint
                    and _usage_constraint["href"]
                    == "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/"
                ):
                    # noinspection PyUnresolvedReferences
                    _["usage"]["copyright_licence"]["code"] = "OGL-UK-3.0"
            elif _id == "citation":
                _["usage"] = {"required_citation": _usage_constraint}

        if _id == "InspireLimitationsOnPublicAccess":
            limitations_on_access = self.record.xpath(
                f"{self.xpath}/gmd:MD_LegalConstraints/gmd:otherConstraints/gmx:Anchor/text()",
                namespaces=self.ns.nsmap(),
            )
            if len(limitations_on_access) == 1:
                if "access" in _.keys():
                    _["access"]["inspire_limitations_on_public_access"] = limitations_on_access[0]

        return _

    def make_element(self):
        if "access" in self.element_attributes:
            for access_constraint_attributes in self.element_attributes["access"]:
                constraints_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}resourceConstraints")
                constraints_element = SubElement(constraints_wrapper, f"{{{self.ns.gmd}}}MD_LegalConstraints")

                access_constraint = AccessConstraint(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=constraints_element,
                    element_attributes=access_constraint_attributes,
                )
                access_constraint.make_element()

                if "statement" in access_constraint_attributes:
                    element_attributes = {"value": deepcopy(access_constraint_attributes["statement"])}

                    other_constraint = OtherConstraints(
                        record=self.record,
                        attributes=self.attributes,
                        parent_element=constraints_element,
                        element_attributes=element_attributes,
                    )
                    other_constraint.make_element()

                if "inspire_limitations_on_public_access" in access_constraint_attributes:
                    constraints_element.set("id", "InspireLimitationsOnPublicAccess")

                    public_access_limitation = InspireLimitationsOnPublicAccess(
                        record=self.record,
                        attributes=self.attributes,
                        parent_element=constraints_element,
                        element_attributes=access_constraint_attributes,
                    )
                    public_access_limitation.make_element()

        if "usage" in self.element_attributes:
            for usage_constraint_attributes in self.element_attributes["usage"]:
                constraints_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}resourceConstraints")
                constraints_element = SubElement(constraints_wrapper, f"{{{self.ns.gmd}}}MD_LegalConstraints")

                if "statement" in usage_constraint_attributes:
                    element_attributes = {"value": deepcopy(usage_constraint_attributes["statement"])}

                    use_limitation = UseLimitation(
                        record=self.record,
                        attributes=self.attributes,
                        parent_element=constraints_element,
                        element_attributes=element_attributes,
                    )
                    use_limitation.make_element()

                if "copyright_licence" in usage_constraint_attributes:
                    constraints_element.set("id", "copyright")

                    element_attributes = deepcopy(usage_constraint_attributes["copyright_licence"])
                    element_attributes["value"] = element_attributes["statement"]

                    use_limitation = UseLimitation(
                        record=self.record,
                        attributes=self.attributes,
                        parent_element=constraints_element,
                        element_attributes=element_attributes,
                    )
                    use_limitation.make_element()

                if "required_citation" in usage_constraint_attributes:
                    constraints_element.set("id", "citation")

                    element_attributes = {}
                    if "statement" in usage_constraint_attributes["required_citation"]:
                        element_attributes["value"] = usage_constraint_attributes["required_citation"]["statement"]
                    elif "doi" in usage_constraint_attributes["required_citation"]:
                        citation = self._get_doi_citation(doi=usage_constraint_attributes["required_citation"]["doi"])
                        element_attributes["value"] = f'Cite this information as "{citation}"'

                    use_limitation = UseLimitation(
                        record=self.record,
                        attributes=self.attributes,
                        parent_element=constraints_element,
                        element_attributes=element_attributes,
                    )
                    use_limitation.make_element()

    @staticmethod
    def _get_doi_citation(doi: str) -> str:
        """
        Get citation for a DOI using crosscite.org

        This is a standalone method to allow for mocking during tests.

        @:type doi: str
        @:param doi: DOI to get citation for

        @:rtype: str
        @:return APA style citation for DOI
        """
        citation_response = requests.get(doi, headers={"Accept": "text/x-bibliography; style=apa; locale=en-GB"})
        citation_response.raise_for_status()
        return citation_response.text


class AccessConstraint(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None,
        xpath: str = None,
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes,
            xpath=f"{xpath}/gmd:MD_RestrictionCode",
        )
        self.code_list_values = [
            "copyright",
            "patent",
            "patentPending",
            "trademark",
            "license",
            "intellectualPropertyRights",
            "restricted",
            "otherRestrictions",
        ]
        self.code_list = (
            "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/"
            "codelist/gmxCodelists.xml#MD_RestrictionCode"
        )
        self.element = f"{{{self.ns.gmd}}}accessConstraints"
        self.element_code = f"{{{self.ns.gmd}}}MD_RestrictionCode"
        self.attribute = "restriction_code"


class InspireLimitationsOnPublicAccess(MetadataRecordElement):
    def make_element(self):
        other_constraints_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}otherConstraints")

        other_constraints_value = AnchorElement(
            record=self.record,
            attributes=self.attributes,
            parent_element=other_constraints_element,
            element_attributes={
                "href": f"http://inspire.ec.europa.eu/metadata-codelist/LimitationsOnPublicAccess/"
                f"{self.element_attributes['inspire_limitations_on_public_access']}"
            },
            element_value=self.element_attributes["inspire_limitations_on_public_access"],
        )
        other_constraints_value.make_element()


class OtherConstraints(MetadataRecordElement):
    def make_config(self) -> str:
        _ = ""

        other_constraint = self.record.xpath(
            f"{self.xpath}/gmd:otherConstraints/gco:CharacterString/text()", namespaces=self.ns.nsmap()
        )
        if len(other_constraint) == 1:
            _ = other_constraint[0]

        return _

    def make_element(self):
        other_constraints_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}otherConstraints")
        other_constraints_value = SubElement(other_constraints_element, f"{{{self.ns.gco}}}CharacterString")
        other_constraints_value.text = self.element_attributes["value"]


class UseLimitation(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        use_constraint_statement = self.record.xpath(
            f"{self.xpath}/gco:CharacterString/text() | {self.xpath}/gmx:Anchor/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(use_constraint_statement) == 1:
            _["statement"] = use_constraint_statement[0]

        use_constraint_href = self.record.xpath(f"{self.xpath}/gmx:Anchor/@xlink:href", namespaces=self.ns.nsmap())
        if len(use_constraint_href) == 1:
            _["href"] = use_constraint_href[0]

        return _

    def make_element(self):
        use_limitation_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}useLimitation")

        if "href" in self.element_attributes:
            use_limitation_value = AnchorElement(
                record=self.record,
                attributes=self.attributes,
                parent_element=use_limitation_element,
                element_attributes=self.element_attributes,
                element_value=self.element_attributes["value"],
            )
            use_limitation_value.make_element()
        else:
            use_limitation_value = SubElement(use_limitation_element, f"{{{self.ns.gco}}}CharacterString")
            use_limitation_value.text = self.element_attributes["value"]


class SupplementalInformation(MetadataRecordElement):
    def make_config(self) -> str:
        _ = ""

        supplemental_value = self.record.xpath(f"{self.xpath}/gco:CharacterString/text()", namespaces=self.ns.nsmap())
        if len(supplemental_value) == 1:
            _ = supplemental_value[0]

        return _

    def make_element(self):
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
        element_attributes: dict = None,
        xpath: str = None,
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


class SpatialResolution(MetadataRecordElement):  # pragma: no cover
    def make_config(self) -> str:
        _ = ""

        spatial_resolution_value = self.record.xpath(
            f"{self.xpath}/gmd:MD_Resolution/gco:Distance/text()", namespaces=self.ns.nsmap()
        )
        if len(spatial_resolution_value) == 1:
            _ = spatial_resolution_value[0]

        return _

    def make_element(self):
        resolution_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}spatialResolution")
        resolution_element = SubElement(resolution_wrapper, f"{{{self.ns.gmd}}}MD_Resolution")

        if self.element_attributes["spatial_resolution"] is None:
            SubElement(
                resolution_element, f"{{{self.ns.gco}}}Distance", attrib={f"{{{self.ns.gco}}}nilReason": "inapplicable"}
            )


class TopicCategory(MetadataRecordElement):
    def make_config(self) -> str:
        _ = ""

        topic_category_value = self.record.xpath(
            f"{self.xpath}/gmd:MD_TopicCategoryCode/text()", namespaces=self.ns.nsmap()
        )
        if len(topic_category_value) == 1:
            _ = topic_category_value[0]

        return _

    def make_element(self):
        topic_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}topicCategory")
        topic_value = SubElement(topic_element, f"{{{self.ns.gmd}}}MD_TopicCategoryCode")
        topic_value.text = self.element_attributes["topic"]


class Extent(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        geographic_extent = GeographicExtent(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent",
        )
        _geographic_extent = geographic_extent.make_config()
        if bool(_geographic_extent):
            _["geographic"] = _geographic_extent

        temporal_extent = TemporalExtent(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent",
        )
        _temporal_extent = temporal_extent.make_config()
        if bool(_temporal_extent):
            _["temporal"] = _temporal_extent

        vertical_extent = VerticalExtent(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/"
            f"gmd:verticalElement",
        )
        _vertical_extent = vertical_extent.make_config()
        if bool(_vertical_extent):
            _["vertical"] = _vertical_extent

        return _

    def make_element(self):
        extent_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}extent")
        extent_element = SubElement(extent_wrapper, f"{{{self.ns.gmd}}}EX_Extent")

        if "geographic" in self.element_attributes:
            geographic_extent = GeographicExtent(
                record=self.record,
                attributes=self.attributes,
                parent_element=extent_element,
                element_attributes=self.element_attributes["geographic"],
            )
            geographic_extent.make_element()

        if "temporal" in self.element_attributes:
            temporal_extent = TemporalExtent(
                record=self.record,
                attributes=self.attributes,
                parent_element=extent_element,
                element_attributes=self.element_attributes["temporal"],
            )
            temporal_extent.make_element()

        if "vertical" in self.element_attributes:
            vertical_extent = VerticalExtent(
                record=self.record,
                attributes=self.attributes,
                parent_element=extent_element,
                element_attributes=self.element_attributes["vertical"],
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

        return _

    def make_element(self):
        geographic_extent_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}geographicElement")

        if "bounding_box" in self.element_attributes:
            bounding_box = BoundingBox(
                record=self.record,
                attributes=self.attributes,
                parent_element=geographic_extent_element,
                element_attributes=self.element_attributes["bounding_box"],
            )
            bounding_box.make_element()


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

    def make_element(self):
        bounding_box_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}EX_GeographicBoundingBox")

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

    def make_element(self):
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

    def make_element(self):
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
            if "period" not in _.keys():
                _["period"] = {}
            try:
                _["period"]["start"] = datetime.fromisoformat(begin_value[0])
            except ValueError:  # pragma: no cover
                raise RuntimeError("date time could not be parsed as an ISO datetime value")

        end_value = self.record.xpath(
            f"{self.xpath}/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:endPosition/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(end_value) == 1:
            if "period" not in _.keys():  # pragma: no cover
                _["period"] = {}
            try:
                _["period"]["end"] = datetime.fromisoformat(end_value[0])
            except ValueError:  # pragma: no cover
                raise RuntimeError("date time could not be parsed as an ISO datetime value")

        return _

    def make_element(self):
        temporal_extent_container = SubElement(self.parent_element, f"{{{self.ns.gmd}}}temporalElement")
        temporal_extent_wrapper = SubElement(temporal_extent_container, f"{{{self.ns.gmd}}}EX_TemporalExtent")
        temporal_extent_element = SubElement(temporal_extent_wrapper, f"{{{self.ns.gmd}}}extent")

        if "period" in self.element_attributes:
            time_period_element = SubElement(
                temporal_extent_element,
                f"{{{self.ns.gml}}}TimePeriod",
                attrib={f"{{{self.ns.gml}}}id": "boundingExtent"},
            )
            begin_position_element = SubElement(time_period_element, f"{{{self.ns.gml}}}beginPosition")
            begin_position_element.text = format_date_string(self.element_attributes["period"]["start"])

            end_position_element = SubElement(time_period_element, f"{{{self.ns.gml}}}endPosition")
            end_position_element.text = format_date_string(self.element_attributes["period"]["end"])
