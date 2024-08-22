import json
from copy import deepcopy
from hashlib import sha1

from lxml.etree import SubElement  # nosec - see 'lxml` package (bandit)' section in README

from bas_metadata_library.standards.iso_19115_common import MetadataRecordElement
from bas_metadata_library.standards.iso_19115_common.common_elements import (
    Format,
    OnlineResource,
    ResponsibleParty,
)
from bas_metadata_library.standards.iso_19115_common.utils import (
    condense_distribution_distributors,
    flatten_distribution_distributors,
    format_distribution_option_consistently,
    format_numbers_consistently,
)


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
                xpath=f"{self.xpath}/gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor[{distribution_index}]/"
                f"gmd:MD_Distributor",
            )
            _distribution = distribution.make_config()
            if bool(_distribution):
                _.append(_distribution)

        # distributions are grouped by distributor in ISO but should not be in configs
        return flatten_distribution_distributors(distributions=_)

    def make_element(self) -> None:
        data_distribution_wrapper = SubElement(self.record, f"{{{self.ns.gmd}}}distributionInfo")
        data_distribution_element = SubElement(data_distribution_wrapper, f"{{{self.ns.gmd}}}MD_Distribution")

        # distributions are grouped by distributor in ISO but aren't in configs
        # noinspection PyTypeChecker
        distributions = condense_distribution_distributors(distributions=self.element_attributes)

        for distribution_config in distributions:
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

        _distribution_formats = []
        distribution_formats_length = int(
            self.record.xpath(
                f"count({self.xpath}/gmd:distributorFormat)",
                namespaces=self.ns.nsmap(),
            )
        )
        for distribution_format_index in range(1, distribution_formats_length + 1):
            distribution_option_format = DistributorFormat(
                record=self.record,
                attributes=self.attributes,
                xpath=f"{self.xpath}/gmd:distributorFormat[{distribution_format_index}]",
            )
            _distribution_option_format = distribution_option_format.make_config()
            if bool(_distribution_option_format):
                _distribution_formats.append(_distribution_option_format)

        _transfer_options = []
        transfer_options_length = int(
            self.record.xpath(
                f"count({self.xpath}/gmd:distributorTransferOptions)",
                namespaces=self.ns.nsmap(),
            )
        )
        for transfer_option_index in range(1, transfer_options_length + 1):
            distribution_transfer_option = DistributorTransferOption(
                record=self.record,
                attributes=self.attributes,
                xpath=f"{self.xpath}/gmd:distributorTransferOptions[{transfer_option_index}]",
            )
            _distribution_transfer_option = distribution_transfer_option.make_config()
            if bool(_distribution_transfer_option):
                _transfer_options.append(_distribution_transfer_option)

        _["distribution_options"] = self._match_distribution_options(
            distribution_formats=_distribution_formats, transfer_options=_transfer_options
        )

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

        _formats: list[DistributorFormat] = []
        _transfer_options: list[DistributorTransferOption] = []

        for distribution_option in self.element_attributes["distribution_options"]:
            # ID elements are generated by hashing a JSON encoding of the entire distribution object,
            # see the README 'Automatic transfer option / format IDs' section for more information
            _distribution_option = format_distribution_option_consistently(distribution_option=distribution_option)
            # S324 warning is exempted as these hashes are not used for any security related purposes
            _id = sha1(json.dumps(_distribution_option).encode()).hexdigest()  # noqa: S324

            if "format" in distribution_option:
                distribution_format = DistributorFormat(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=distribution_element,
                    element_attributes={**distribution_option["format"], "_id": _id},
                )
                _formats.append(distribution_format)

            if "transfer_option" in distribution_option:
                transfer_option = DistributorTransferOption(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=distribution_element,
                    element_attributes={**distribution_option["transfer_option"], "_id": _id},
                )
                _transfer_options.append(transfer_option)

        for _format in _formats:
            _format.make_element()
        for _transfer_option in _transfer_options:
            _transfer_option.make_element()

    @staticmethod
    def _match_distribution_options(distribution_formats: list[dict], transfer_options: list[dict]) -> list[dict]:  # noqa: C901 see uk-pdc/metadata-infrastructure/metadata-library#175 for more information
        """
        Utility method to match distribution formats and transfer options into complete or partial distribution objects.

        See the README 'Automatic transfer option / format IDs' section for more information on the background to this
        feature and why it's needed.

        Note: there is almost certainly a more elegant/efficient way to do this process. Alternative/improved
        implementations are definitely welcome as contributions.

        :param distribution_formats: list of distribution format objects
        :param transfer_options: list of transfer option objects
        :return list of complete or partial distribution option objects
        """
        distribution_options = []
        _distribution_formats = {}
        _transfer_options = {}
        _unmatched_distribution_formats = []
        _unmatched_transfer_options = []
        _matched_distribution_formats = []
        _matched_transfer_options = []

        # index options by ID or add to unmatched list
        for distribution_format in distribution_formats:
            if "_id" in distribution_format:
                _id = distribution_format["_id"]
                del distribution_format["_id"]
                _distribution_formats[_id] = distribution_format
                continue
            _unmatched_distribution_formats.append(distribution_format)
        for transfer_option in transfer_options:
            if "_id" in transfer_option:
                _id = transfer_option["_id"]
                del transfer_option["_id"]
                _transfer_options[_id] = transfer_option
                continue
            _unmatched_transfer_options.append(transfer_option)

        # try to match up items or add to unmatched list
        if len(_distribution_formats) >= len(_transfer_options):
            for fmt_id, distribution_format in _distribution_formats.items():
                if fmt_id not in _transfer_options:
                    _unmatched_distribution_formats.append(distribution_format)
                    continue

                distribution_options.append(
                    {"format": distribution_format, "transfer_option": _transfer_options[fmt_id]}
                )
                _matched_distribution_formats.append(fmt_id)
                _matched_transfer_options.append(fmt_id)
        if len(_transfer_options) > len(_distribution_formats):
            for tfo_id, transfer_option in _transfer_options.items():
                if tfo_id not in _distribution_formats:
                    _unmatched_transfer_options.append(transfer_option)
                    continue

                distribution_options.append(
                    {"format": _distribution_formats[tfo_id], "transfer_option": transfer_option}
                )
                _matched_transfer_options.append(tfo_id)
                _matched_distribution_formats.append(tfo_id)

        # add all unmatched items as non-complete distribution options
        for unmatched_distribution_format in _unmatched_distribution_formats:
            distribution_options.append({"format": unmatched_distribution_format})
        for unmatched_transfer_options in _unmatched_transfer_options:
            distribution_options.append({"transfer_option": unmatched_transfer_options})

        return distribution_options


