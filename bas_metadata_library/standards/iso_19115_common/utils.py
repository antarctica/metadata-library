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


def contacts_have_role(contacts: list, role: str) -> bool:
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
