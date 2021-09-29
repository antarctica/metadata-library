import json
from copy import deepcopy
from datetime import date, datetime
from itertools import groupby
from typing import Union, List


def _sort_dict_by_keys(dictionary: dict) -> dict:
    """
    Utility method to sort a dictionary by it's keys recursively.

    Keys are sorted alphabetically in ascending order.

    :type dictionary: dict
    :param dictionary: input dictionary

    :rtype dict
    :return dictionary sorted by keys
    """
    return {k: _sort_dict_by_keys(v) if isinstance(v, dict) else v for k, v in sorted(dictionary.items())}


def format_date_string(date_datetime: Union[date, datetime]) -> str:
    """
    Formats a python date or datetime as an ISO 8601 date or datetime string representation

    E.g. Return 'date(2012, 4, 18)' as '2012-04-18' or 'datetime(2012, 4, 18, 22, 48, 56)' as '2012-4-18T22:48:56'.

    :type date_datetime: date/datetime
    :param date_datetime: python date/datetime

    :rtype str
    :return: ISO 8601 formatted date/datetime
    """
    return date_datetime.isoformat()


def contacts_have_role(contacts: list, role: str) -> bool:  # pragma: no cover
    """
    Checks if at least one contact has a given role

    E.g. in all the contacts in a resource, do any have the 'distributor' role?

    :type contacts: list
    :param contacts: list of contacts (point of contacts)
    :type role: str
    :param role: role to check for

    :rtype bool
    :return True if at least one contact has the given role, otherwise False
    """
    for contact in contacts:
        if role in contact["role"]:
            return True

    return False


def contacts_condense_roles(contacts: List[dict]):
    """
    Groups separate contacts with multiple roles into a single contact with multiple roles

    I.e. if two contacts are identical but with different, singular, roles, this method will return a single contact
    with multiple roles.

    E.g. a set of contacts: {'name': 'foo', role: ['a']}, {'name': 'foo', role: ['b']}, {'name': 'bar', role: ['a']}
               with become: {'name': 'foo', role: ['a', 'b']}, {'name': 'bar', role: ['a']}

    :type contacts: list
    :param contacts: list of contacts to be grouped/reduced

    :rtype list
    :return list of contacts with merged roles
    """
    _merged_contacts = []

    _contacts_without_roles = []
    for contact in contacts:
        _contact = deepcopy(contact)
        del _contact["role"]
        _contacts_without_roles.append(
            {"key": json.dumps(_contact), "key_data": _contact, "role_data": contact["role"][0]}
        )

    for key, contact in groupby(_contacts_without_roles, key=lambda x: x["key"]):
        contact = list(contact)
        _merged_contact = contact[0]["key_data"]
        _merged_contact["role"] = []
        for _contact in contact:
            _merged_contact["role"].append(_contact["role_data"])
        _merged_contacts.append(_merged_contact)

    return _merged_contacts


def format_numbers_consistently(number: Union[int, float]) -> Union[int, float]:
    """
    Formats numeric values in a consistent way.

    Prevents inconsistencies with how numbers are formatted (e.g. should '12.0' be '12'?)

    :type number: float or int
    :param number: numeric value to format

    :rtype float or int
    :return number as an integer if applicable, otherwise float
    """
    number = float(number)
    if number.is_integer():
        number = int(number)
    return number