class Distributor(MetadataRecordElement):
    def make_config(self) -> dict:
        responsible_party = ResponsibleParty(record=self.record, attributes=self.attributes, xpath=self.xpath)
        return responsible_party.make_config()

    def make_element(self) -> None:
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
        distributor_format = Format(record=self.record, attributes=self.attributes, xpath=self.xpath)
        return distributor_format.make_config()

    def make_element(self) -> None:
        distributor_format_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}distributorFormat")

        distributor_format = Format(
            record=self.record,
            attributes=self.attributes,
            parent_element=distributor_format_element,
            element_attributes=self.element_attributes,
        )
        distributor_format.make_element()


class DistributorTransferOption(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        format_id = self.record.xpath(f"{self.xpath}/gmd:MD_DigitalTransferOptions/@id", namespaces=self.ns.nsmap())
        if len(format_id) == 1:
            _id: str = format_id[0].replace("bml-", "")
            _id = _id.replace("-tfo", "")
            _["_id"] = _id

        size_unit = self.record.xpath(
            f"{self.xpath}/gmd:MD_DigitalTransferOptions/gmd:unitsOfDistribution/gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(size_unit) == 1:
            if "size" not in _:
                _["size"] = {}
            _["size"]["unit"] = size_unit[0]

        size_magnitude = self.record.xpath(
            f"{self.xpath}/gmd:MD_DigitalTransferOptions/gmd:transferSize/gco:Real/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(size_magnitude) == 1:
            if "size" not in _:
                _["size"] = {}
            _["size"]["magnitude"] = format_numbers_consistently(size_magnitude[0])

        online_resource = OnlineResource(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:MD_DigitalTransferOptions/gmd:onLine",
        )
        _online_resource = online_resource.make_config()
        if bool(_online_resource):
            _["online_resource"] = _online_resource

        if list(_.keys()) == ["_id"]:
            _ = {}
        return _

    def make_element(self) -> None:
        transfer_options_container = SubElement(self.parent_element, f"{{{self.ns.gmd}}}distributorTransferOptions")
        transfer_options_wrapper = SubElement(
            transfer_options_container,
            f"{{{self.ns.gmd}}}MD_DigitalTransferOptions",
            attrib={"id": f"bml-{self.element_attributes['_id']}-tfo"},
        )

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
