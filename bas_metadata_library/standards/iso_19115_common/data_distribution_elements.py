from copy import deepcopy

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
from bas_metadata_library.standards.iso_19115_common.utils import format_numbers_consistently


class DataDistribution(MetadataRecordElement):
    def make_config(self) -> list:
        _ = []

        distributions_length = int(
            self.record.xpath(
                f"count({self.xpath}/gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor)",
                namespaces=self.ns.nsmap(),
            )
        )
        for distribution_index in range(1, distributions_length + 1):
            distribution = Distribution(
                record=self.record,
                attributes=self.attributes,
                xpath=f"{self.xpath}/gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor[{distribution_index}]/gmd:MD_Distributor",
            )
            _distribution = distribution.make_config()
            if bool(_distribution):
                _.append(_distribution)

        return _

    def make_element(self):
        data_distribution_wrapper = SubElement(self.record, f"{{{self.ns.gmd}}}distributionInfo")
        data_distribution_element = SubElement(data_distribution_wrapper, f"{{{self.ns.gmd}}}MD_Distribution")

        for distribution_config in self.element_attributes:
            distribution_element = Distribution(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_distribution_element,
                element_attributes=distribution_config,
            )
            distribution_element.make_element()


class Distribution(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        distributor = Distributor(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:distributorContact",
        )
        _distributor = distributor.make_config()
        if bool(_distributor):
            _["distributor"] = _distributor

        # use transfer options as a proxy for the number of distribution options that exist
        distribution_options_length = int(
            self.record.xpath(
                f"count({self.xpath}/gmd:distributorTransferOptions)",
                namespaces=self.ns.nsmap(),
            )
        )
        _["distribution_options"] = []
        for distribution_option_index in range(1, distribution_options_length + 1):
            _distribution_option = {}

            # currently we match up formats and transfer options without knowing if they really relate to each other.
            # This will be addressed in [#108].

            distribution_option_format = DistributorFormat(
                record=self.record,
                attributes=self.attributes,
                xpath=f"{self.xpath}/gmd:distributorFormat[{distribution_option_index}]",
            )
            _distribution_option_format = distribution_option_format.make_config()
            if bool(_distribution_option_format):
                _distribution_option["format"] = _distribution_option_format

            distribution_transfer_option = DistributorTransferOption(
                record=self.record,
                attributes=self.attributes,
                xpath=f"{self.xpath}/gmd:distributorTransferOptions[{distribution_option_index}]",
            )
            _distribution_transfer_option = distribution_transfer_option.make_config()
            if bool(_distribution_transfer_option):
                _distribution_option["transfer_option"] = _distribution_transfer_option

            if "format" in _distribution_option or "transfer_option" in _distribution_option:
                _["distribution_options"].append(_distribution_option)

        return _

    def make_element(self) -> None:
        distribution_container = SubElement(self.parent_element, f"{{{self.ns.gmd}}}distributor")
        distribution_element = SubElement(distribution_container, f"{{{self.ns.gmd}}}MD_Distributor")

        distributor = Distributor(
            record=self.record,
            attributes=self.attributes,
            parent_element=distribution_element,
            element_attributes=self.element_attributes["distributor"],
        )
        distributor.make_element()

        for distribution_option in self.element_attributes["distribution_options"]:
            if "format" in distribution_option.keys():
                distribution_format = DistributorFormat(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=distribution_element,
                    element_attributes=distribution_option["format"],
                )
                distribution_format.make_element()

            if "transfer_option" in distribution_option.keys():
                transfer_option = DistributorTransferOption(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=distribution_element,
                    element_attributes=distribution_option["transfer_option"],
                )
                transfer_option.make_element()


class Distributor(MetadataRecordElement):
    def make_config(self) -> dict:
        responsible_party = ResponsibleParty(record=self.record, attributes=self.attributes, xpath=self.xpath)
        _responsible_party = responsible_party.make_config()
        if not bool(_responsible_party):  # pragma: no cover
            return {}

        return _responsible_party

    def make_element(self):
        distributor_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}distributorContact")

        # roles need to looped through, but will always be 'distributor' only for distributors
        self.element_attributes = deepcopy(self.element_attributes)
        self.element_attributes["role"] = self.element_attributes["role"][0]

        responsible_party = ResponsibleParty(
            record=self.record,
            attributes=self.attributes,
            parent_element=distributor_element,
            element_attributes=self.element_attributes,
        )
        responsible_party.make_element()


class DistributorFormat(MetadataRecordElement):
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
        distribution_format_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}distributorFormat")
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
                attrib={f"{{{self.ns.gco}}}nilReason": "missing"},
            )


class DistributorTransferOption(MetadataRecordElement):
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
            _["size"]["magnitude"] = format_numbers_consistently(size_magnitude[0])

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
        transfer_options_container = SubElement(self.parent_element, f"{{{self.ns.gmd}}}distributorTransferOptions")
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
                transfer_size_magnitude_value.text = str(
                    format_numbers_consistently(self.element_attributes["size"]["magnitude"])
                )

        transfer_options_element = SubElement(transfer_options_wrapper, f"{{{self.ns.gmd}}}onLine")
        online_resource = OnlineResource(
            record=self.record,
            attributes=self.attributes,
            parent_element=transfer_options_element,
            element_attributes=self.element_attributes["online_resource"],
        )
        online_resource.make_element()
