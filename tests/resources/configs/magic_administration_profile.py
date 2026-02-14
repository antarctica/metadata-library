import datetime
import json

from tests.resources.configs.magic_discovery_profile import _appendix_2

_appendix_1_v1 = {
    "specification": {
        "title": {
            "value": "British Antarctic Survey (BAS) Mapping and Geographic Information Centre (MAGIC) Administration Metadata Profile",
            "href": "https://metadata-standards.data.bas.ac.uk/profiles/magic-administration/v1/",
        },
        "dates": {"publication": {"date": datetime.date(2025, 10, 22)}},
        "edition": "1",
        "contact": {**_appendix_2, "role": ["publisher"]},
    },
    "explanation": "Resource within scope of British Antarctic Survey (BAS) Mapping and Geographic Information Centre (MAGIC) Administration Metadata Profile.",
    "result": True,
}

_content_minimal_v1_id = "c321cfb7-5541-4881-88cc-73f2a4a8f533"
content_minimal_v1 = {
    "$schema": "https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/magic-administration-content-v1.json",
    "id": _content_minimal_v1_id,
}

_content_all_v1_id = "1ddf0fa2-3dab-456b-baed-09803260a4e2"
_content_all_v1_permissions = [
    {
        "directory": "*",
        "group": "*",
        "expiry": "2099-12-31T23:59:59+00:00",
    },
    {"directory": "123", "group": "~bas-staff", "expiry": "2099-12-31T23:59:59+00:00", "comment": "..."},
]
content_all_v1 = {
    "$schema": "https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/magic-administration-content-v1.json",
    "id": _content_all_v1_id,
    "gitlab_issues": ["https://gitlab.data.bas.ac.uk/MAGIC/example/-/issues/123"],
    "metadata_permissions": _content_all_v1_permissions,
    "resource_permissions": _content_all_v1_permissions,
}


def _make_encoding_for_content(admin_meta: dict, configuration: str, version: str) -> dict:
    return {
        "$schema": "https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v4.json",
        "file_identifier": admin_meta["id"],
        "metadata": {
            "contacts": [{**_appendix_2, "role": ["pointOfContact"]}],
            "date_stamp": datetime.date(2024, 10, 3),
        },
        "identification": {
            "title": {
                "value": f"Test Record with minimal MAGIC Administration Profile properties ({configuration}_{version})"
            },
            "dates": {
                "creation": {"date": datetime.date(2024, 9, 14)},
            },
            "abstract": f"Test Record for ISO 19115 metadata standard (MAGIC Administration {version} profile) with required properties only and a {configuration} administration metadata instance.",
            "language": "eng",
            "supplemental_information": json.dumps({"admin_metadata": "..."}),
            "domain_consistency": [_appendix_1_v1],
        },
    }


content_configs_v1_all = {"minimal_v1": content_minimal_v1, "all_v1": content_all_v1}
encoding_configs_v1_all = {
    "minimal_v1": _make_encoding_for_content(content_minimal_v1, "minimal", "v1"),
    "all_v1": _make_encoding_for_content(content_all_v1, "all", "v1"),
}

content_configs_all = {**content_configs_v1_all}
encoding_configs_all = {**encoding_configs_v1_all}
