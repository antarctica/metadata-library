from __future__ import annotations

from lxml.etree import Element, SubElement

from bas_metadata_library import (
    MetadataRecord as _MetadataRecord,
)
from bas_metadata_library import (
    MetadataRecordElement as _MetadataRecordElement,
)
from bas_metadata_library import (
    Namespaces as _Namespaces,
)


class Namespaces(_Namespaces):
    """Defines the namespaces for this standard."""

    gmd = "http://www.isotc211.org/2005/gmd"
    gco = "http://www.isotc211.org/2005/gco"
    gml = "http://www.opengis.net/gml/3.2"
    gmx = "http://www.isotc211.org/2005/gmx"
    srv = "http://www.isotc211.org/2005/srv"
    xlink = "http://www.w3.org/1999/xlink"
    xsi = "http://www.w3.org/2001/XMLSchema-instance"
    gmi = "http://www.isotc211.org/2005/gmi"
    gss = "http://www.isotc211.org/2005/gss"
    gsr = "http://www.isotc211.org/2005/gsr"
    gts = "http://www.isotc211.org/2005/gts"

    _schema_locations = {  # noqa: RUF012
        "gmd": "https://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/gmd/gmd.xsd",
        "gco": "https://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/gco/gco.xsd",
        "gmx": "https://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/gmx/gmx.xsd",
        "srv": "https://standards.iso.org/iso/19119/srv/srv.xsd",
        "gmi": "https://standards.iso.org/iso/19115/-2/gmi/1.0/gmi.xsd",
        "gss": "https://standards.iso.org/iso/19139/Schemas/gss/gss.xsd",
        "gsr": "https://standards.iso.org/iso/19139/Schemas/gsr/gsr.xsd",
        "gts": "https://standards.iso.org/iso/19139/Schemas/gts/gts.xsd",
    }

    def __init__(self):
        self._namespaces = {
            "gmd": self.gmd,
            "gco": self.gco,
            "gml": self.gml,
            "gmx": self.gmx,
            "srv": self.srv,
            "xlink": self.xlink,
            "xsi": self.xsi,
            "gmi": self.gmi,
            "gss": self.gss,
            "gsr": self.gsr,
            "gts": self.gts,
        }
        super().__init__(namespaces=self._namespaces)


class MetadataRecordElement(_MetadataRecordElement):
    """
    Overloaded base MetadataRecordElement class.

    Sets the type hint of the record attribute to the MetadataRecord class for this metadata standard.
    """

    def __init__(
        self,
        record: _MetadataRecord,
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
        self.ns = Namespaces()


class CodeListElement(MetadataRecordElement):
    """Derived MetadataRecordElement class defining an ISO code list element."""

    def __init__(
        self,
        record: _MetadataRecord,
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
        self.code_list_values = []
        self.code_list = None
        self.element = None
        self.element_code = None
        self.attribute = None

    def make_config(self) -> str:
        """Build partial record configuration."""
        _ = ""

        value = self.record.xpath(
            f"{self.xpath}[@codeList = '{self.code_list}']/@codeListValue",
            namespaces=self.ns.nsmap(),
        )
        if len(value) == 1:
            _ = value[0]

        return _

    def make_element(self) -> None:
        """Build XML element."""
        code_list_element = SubElement(self.parent_element, self.element)
        if (
            self.attribute in self.element_attributes
            and self.element_attributes[self.attribute] in self.code_list_values
        ):
            code_list_value = SubElement(
                code_list_element,
                self.element_code,
                attrib={"codeList": self.code_list, "codeListValue": self.element_attributes[self.attribute]},
            )
            code_list_value.text = self.element_attributes[self.attribute]
