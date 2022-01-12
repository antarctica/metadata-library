import json
from copy import deepcopy
from datetime import date, datetime
from itertools import groupby
from typing import List, Optional, Union


def _sort_dict_by_keys(dictionary: dict) -> dict:
    """
    Utility method to recursively sort a dictionary by it's keys.

    Keys are sorted alphabetically in ascending order.

    :type dictionary: dict
    :param dictionary: input dictionary

    :rtype dict
    :return dictionary sorted by keys
    """
    return {k: _sort_dict_by_keys(v) if isinstance(v, dict) else v for k, v in sorted(dictionary.items())}


def _decode_date_properties(dictionary: dict, parent_keys: Optional[List[str]] = None) -> dict:
    """
    Utility method to convert any date(time) values in a record configuration into a Python date(time) object using the
    `decode_date_string()` method (to handle partial dates).

    Date properties that are searched for:
    - metadata.date_stamp
    - *.dates.*
    - identification.extent.temporal.period.*

    E.g.
    - '2012-02-20' becomes `{'date': date(2012, 2, 20)}`
    - '2012-02' becomes `{'date': date(2012, 1, 1), 'date_precision': 'year'}`

    :type dictionary: dict
    :param dictionary: input dictionary
    :type parent_keys: list
    :param parent_keys: list of parent keys when current key/value has been accessed through recursion

    :rtype dict
    :return dictionary with parsed property values
    """
    if parent_keys is None:
        parent_keys = []

    for key, value in list(dictionary.items()):
        # check if value in dict is itself a dictionary, or a list of dictionaries, and recurse into if so
        if isinstance(value, list):
            for list_value in value:
                if isinstance(list_value, dict):
                    parent_keys.append(key)
                    _decode_date_properties(dictionary=list_value, parent_keys=parent_keys)
                    parent_keys.remove(key)
        elif isinstance(value, dict):
            parent_keys.append(key)
            _decode_date_properties(dictionary=value, parent_keys=parent_keys)
            parent_keys.remove(key)

        # check if key is a property that will contain a date(time) value
        elif isinstance(value, str) and "metadata" in parent_keys and key == "date_stamp":
            dictionary[key] = date.fromisoformat(value)
        elif isinstance(value, str) and "dates" in parent_keys:
            dictionary[key] = decode_date_string(date_datetime=value)
        elif (
            isinstance(value, str)
            and "identification" in parent_keys
            and "extent" in parent_keys
            and "temporal" in parent_keys
            and "period" in parent_keys
        ):
            dictionary[key] = decode_date_string(date_datetime=value)

    return dictionary


def _encode_date_properties(dictionary: dict) -> dict:
    """
    Utility method to recursively convert any date values into a string value using the `encode_date_string()` utility
    method.

    Dates are represented as an dict with a date property, containing a date or datetime object, plus an optional date
    precision value. As dates are dicts, it's necessary for this method to check, when recusing through values, whether
    a value is a date dict, or a property dict. Otherwise this method will produce incorrect results.

    :type dictionary: dict
    :param dictionary: input dictionary

    :rtype dict
    :return dictionary with encoded property values
    """
    for key, value in list(dictionary.items()):
        if isinstance(value, list):
            # list of dictionaries, loop and recurse into
            for list_value in value:
                if isinstance(list_value, dict):
                    _encode_date_properties(dictionary=list_value)
        elif isinstance(value, dict) and list(value.keys()) == ["date"]:
            # date or datetime
            dictionary[key] = encode_date_string(date_datetime=value["date"])
        elif isinstance(value, dict) and {"date", "date_precision"}.issubset(set(value.keys())):
            # date or datetime with precision
            dictionary[key] = encode_date_string(date_datetime=value["date"], date_precision=value["date_precision"])
        elif isinstance(value, dict):
            # value is dictionary itself, recurse into
            _encode_date_properties(dictionary=value)
        elif isinstance(value, date) and key == "date_stamp":
            # metadata.date_stamp is always a date
            dictionary[key] = value.isoformat()

    return dictionary


