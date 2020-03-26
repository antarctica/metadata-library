# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# We don't currently allow untrusted/user-provided XML so this is not a risk
from lxml.etree import SubElement  # nosec

from bas_metadata_library.standards.iso_19115_common import MetadataRecordElement
from bas_metadata_library.standards.iso_19115_common.common_elements import Citation
from bas_metadata_library.standards.iso_19115_common.base_elements import ScopeCode


class DataQuality(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        report = Report(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:report/",
        )
        _report = report.make_config()
        if bool(_report):
            _["measures"] = [_report]

        lineage = Lineage(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage",
        )
        _lineage = lineage.make_config()
        if _lineage != "":
            _["lineage"] = _lineage

        return _

    def make_element(self):
        data_quality_wrapper = SubElement(self.record, f"{{{self.ns.gmd}}}dataQualityInfo")
        data_quality_element = SubElement(data_quality_wrapper, f"{{{self.ns.gmd}}}DQ_DataQuality")

        scope = Scope(record=self.record, attributes=self.attributes, parent_element=data_quality_element)
        scope.make_element()

        if "measures" in self.attributes["resource"]:
            for measure_attributes in self.attributes["resource"]["measures"]:
                report = Report(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=data_quality_element,
                    element_attributes=measure_attributes,
                )
                report.make_element()

        lineage = Lineage(
            record=self.record,
            attributes=self.attributes,
            parent_element=data_quality_element,
            element_attributes=self.attributes["resource"],
        )
        lineage.make_element()


class Scope(MetadataRecordElement):
    def make_element(self):
        scope_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}scope")
        scope_element = SubElement(scope_wrapper, f"{{{self.ns.gmd}}}DQ_Scope")

        scope_code = ScopeCode(record=self.record, attributes=self.attributes, parent_element=scope_element)
        scope_code.make_element()


class Report(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        report_code = self.record.xpath(
            f"{self.xpath}/gmd:DQ_DomainConsistency/gmd:measureIdentification/gmd:RS_Identifier/gmd:code/"
            f"gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(report_code) == 1:
            _["code"] = report_code[0]

        report_code_space = self.record.xpath(
            f"{self.xpath}/gmd:DQ_DomainConsistency/gmd:measureIdentification/gmd:RS_Identifier/gmd:codeSpace/"
            f"gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(report_code_space) == 1:
            _["code_space"] = report_code_space[0]

        specification = Citation(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:DQ_DomainConsistency/gmd:result/gmd:DQ_ConformanceResult/gmd:specification",
        )
        _specification = specification.make_config()
        if bool(_specification):
            _ = {**_, **_specification}

        report_explanation = self.record.xpath(
            f"{self.xpath}/gmd:DQ_DomainConsistency/gmd:result/gmd:DQ_ConformanceResult/gmd:explanation/"
            f"gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(report_explanation) == 1:
            _["explanation"] = report_explanation[0]

        report_result = self.record.xpath(
            f"{self.xpath}/gmd:DQ_DomainConsistency/gmd:result/gmd:DQ_ConformanceResult/gmd:pass/gco:Boolean/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(report_result) == 1:
            _["pass"] = bool(report_result[0])

        return _

    def make_element(self):
        report_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}report")
        report_element = SubElement(report_wrapper, f"{{{self.ns.gmd}}}DQ_DomainConsistency")

        identification_wrapper = SubElement(report_element, f"{{{self.ns.gmd}}}measureIdentification")
        identification_element = SubElement(identification_wrapper, f"{{{self.ns.gmd}}}RS_Identifier")

        identification_code_element = SubElement(identification_element, f"{{{self.ns.gmd}}}code")
        identification_code_value = SubElement(identification_code_element, f"{{{self.ns.gco}}}CharacterString")
        identification_code_value.text = self.element_attributes["code"]

        identification_code_space_element = SubElement(identification_element, f"{{{self.ns.gmd}}}codeSpace")
        identification_code_space_value = SubElement(
            identification_code_space_element, f"{{{self.ns.gco}}}CharacterString"
        )
        identification_code_space_value.text = self.element_attributes["code_space"]

        result_wrapper = SubElement(report_element, f"{{{self.ns.gmd}}}result")
        result_element = SubElement(result_wrapper, f"{{{self.ns.gmd}}}DQ_ConformanceResult")

        specification_element = SubElement(result_element, f"{{{self.ns.gmd}}}specification")
        citation = Citation(
            record=self.record,
            attributes=self.attributes,
            parent_element=specification_element,
            element_attributes=self.element_attributes,
        )
        citation.make_element()

        explanation_element = SubElement(result_element, f"{{{self.ns.gmd}}}explanation")
        explanation_value = SubElement(explanation_element, f"{{{self.ns.gco}}}CharacterString")
        explanation_value.text = self.element_attributes["explanation"]

        pass_element = SubElement(result_element, f"{{{self.ns.gmd}}}pass")
        pass_value = SubElement(pass_element, f"{{{self.ns.gco}}}Boolean")
        pass_value.text = str(self.element_attributes["pass"]).lower()


class Lineage(MetadataRecordElement):
    def make_config(self) -> str:
        _ = ""

        lineage_value = self.record.xpath(
            f"{self.xpath}/gmd:LI_Lineage/gmd:statement/gco:CharacterString/text()", namespaces=self.ns.nsmap()
        )
        if len(lineage_value) == 1:
            _ = lineage_value[0]

        return _

    def make_element(self):
        if "lineage" in self.element_attributes:
            lineage_container = SubElement(self.parent_element, f"{{{self.ns.gmd}}}lineage")
            lineage_wrapper = SubElement(lineage_container, f"{{{self.ns.gmd}}}LI_Lineage")
            lineage_element = SubElement(lineage_wrapper, f"{{{self.ns.gmd}}}statement")
            lineage_value = SubElement(lineage_element, f"{{{self.ns.gco}}}CharacterString")
            lineage_value.text = self.element_attributes["lineage"]
