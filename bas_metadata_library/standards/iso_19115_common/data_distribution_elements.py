# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# We don't currently allow untrusted/user-provided XML so this is not a risk
from lxml.etree import SubElement  # nosec

from bas_metadata_library.standards.iso_19115_common import MetadataRecordElement
from bas_metadata_library.standards.iso_19115_common.common_elements import (
    AnchorElement,
    ResponsibleParty,
    OnlineResource,
)


class DataDistribution(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        _distribution_formats = []
        formats_length = int(
            self.record.xpath(
                f"count({self.xpath}/gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat)",
                namespaces=self.ns.nsmap(),
            )
        )
        for format_index in range(1, formats_length + 1):
            format_ = DistributionFormat(
                record=self.record,
                attributes=self.attributes,
                xpath=f"({self.xpath}/gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat)"
                f"[{format_index}]",
            )
            _format = format_.make_config()
            if bool(_format):
                _distribution_formats.append(_format)
        if len(_distribution_formats) > 0:
            _["formats"] = _distribution_formats

        _distributors = []
        distributors_length = int(
            self.record.xpath(
                f"count({self.xpath}/gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/"
                f"gmd:distributorContact)",
                namespaces=self.ns.nsmap(),
            )
        )
        for distributor_index in range(1, distributors_length + 1):
            distributor = Distributor(
                record=self.record,
                attributes=self.attributes,
                xpath=f"({self.xpath}/gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/"
                f"gmd:distributorContact)"
                f"[{distributor_index}]",
            )
            _distributor = distributor.make_config()
            if bool(_distributor):
                _distributors.append(_distributor)
        if len(_distributors) > 0:
            _["distributors"] = _distributors

        _transfer_options = []
        transfer_options_length = int(
            self.record.xpath(
                f"count({self.xpath}/gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions)",
                namespaces=self.ns.nsmap(),
            )
        )
        for transfer_option_index in range(1, transfer_options_length + 1):
            transfer_option = TransferOptions(
                record=self.record,
                attributes=self.attributes,
                xpath=f"({self.xpath}/gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions)"
                f"[{transfer_option_index}]",
            )
            _transfer_option = transfer_option.make_config()
            if bool(_transfer_option):
                _transfer_options.append(_transfer_option)
        if len(_transfer_options) > 0:
            _["transfer_options"] = _transfer_options

        return _

    def make_element(self):
        data_distribution_wrapper = SubElement(self.record, f"{{{self.ns.gmd}}}distributionInfo")
        data_distribution_element = SubElement(data_distribution_wrapper, f"{{{self.ns.gmd}}}MD_Distribution")

        if "formats" in self.attributes["resource"]:
            for format_attributes in self.attributes["resource"]["formats"]:
                distribution_format = DistributionFormat(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=data_distribution_element,
                    element_attributes=format_attributes,
                )
                distribution_format.make_element()

        if "contacts" in self.attributes["resource"]:
            for point_of_contact_attributes in self.attributes["resource"]["contacts"]:
                for role in point_of_contact_attributes["role"]:
                    if role == "distributor":
                        _point_of_contact = point_of_contact_attributes.copy()
                        _point_of_contact["role"] = role

                        distributor = Distributor(
                            record=self.record,
                            attributes=self.attributes,
                            parent_element=data_distribution_element,
                            element_attributes=_point_of_contact,
                        )
                        distributor.make_element()

        if "transfer_options" in self.attributes["resource"]:
            for transfer_attributes in self.attributes["resource"]["transfer_options"]:
                transfer_options = TransferOptions(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=data_distribution_element,
                    element_attributes=transfer_attributes,
                )
                transfer_options.make_element()


class DistributionFormat(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        format_name = self.record.xpath(
            f"{self.xpath}/gmd:MD_Format/gmd:name/gco:CharacterString/text() | "
            f"{self.xpath}/gmd:MD_Format/gmd:name/gmx:Anchor/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(format_name) == 1:
            _["format"] = format_name[0]

        format_href = self.record.xpath(
            f"{self.xpath}/gmd:MD_Format/gmd:name/gmx:Anchor/@xlink:href",
            namespaces=self.ns.nsmap(),
        )
        if len(format_href) == 1:
            _["href"] = format_href[0]

        version_value = self.record.xpath(
            f"{self.xpath}/gmd:MD_Format/gmd:version/gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(version_value) == 1:  # pragma: no cover
            _["version"] = version_value[0]

        return _

    def make_element(self):
        distribution_format_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}distributionFormat")
        distribution_format_element = SubElement(distribution_format_wrapper, f"{{{self.ns.gmd}}}MD_Format")

        format_name_element = SubElement(distribution_format_element, f"{{{self.ns.gmd}}}name")
        if "href" in self.element_attributes:
            anchor = AnchorElement(
                record=self.record,
                attributes=self.attributes,
                parent_element=format_name_element,
                element_attributes=self.element_attributes,
                element_value=self.element_attributes["format"],
            )
            anchor.make_element()
        else:
            format_name_value = SubElement(format_name_element, f"{{{self.ns.gco}}}CharacterString")
            format_name_value.text = self.element_attributes["format"]

        if "version" in self.element_attributes:
            format_version_element = SubElement(distribution_format_element, f"{{{self.ns.gmd}}}version")
            format_version_value = SubElement(format_version_element, f"{{{self.ns.gco}}}CharacterString")
            format_version_value.text = self.element_attributes["version"]
        else:
            SubElement(
                distribution_format_element,
                f"{{{self.ns.gmd}}}version",
                attrib={f"{{{self.ns.gco}}}nilReason": "unknown"},
            )


class Distributor(MetadataRecordElement):
    def make_config(self) -> dict:
        responsible_party = ResponsibleParty(record=self.record, attributes=self.attributes, xpath=self.xpath)
        _responsible_party = responsible_party.make_config()
        if not bool(_responsible_party):  # pragma: no cover
            return {}

        return _responsible_party

    def make_element(self):
        distributor_container = SubElement(self.parent_element, f"{{{self.ns.gmd}}}distributor")
        distributor_wrapper = SubElement(distributor_container, f"{{{self.ns.gmd}}}MD_Distributor")
        distributor_element = SubElement(distributor_wrapper, f"{{{self.ns.gmd}}}distributorContact")

        responsible_party = ResponsibleParty(
            record=self.record,
            attributes=self.attributes,
            parent_element=distributor_element,
            element_attributes=self.element_attributes,
        )
        responsible_party.make_element()


class TransferOptions(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        size_unit = self.record.xpath(
            f"{self.xpath}/gmd:MD_DigitalTransferOptions/gmd:unitsOfDistribution/gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(size_unit) == 1:
            if "size" not in _.keys():
                _["size"] = {}
            _["size"]["unit"] = size_unit[0]

        size_magnitude = self.record.xpath(
            f"{self.xpath}/gmd:MD_DigitalTransferOptions/gmd:transferSize/gco:Real/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(size_magnitude) == 1:
            if "size" not in _.keys():  # pragma: no cover
                _["size"] = {}
            _["size"]["magnitude"] = float(size_magnitude[0])

        online_resource = OnlineResource(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:MD_DigitalTransferOptions/gmd:onLine",
        )
        _online_resource = online_resource.make_config()
        if list(_online_resource.keys()) == ["function"] and _online_resource["function"] == "":  # pragma: no cover
            _online_resource = {}
        if bool(_online_resource):
            _["online_resource"] = _online_resource

        return _

    def make_element(self):
        transfer_options_container = SubElement(self.parent_element, f"{{{self.ns.gmd}}}transferOptions")
        transfer_options_wrapper = SubElement(transfer_options_container, f"{{{self.ns.gmd}}}MD_DigitalTransferOptions")

        if "size" in self.element_attributes:
            if "unit" in self.element_attributes["size"]:
                transfer_size_unit_element = SubElement(
                    transfer_options_wrapper, f"{{{self.ns.gmd}}}unitsOfDistribution"
                )
                transfer_size_unit_value = SubElement(transfer_size_unit_element, f"{{{self.ns.gco}}}CharacterString")
                transfer_size_unit_value.text = self.element_attributes["size"]["unit"]
            if "magnitude" in self.element_attributes["size"]:
                transfer_size_magnitude_element = SubElement(transfer_options_wrapper, f"{{{self.ns.gmd}}}transferSize")
                transfer_size_magnitude_value = SubElement(transfer_size_magnitude_element, f"{{{self.ns.gco}}}Real")
                transfer_size_magnitude_value.text = str(self.element_attributes["size"]["magnitude"])

        transfer_options_element = SubElement(transfer_options_wrapper, f"{{{self.ns.gmd}}}onLine")
        online_resource = OnlineResource(
            record=self.record,
            attributes=self.attributes,
            parent_element=transfer_options_element,
            element_attributes=self.element_attributes["online_resource"],
        )
        online_resource.make_element()