def format_distribution_option_consistently(distribution_option: dict) -> dict:
    """
    Formats a distribution option object into a consistent structure.

    Distribution option objects are hashed to generate ID values for linking their format and transfer options together.
    As these hashes are sensitive to the order of information, and the format of numeric values etc., this method is
    used to sort and format these objects so they are consistent, and therefore generate the same hash values.

    For example these serialised (simplified) objects are the same but have different hash values:

    1. '{'format', 'csv', 'transfer_option': {'size': '40.0', 'url': 'https://example.com/foo.csv'}}' ->
        SHA1: e1342bc7fd5736aaf2cf7e6fd465c71d975b9747
    2. '{'transfer_option': {'size': '40', 'url': 'https://example.com/foo.csv'}, 'format', 'csv'}}' ->
        SHA1: e4554470d7712aadf5f5467d6bd1427a689dea74

    By sorting the keys (so 'format' always comes before 'transfer_option' for example) and formatting '40.0' as '40',
    these differences are removed and the same hash value is given.

    :type distribution_option: dict
    :param distribution_option: distribution option object

    :rtype dict
    :return consistently structured/formatted distribution option object
    """
    _distribution_option = deepcopy(distribution_option)
    _distribution_option = _sort_dict_by_keys(dictionary=_distribution_option)
    if (
        "transfer_option" in _distribution_option
        and "size" in _distribution_option["transfer_option"]
        and "magnitude" in _distribution_option["transfer_option"]["size"]
    ):
        _distribution_option["transfer_option"]["size"]["magnitude"] = format_numbers_consistently(
            number=_distribution_option["transfer_option"]["size"]["magnitude"]
        )

    return _distribution_option


def convert_from_v1_to_v2_configuration(config: dict) -> dict:
    """
    Common method to convert a V1 ISO 19115 record configuration to a V2 configuration.

    This method is provided on an ad-hoc and best efforts basis, supporting known use-cases only.

    This method tries to be lossless wherever possible, however this is not guaranteed,
    and may not be possible in all cases.

    :type config: dict
    :param config: V1 record configuration to be converted

    :rtype dict
    :return converted V1 configuration
    """
    config = deepcopy(config)

    _metadata_keys = ["language", "character_set", "contacts", "date_stamp", "maintenance", "metadata_standard"]
    if any(key in _metadata_keys for key in config.keys()):
        config["metadata"] = {}
        for key in _metadata_keys:
            if key in config.keys():
                config["metadata"][key] = config[key]
                del config[key]

    if "resource" in config and "constraints" in config["resource"]:
        constraints = []
        constraint_types = ["access", "usage"]
        for constraint_type in constraint_types:
            if constraint_type in config["resource"]["constraints"]:
                for constraint in config["resource"]["constraints"][constraint_type]:
                    _constraint = {
                        "type": constraint_type,
                    }
                    if "restriction_code" in constraint:
                        _constraint["restriction_code"] = constraint["restriction_code"]
                    if "statement" in constraint:
                        _constraint["statement"] = constraint["statement"]

                    if "copyright_licence" in constraint:
                        _constraint["restriction_code"] = "license"
                        _constraint["statement"] = constraint["copyright_licence"]["statement"]
                        if "href" in constraint["copyright_licence"]:
                            _constraint["href"] = constraint["copyright_licence"]["href"]
                    if "required_citation" in constraint:
                        _constraint["restriction_code"] = "otherRestrictions"
                        if "statement" in constraint["required_citation"]:
                            _constraint["statement"] = constraint["required_citation"]["statement"]
                        if "doi" in constraint["required_citation"]:  # pragma: no cover
                            _constraint["statement"] = constraint["required_citation"]["doi"]
                            _constraint["href"] = constraint["required_citation"]["doi"]

                    if "restriction_code" not in _constraint:
                        _constraint["restriction_code"] = "otherRestrictions"

                    constraints.append(_constraint)
        config["resource"]["constraints"] = constraints

    if "resource" in config and "formats" in config["resource"] and "transfer_options" in config["resource"]:
        distributions: List[dict] = []

        if "contacts" in config["resource"]:
            for index, contact in enumerate(config["resource"]["contacts"]):
                if "distributor" in contact["role"]:
                    # duplicate contact as a distributor (only one role)
                    distributor = deepcopy(contact)  # type: dict
                    distributor["role"] = ["distributor"]
                    distributions.append({"distributor": distributor, "distribution_options": []})

                    # remove distributor role now contact is duplicated
                    config["resource"]["contacts"][index]["role"].remove("distributor")
                    # if contact was only a distributor, remove whole contact
                    if len(config["resource"]["contacts"][index]["role"]) == 0:
                        del config["resource"]["contacts"][index]

            # Naively group formats and transfer options together under the first distributor
            for index, transfer_option in enumerate(config["resource"]["transfer_options"]):
                distribution_option = {"transfer_option": transfer_option}
                try:
                    distribution_option["format"] = config["resource"]["formats"][index]
                except IndexError:
                    pass

                distributions[0]["distribution_options"].append(distribution_option)

        config["distribution"] = distributions
        del config["resource"]["formats"]
        del config["resource"]["transfer_options"]

    if "resource" in config:
        config["identification"] = config["resource"]
        del config["resource"]

    return config