def encode_date_string(date_datetime: Union[date, datetime], date_precision: str = None) -> str:
    """
    Formats a python date or datetime object as an ISO 8601 date or datetime string representation

    This method includes support for partial dates (year or year month) via an optional date precision element.
    When set the month and/or day elements in the Python date object are ignored when encoding as an ISO date.

    This is intended to work around issues where a date is not known for example but Python's date object requires
    one to be set. '1' is used as a default/convention but without a precision flag it isn't possible to know if '1'
    represents the first of the month (and is known), or represents an unknown value.

    This method is the inverse of `encode_date_string`.

    Examples:
    * 'date(2012, 4, 18)' is returned as '2012-04-18'
    * 'datetime(2012, 4, 18, 22, 48, 56)' is returned as '2012-4-18T22:48:56'
    * 'date(2012, 4, 18), date_precision='year' is returned as '2012'
    * 'date(2012, 4, 18), date_precision='month' is returned as '2012-04'

    :type date_datetime: date/datetime
    :param date_datetime: python date/datetime
    :type date_precision: str
    :param date_precision: qualifier to limit the precision of the date_datetime to a month or year

    :rtype str
    :return: ISO 8601 formatted date/datetime
    """
    if date_precision is None:
        return date_datetime.isoformat()
    if date_precision == "year":
        return str(date_datetime.year)
    if date_precision == "month":
        return f"{date_datetime.year}-{date_datetime.month:02}"


def decode_date_string(date_datetime: str) -> dict:
    """
    Parses an ISO 8601 date, partial date or datetime string representation as a python date or datetime object

    This method includes support for partial dates (year or year month) via an optional date precision element.
    When applicable, a `date_precision` property will be included in the returned dict to indicate the date object
    is precise to the 'month' or 'year'.

    This is intended to work around issues where a date is not known for example but Python's date object requires
    one to be set. '1' is used as a default/convention but without a precision flag it isn't possible to know if '1'
    represents the first of the month (and is known), or represents an unknown value.

    This method is the inverse of `encode_date_string`.

    Examples:
    * '2012-04-18' is returned as '{date(2012, 4, 18)}'
    * '2012-4-18T22:48:56' is returned as 'datetime(2012, 4, 18, 22, 48, 56)'
    * '2012' is returned as {'date(2012, 1, 1), date_precision='year'}
    * '2012-04' is returned as {'date(2012, 1, 1), date_precision='month'}

    :type date_datetime: str
    :param date_datetime: ISO 8601 formatted date/datetime

    :rtype dict
    :return: dict containing a python date/datetime and optionally a date_precision qualifying string
    """
    if "T" in date_datetime:
        return {"date": datetime.fromisoformat(date_datetime)}

    _ = {}
    _date_datetime_parts = date_datetime.split("-")
    if len(_date_datetime_parts) == 1:
        # Assume a year only date
        date_datetime = f"{date_datetime}-01-01"
        _["date_precision"] = "year"
    elif len(_date_datetime_parts) == 2:
        # Assume a year and month only date
        date_datetime = f"{date_datetime}-01"
        _["date_precision"] = "month"

    _["date"] = datetime.fromisoformat(date_datetime).date()
    return _


def contacts_condense_roles(contacts: List[dict]):
    """
    Groups separate contacts with multiple roles into a single contact with multiple roles

    I.e. if two contacts are identical but with different, singular, roles, this method will return a single contact
    with multiple roles.

    E.g. a set of contacts: {'name': 'foo', role: ['a']}, {'name': 'foo', role: ['b']}, {'name': 'bar', role: ['a']}
               with become: {'name': 'foo', role: ['a', 'b']}, {'name': 'bar', role: ['a']}

    Note: this method triggers a bug-bear error in flake8 for an unused loop control variable. In this case the error
    is invalid as the 'key' control variable is used in the groupby lambda function, rather than the body of the loop.

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

    for key, contact in groupby(_contacts_without_roles, key=lambda x: x["key"]):  # noqa: B007 - see docblock
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

    Prevents inconsistencies with how numbers are formatted (e.g. '12.0' as '12')

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


def decode_config_from_json(config: dict) -> dict:
    """
    Parse a record configuration loaded from a JSON encoded document

    Specifically this method looks for any string encoded date or datetime values and converts them to their Python
    equivalents, including workarounds for partial dates if applicable. E.g. '2012-02' becomes
    `{'date': date(2012, 2, 1), 'date_precision': 'year'}`.

    This method is the reverse of `encode_config_for_json()`.

    :type config: dict
    :param config: record configuration

    :rtype dict
    :return parsed record configuration
    """
    return _decode_date_properties(dictionary=config)


def encode_config_for_json(config: dict) -> dict:
    """
    Prepare a record configuration for use in a JSON encoded document

    Specifically this method looks for any date or datetime values and converts them to their string equivalents.
    E.g. `{'date': date(2012, 2, 1), 'date_precision': 'year'}` becomes '2012-02'.

    This method is the reverse of `decode_config_from_json()`.

    :type config: dict
    :param config: record configuration

    :rtype dict
    :return encoded record configuration
    """
    return _encode_date_properties(dictionary=config)
