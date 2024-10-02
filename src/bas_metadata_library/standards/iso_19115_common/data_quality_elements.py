from lxml.etree import SubElement

from bas_metadata_library.standards.iso_19115_common import MetadataRecordElement
from bas_metadata_library.standards.iso_19115_common.base_elements import ScopeCode
from bas_metadata_library.standards.iso_19115_common.common_elements import Citation, ResponsibleParty
from bas_metadata_library.standards.iso_19115_common.utils import (
    condense_contacts_roles,
    decode_date_string,
    encode_date_string,
)


class DataQuality(MetadataRecordElement):
    """gmd:dataQualityInfo."""

    def make_config(self) -> dict:
        """Decode to Python."""
        _ = {}

        _domain_consistency = []
        domains_length = int(
            self.record.xpath(
                f"count({self.xpath}/gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:report/gmd:DQ_DomainConsistency)",
                namespaces=self.ns.nsmap(),
            )
        )
        for domain_index in range(1, domains_length + 1):
            domain_consistency = DomainConsistency(
                record=self.record,
                attributes=self.attributes,
                xpath=f"({self.xpath}/gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:report[gmd:DQ_DomainConsistency])[{domain_index}]",
            )
            _domain = domain_consistency.make_config()
            if bool(_domain):
                _domain_consistency.append(_domain)
        if len(_domain_consistency) > 0:
            _["domain_consistency"] = _domain_consistency

        lineage = Lineage(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage",
        )
        _lineage = lineage.make_config()
        if bool(_lineage):
            _["lineage"] = _lineage

        return _

    def make_element(self) -> None:
        """Encode as XML."""
        data_quality_wrapper = SubElement(self.record, f"{{{self.ns.gmd}}}dataQualityInfo")
        data_quality_element = SubElement(data_quality_wrapper, f"{{{self.ns.gmd}}}DQ_DataQuality")

        scope = Scope(record=self.record, attributes=self.attributes, parent_element=data_quality_element)
        scope.make_element()

        if "domain_consistency" in self.element_attributes["identification"]:
            for domain_consistency_attributes in self.element_attributes["identification"]["domain_consistency"]:
                domain_consistency = DomainConsistency(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=data_quality_element,
                    element_attributes=domain_consistency_attributes,
                )
                domain_consistency.make_element()

        if "lineage" in self.element_attributes["identification"]:
            lineage = Lineage(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_quality_element,
                element_attributes=self.element_attributes["identification"]["lineage"],
            )
            lineage.make_element()


class Scope(MetadataRecordElement):
    """gmd:scope."""

    def make_element(self) -> None:
        """Encode as XML."""
        scope_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}scope")
        scope_element = SubElement(scope_wrapper, f"{{{self.ns.gmd}}}DQ_Scope")

        scope_code = ScopeCode(record=self.record, attributes=self.attributes, parent_element=scope_element)
        scope_code.make_element()


class Lineage(MetadataRecordElement):
    """gmd:lineage."""

    def make_config(self) -> dict[str, str]:
        """Decode to Python."""
        _ = {}

        statement_value = self.record.xpath(
            f"{self.xpath}/gmd:LI_Lineage/gmd:statement/gco:CharacterString/text()", namespaces=self.ns.nsmap()
        )
        if len(statement_value) == 1:
            _["statement"] = statement_value[0]

        _process_steps = []
        steps_length = int(
            self.record.xpath(f"count({self.xpath}/gmd:LI_Lineage/gmd:processStep)", namespaces=self.ns.nsmap())
        )
        for step_index in range(1, steps_length + 1):
            process_step = ProcessStep(
                record=self.record,
                attributes=self.attributes,
                xpath=f"({self.xpath}/gmd:LI_Lineage/gmd:processStep)[{step_index}]",
            )
            _process_step = process_step.make_config()
            if bool(_process_step):
                _process_steps.append(_process_step)
        if len(_process_steps) > 0:
            _["process_steps"] = _process_steps

        _sources = []
        sources_length = int(
            self.record.xpath(f"count({self.xpath}/gmd:LI_Lineage/gmd:source)", namespaces=self.ns.nsmap())
        )
        for source_index in range(1, sources_length + 1):
            source = Source(
                record=self.record,
                attributes=self.attributes,
                xpath=f"({self.xpath}/gmd:LI_Lineage/gmd:source)[{source_index}]",
            )
            _source = source.make_config()
            if bool(_source):
                _sources.append(_source)
        if len(_sources) > 0:
            _["sources"] = _sources

        return _

    def make_element(self) -> None:
        """Encode as XML."""
        lineage_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}lineage")
        lineage_element = SubElement(lineage_wrapper, f"{{{self.ns.gmd}}}LI_Lineage")

        if "statement" in self.element_attributes:
            statement_element = SubElement(lineage_element, f"{{{self.ns.gmd}}}statement")
            statement_value = SubElement(statement_element, f"{{{self.ns.gco}}}CharacterString")
            statement_value.text = self.element_attributes["statement"]

        if "process_steps" in self.element_attributes:
            for process_step_attributes in self.element_attributes["process_steps"]:
                process_step_wrapper = SubElement(lineage_element, f"{{{self.ns.gmd}}}processStep")

                process_step = ProcessStep(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=process_step_wrapper,
                    element_attributes=process_step_attributes,
                )
                process_step.make_element()

        if "sources" in self.element_attributes:
            for source_attributes in self.element_attributes["sources"]:
                source_wrapper = SubElement(lineage_element, f"{{{self.ns.gmd}}}source")

                source = Source(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=source_wrapper,
                    element_attributes=source_attributes,
                )
                source.make_element()


