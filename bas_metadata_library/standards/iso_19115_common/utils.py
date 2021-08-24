import json
from copy import deepcopy
from datetime import date, datetime
from itertools import groupby
from typing import Union, List


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


def convert_from_v1_to_v2_configuration(config: dict) -> dict:
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

    if "resource" in config:
        config["identification"] = config["resource"]
        del config["resource"]

    return config


def convert_from_v2_to_v1_configuration(config: dict) -> dict:
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

    return config