def convert_from_v2_to_v1_configuration(config: dict) -> dict:
    """
    Common method to convert a V2 ISO 19115 record configuration to a V1 configuration.

    This method is provided on an ad-hoc and best efforts basis, supporting known use-cases only.

    This method tries to be lossless wherever possible, however this is not guaranteed,
    and may not be possible in all cases.

    :type config: dict
    :param config: V2 record configuration to be converted

    :rtype dict
    :return converted V2 configuration
    """
    _metadata_keys = ["language", "character_set", "contacts", "date_stamp", "maintenance", "metadata_standard"]
    if any(key in _metadata_keys for key in config["metadata"].keys()):
        for key in _metadata_keys:
            if key in config["metadata"].keys():
                config[key] = config["metadata"][key]
    if "metadata" in config:
        del config["metadata"]

    if "identification" in config:
        config["resource"] = config["identification"]
        del config["identification"]

    if "distribution" in config:
        config["resource"]["formats"] = []
        config["resource"]["transfer_options"] = []

        for distribution in config["distribution"]:
            role_merged = False
            for index, contact in enumerate(config["resource"]["contacts"]):
                if "email" in contact and "email" in distribution["distributor"]:
                    if contact["email"] == distribution["distributor"]["email"]:
                        config["resource"]["contacts"][index]["role"].append("distributor")
                        role_merged = True
            if not role_merged:
                config["resource"]["contacts"].append(distribution["distributor"])

            for distribution_option in distribution["distribution_options"]:
                if "format" in distribution_option.keys():
                    config["resource"]["formats"].append(distribution_option["format"])
                if "transfer_option" in distribution_option.keys():
                    config["resource"]["transfer_options"].append(distribution_option["transfer_option"])
        del config["distribution"]

    if "constraints" in config["resource"]:
        constraints = {"access": [], "usage": []}
        for constraint in config["resource"]["constraints"]:
            _constraint = {}

            if constraint["type"] == "access" and "restriction_code" in constraint:
                _constraint["restriction_code"] = constraint["restriction_code"]

            if "statement" in constraint:
                _constraint["statement"] = constraint["statement"]

            #
            # this is all a big hack
            #

            # required citation
            if "href" in constraint and "doi.org" in constraint["href"]:  # pragma: no cover
                _constraint["required_citation"] = {"doi": constraint["href"]}
            if "statement" in _constraint and "Cite this information as" in _constraint["statement"]:
                _constraint["required_citation"] = {"statement": constraint["statement"]}
                del _constraint["statement"]

            # copyright licence
            if (
                "statement" in constraint
                and "This information is licensed under the Open Government Licence v3.0." in constraint["statement"]
            ):
                _constraint["copyright_licence"] = {"statement": constraint["statement"]}
                del _constraint["statement"]
                if (
                    "href" in constraint
                    and "//www.nationalarchives.gov.uk/doc/open-government-licence/version/3/" in constraint["href"]
                ):
                    _constraint["copyright_licence"]["href"] = constraint["href"]
                    _constraint["copyright_licence"]["code"] = "OGL-UK-3.0"

            constraints[constraint["type"]].append(_constraint)

        if not constraints["access"]:  # pragma: no cover
            del constraints["access"]
        if not constraints["usage"]:  # pragma: no cover
            del constraints["usage"]
        config["resource"]["constraints"] = constraints

    # a number of new properties were not supported in the V1 schema and so are removed to prevent validation errors
    # due to unknown/unexpected properties.
    # TODO: Check this includes other new keys such as 'status'
    _new_resource_identification_keys = ["aggregations"]
    for key in _new_resource_identification_keys:  # pragma: no cover
        if key in config["resource"].keys():
            del config["resource"][key]

    return config