class ProcessStep(MetadataRecordElement):
    """gmd:LI_ProcessStep."""

    def make_config(self) -> dict[str, str]:
        """Decode to Python."""
        _ = {}

        description_value = self.record.xpath(
            f"{self.xpath}/gmd:LI_ProcessStep/gmd:description/gco:CharacterString/text()", namespaces=self.ns.nsmap()
        )
        if len(description_value) == 1:
            _["description"] = description_value[0]

        rationale_value = self.record.xpath(
            f"{self.xpath}/gmd:LI_ProcessStep/gmd:rationale/gco:CharacterString/text()", namespaces=self.ns.nsmap()
        )
        if len(rationale_value) == 1:
            _["rationale"] = rationale_value[0]

        date_value = self.record.xpath(
            f"{self.xpath}/gmd:LI_ProcessStep/gmd:dateTime/gco:DateTime/text()", namespaces=self.ns.nsmap()
        )
        if len(date_value) == 1:
            _["date"] = decode_date_string(date_datetime=date_value[0])["date"]  # unwrap datetime value

        _processors = []
        processors_length = int(
            self.record.xpath(f"count({self.xpath}/gmd:LI_ProcessStep/gmd:processor)", namespaces=self.ns.nsmap())
        )
        for processor_index in range(1, processors_length + 1):
            processor = Processor(
                record=self.record,
                attributes=self.attributes,
                xpath=f"({self.xpath}/gmd:LI_ProcessStep/gmd:processor)[{processor_index}]",
            )
            _processor = processor.make_config()
            if bool(_processor):
                _processors.append(_processor)
        if len(_processors) > 0:
            _processors = condense_contacts_roles(contacts=_processors)
            _["processors"] = _processors

        _sources = []
        sources_length = int(
            self.record.xpath(f"count({self.xpath}/gmd:LI_ProcessStep/gmd:source)", namespaces=self.ns.nsmap())
        )
        for source_index in range(1, sources_length + 1):
            source = Source(
                record=self.record,
                attributes=self.attributes,
                xpath=f"({self.xpath}/gmd:LI_ProcessStep/gmd:source)[{source_index}]",
            )
            _source = source.make_config()
            if bool(_source):
                _sources.append(_source)
        if len(_sources) > 0:
            _["sources"] = _sources

        return _

    def make_element(self) -> None:
        """Encode as XML."""
        process_step_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}LI_ProcessStep")

        description_element = SubElement(process_step_element, f"{{{self.ns.gmd}}}description")
        description_value = SubElement(description_element, f"{{{self.ns.gco}}}CharacterString")
        description_value.text = self.element_attributes["description"]

        if "rationale" in self.element_attributes:
            rational_element = SubElement(process_step_element, f"{{{self.ns.gmd}}}rationale")
            rational_value = SubElement(rational_element, f"{{{self.ns.gco}}}CharacterString")
            rational_value.text = self.element_attributes["rationale"]

        if "date" in self.element_attributes:
            date_element = SubElement(process_step_element, f"{{{self.ns.gmd}}}dateTime")
            date_value = SubElement(date_element, f"{{{self.ns.gco}}}DateTime")
            date_value.text = encode_date_string(self.element_attributes["date"])

        if "processors" in self.element_attributes:
            for processor_attributes in self.element_attributes["processors"]:
                for role in processor_attributes["role"]:
                    _processor_attributes = processor_attributes.copy()
                    _processor_attributes["role"] = role

                    processor = Processor(
                        record=self.record,
                        attributes=self.attributes,
                        parent_element=process_step_element,
                        element_attributes=_processor_attributes,
                    )
                    processor.make_element()

        if "sources" in self.element_attributes:
            for source_attributes in self.element_attributes["sources"]:
                source_wrapper = SubElement(process_step_element, f"{{{self.ns.gmd}}}source")

                source = Source(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=source_wrapper,
                    element_attributes=source_attributes,
                )
                source.make_element()


class Processor(MetadataRecordElement):
    """gmd:processor."""

    def make_config(self) -> dict:
        """Decode to Python."""
        responsible_party = ResponsibleParty(record=self.record, attributes=self.attributes, xpath=self.xpath)
        return responsible_party.make_config()

    def make_element(self) -> None:
        """Encode as XML."""
        processor_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}processor")

        responsible_party = ResponsibleParty(
            record=self.record,
            attributes=self.attributes,
            parent_element=processor_element,
            element_attributes=self.element_attributes,
        )
        responsible_party.make_element()


class Source(MetadataRecordElement):
    """gmd:source."""

    def make_config(self) -> dict:
        """Decode to Python."""
        _ = {}

        description_value = self.record.xpath(
            f"{self.xpath}/gmd:LI_Source/gmd:description/gco:CharacterString/text()", namespaces=self.ns.nsmap()
        )
        if len(description_value) == 1:
            _["description"] = description_value[0]

        citation = Citation(
            record=self.record, attributes=self.attributes, xpath=f"({self.xpath}/gmd:LI_Source/gmd:sourceCitation)"
        )
        _citation = citation.make_config()
        if bool(_citation):
            _.update(**_citation)

        _source_steps = []
        steps_length = int(
            self.record.xpath(f"count({self.xpath}/gmd:LI_Source/gmd:sourceStep)", namespaces=self.ns.nsmap())
        )
        for step_index in range(1, steps_length + 1):
            source_step = ProcessStep(
                record=self.record,
                attributes=self.attributes,
                xpath=f"({self.xpath}/gmd:LI_Source/gmd:sourceStep)[{step_index}]",
            )
            _source_step = source_step.make_config()
            if bool(_source_step):
                _source_steps.append(_source_step)
        if len(_source_steps) > 0:
            _["source_steps"] = _source_steps

        return _

    def make_element(self) -> None:
        """Encode to XML."""
        source_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}LI_Source")

        if "description" in self.element_attributes:
            description_element = SubElement(source_element, f"{{{self.ns.gmd}}}description")
            description_value = SubElement(description_element, f"{{{self.ns.gco}}}CharacterString")
            description_value.text = self.element_attributes["description"]

        # partial citation attributes
        if any(key in ["title", "dates", "edition", "identifiers", "contact"] for key in self.element_attributes):
            citation_element = SubElement(source_element, f"{{{self.ns.gmd}}}sourceCitation")
            citation = Citation(
                record=self.record,
                attributes=self.attributes,
                parent_element=citation_element,
                element_attributes=self.element_attributes,
            )
            citation.make_element()

        if "source_steps" in self.element_attributes:
            for step_attributes in self.element_attributes["source_steps"]:
                source_step_wrapper = SubElement(source_element, f"{{{self.ns.gmd}}}sourceStep")

                step = ProcessStep(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=source_step_wrapper,
                    element_attributes=step_attributes,
                )
                step.make_element()


class DomainConsistency(MetadataRecordElement):
    """gmd:DQ_DomainConsistency."""

    def make_config(self) -> dict:
        """Decode to Python."""
        _ = {}
        xpath = f"{self.xpath}/gmd:DQ_DomainConsistency/gmd:result/gmd:DQ_ConformanceResult"

        specification = Citation(record=self.record, attributes=self.attributes, xpath=f"({xpath}/gmd:specification)")
        _specification = specification.make_config()
        if bool(_specification):
            _["specification"] = _specification

        explanation_value = self.record.xpath(
            f"{xpath}/gmd:explanation/gco:CharacterString/text()", namespaces=self.ns.nsmap()
        )
        if len(explanation_value) == 1:
            _["explanation"] = explanation_value[0]

        result_value = self.record.xpath(f"{xpath}/gmd:pass/gco:Boolean/text()", namespaces=self.ns.nsmap())
        if len(result_value) == 1:
            _["result"] = bool(result_value[0])

        return _

    def make_element(self) -> None:
        """Encode as XML."""
        domain_conformance_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}report")
        domain_conformance_element = SubElement(domain_conformance_wrapper, f"{{{self.ns.gmd}}}DQ_DomainConsistency")
        result_wrapper = SubElement(domain_conformance_element, f"{{{self.ns.gmd}}}result")
        result_element = SubElement(result_wrapper, f"{{{self.ns.gmd}}}DQ_ConformanceResult")

        specification_element = SubElement(result_element, f"{{{self.ns.gmd}}}specification")
        citation = Citation(
            record=self.record,
            attributes=self.attributes,
            parent_element=specification_element,
            element_attributes=self.element_attributes["specification"],
        )
        citation.make_element()

        explanation_element = SubElement(result_element, f"{{{self.ns.gmd}}}explanation")
        explanation_value = SubElement(explanation_element, f"{{{self.ns.gco}}}CharacterString")
        explanation_value.text = self.element_attributes["explanation"]

        pass_element = SubElement(result_element, f"{{{self.ns.gmd}}}pass")
        pass_value = SubElement(pass_element, f"{{{self.ns.gco}}}Boolean")
        pass_value.text = str(self.element_attributes["result"]).lower()
