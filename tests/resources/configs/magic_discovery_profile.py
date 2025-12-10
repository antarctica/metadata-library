import datetime
from copy import deepcopy

_appendix_2 = {
    "organisation": {
        "name": "Mapping and Geographic Information Centre, British Antarctic Survey",
        "href": "https://ror.org/01rhff309",
        "title": "ror",
    },
    "phone": "+44 (0)1223 221400",
    "address": {
        "delivery_point": "British Antarctic Survey, High Cross, Madingley Road",
        "city": "Cambridge",
        "administrative_area": "Cambridgeshire",
        "postal_code": "CB3 0ET",
        "country": "United Kingdom",
    },
    "email": "magic@bas.ac.uk",
    "online_resource": {
        "href": "https://www.bas.ac.uk/teams/magic",
        "title": "Mapping and Geographic Information Centre (MAGIC) - BAS public website",
        "description": "General information about the BAS Mapping and Geographic Information Centre (MAGIC) from the British Antarctic Survey (BAS) public website.",
        "function": "information",
    },
}

_appendix_1_v1 = {
    "specification": {
        "title": {
            "value": "British Antarctic Survey (BAS) Mapping and Geographic Information Centre (MAGIC) Discovery Metadata Profile",
            "href": "https://metadata-standards.data.bas.ac.uk/profiles/magic-discovery-v1/",
        },
        "dates": {"publication": {"date": datetime.date(2024, 11, 1)}},
        "edition": "1",
        "contact": {**_appendix_2, "role": ["publisher"]},
    },
    "explanation": "Resource within scope of British Antarctic Survey (BAS) Mapping and Geographic Information Centre (MAGIC) Discovery Metadata Profile.",
    "result": True,
}
_appendix_1_v1_alt = deepcopy(_appendix_1_v1)
_appendix_1_v1_alt["specification"]["title"]["href"] = (
    "https://metadata-standards.data.bas.ac.uk/profiles/magic-discovery/v1/"
)

_appendix_1_v2 = {
    "specification": {
        "title": {
            "value": "British Antarctic Survey (BAS) Mapping and Geographic Information Centre (MAGIC) Discovery Metadata Profile",
            "href": "https://metadata-standards.data.bas.ac.uk/profiles/magic-discovery/v2/",
        },
        "dates": {"publication": {"date": datetime.date(2025, 11, 24)}},
        "edition": "2",
        "contact": {**_appendix_2, "role": ["publisher"]},
    },
    "explanation": "Resource within scope of British Antarctic Survey (BAS) Mapping and Geographic Information Centre (MAGIC) Discovery Metadata Profile.",
    "result": True,
}

_minimal_product_v1_id = "f866c298-3b9a-4624-ac31-cd6b97c146fa"
minimal_product_v1 = {
    "$schema": "https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v4.json",
    "file_identifier": _minimal_product_v1_id,
    "metadata": {
        "contacts": [{**_appendix_2, "role": ["pointOfContact"]}],
        "date_stamp": datetime.date(2024, 10, 3),
    },
    "hierarchy_level": "product",
    "identification": {
        "title": {"value": "Test product with minimal MAGIC Discovery Profile properties"},
        "dates": {
            "creation": {"date": datetime.date(2024, 9, 14)},
            "released": {"date": datetime.datetime(2024, 9, 14, 11, 16, 22, tzinfo=datetime.timezone.utc)},
            "publication": {"date": datetime.datetime(2024, 9, 14, 11, 16, 22, tzinfo=datetime.timezone.utc)},
        },
        "edition": "1",
        "identifiers": [
            {
                "identifier": _minimal_product_v1_id,
                "href": f"https://data.bas.ac.uk/items/{_minimal_product_v1_id}",
                "namespace": "data.bas.ac.uk",
            }
        ],
        "abstract": "An example product to verify a record with the minimal set of properties required by the MAGIC Discovery Profile is handled correctly.",
        "contacts": [{**_appendix_2, "role": ["pointOfContact"]}],
        "maintenance": {"maintenance_frequency": "asNeeded", "progress": "completed"},
        "constraints": [
            {"type": "access", "restriction_code": "unrestricted"},
            {
                "type": "usage",
                "restriction_code": "license",
                "statement": "This information is licensed under the Open Government Licence (OGL 3.0). To view this licence, visit https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/.",
                "href": "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
            },
        ],
        "language": "eng",
        "extents": [
            {
                "identifier": "bounding",
                "geographic": {
                    "bounding_box": {
                        "west_longitude": -180.0,
                        "east_longitude": 180.0,
                        "south_latitude": -90.0,
                        "north_latitude": -60.0,
                    }
                },
            }
        ],
        "lineage": {"statement": "This is a fictitious record and has no real origin."},
        "domain_consistency": [_appendix_1_v1],
    },
}

_minimal_collection_v1_id = "0c553abe-5cfa-4208-8354-8cbdafb064d4"
minimal_collection_v1 = {
    "$schema": "https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v4.json",
    "file_identifier": _minimal_collection_v1_id,
    "metadata": {
        "contacts": [{**_appendix_2, "role": ["pointOfContact"]}],
        "date_stamp": datetime.date(2024, 10, 3),
    },
    "hierarchy_level": "collection",
    "identification": {
        "title": {"value": "Test collection with minimal MAGIC Discovery Profile properties"},
        "dates": {
            "creation": {"date": datetime.date(2024, 9, 14)},
            "released": {"date": datetime.datetime(2024, 9, 14, 16, 43, 56, tzinfo=datetime.timezone.utc)},
            "publication": {"date": datetime.datetime(2024, 9, 14, 16, 43, 56, tzinfo=datetime.timezone.utc)},
        },
        "edition": "1",
        "identifiers": [
            {
                "identifier": _minimal_collection_v1_id,
                "href": f"https://data.bas.ac.uk/items/{_minimal_collection_v1_id}",
                "namespace": "data.bas.ac.uk",
            }
        ],
        "abstract": "An example collection to verify a record with the minimal set of properties required by the MAGIC Discovery Profile is handled correctly.",
        "contacts": [{**_appendix_2, "role": ["pointOfContact"]}],
        "maintenance": {"maintenance_frequency": "asNeeded", "progress": "completed"},
        "constraints": [
            {"type": "access", "restriction_code": "unrestricted"},
            {
                "type": "usage",
                "restriction_code": "license",
                "statement": "This information is licensed under the Open Government Licence (OGL 3.0). To view this licence, visit https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/.",
                "href": "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
            },
        ],
        "language": "eng",
        "extents": [
            {
                "identifier": "bounding",
                "geographic": {
                    "bounding_box": {
                        "west_longitude": -180.0,
                        "east_longitude": 180.0,
                        "south_latitude": -90.0,
                        "north_latitude": -60.0,
                    }
                },
            }
        ],
        "domain_consistency": [_appendix_1_v1],
    },
}

_minimal_product_v1_alt_id = "4308fc21-5999-48ea-918e-9a4c855fa944"
minimal_product_v1_alt = deepcopy(minimal_product_v1)
minimal_product_v1_alt["file_identifier"] = _minimal_product_v1_alt_id
minimal_product_v1_alt["identification"]["identifiers"][0]["identifier"] = _minimal_product_v1_alt_id
minimal_product_v1_alt["identification"]["identifiers"][0]["href"] = (
    f"https://data.bas.ac.uk/items/{_minimal_product_v1_alt_id}"
)
minimal_product_v1_alt["identification"]["domain_consistency"][0] = _appendix_1_v1_alt

configs_v1_all = {
    "minimal_product_v1": minimal_product_v1,
    "minimal_collection_v1": minimal_collection_v1,
    "minimal_product_v1_alt": minimal_product_v1_alt,
}

_minimal_resource_v2_id = "f9557951-30c7-4ab1-bb25-79a552d2c53d"
minimal_resource_v2 = {
    "$schema": "https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v4.json",
    "file_identifier": _minimal_resource_v2_id,
    "metadata": {
        "contacts": [{**_appendix_2, "role": ["pointOfContact"]}],
        "date_stamp": datetime.date(2024, 10, 3),
    },
    "hierarchy_level": "product",
    "identification": {
        "title": {"value": "Test resource record super-type with minimal MAGIC Discovery Profile properties"},
        "dates": {
            "creation": {"date": datetime.date(2024, 9, 14)},
        },
        "edition": "1",
        "identifiers": [
            {
                "identifier": _minimal_resource_v2_id,
                "href": f"https://data.bas.ac.uk/items/{_minimal_resource_v2_id}",
                "namespace": "data.bas.ac.uk",
            }
        ],
        "abstract": "An example product to verify resource super-type records with the minimal set of properties required by the MAGIC Discovery Profile is handled correctly.\n\nThis record does not include a publication date to test the 'false' branch of the released date conditional schema.",
        "contacts": [
            {**_appendix_2, "role": ["pointOfContact"]},
            {
                "organisation": {
                    "name": "UK Research and Innovation",
                    "href": "https://ror.org/001aqnf71",
                    "title": "ror",
                },
                "role": ["rightsHolder"],
            },
        ],
        "maintenance": {"maintenance_frequency": "asNeeded", "progress": "completed"},
        "constraints": [
            {"type": "access", "restriction_code": "unrestricted"},
            {
                "type": "usage",
                "restriction_code": "license",
                "statement": "This information is licensed under the Open Government Licence (OGL 3.0). To view this licence, visit https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/.",
                "href": "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
            },
        ],
        "language": "eng",
        "extents": [
            {
                "identifier": "bounding",
                "geographic": {
                    "bounding_box": {
                        "west_longitude": -180.0,
                        "east_longitude": 180.0,
                        "south_latitude": -90.0,
                        "north_latitude": -60.0,
                    }
                },
            }
        ],
        "other_citation_details": "Fictitious citation",
        "lineage": {"statement": "This is a fictitious record and has no real origin."},
        "domain_consistency": [_appendix_1_v2],
    },
}

_minimal_container_v2_id = "ccb0dd38-29cd-4973-be7a-2db494db6e99"
minimal_container_v2 = {
    "$schema": "https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v4.json",
    "file_identifier": _minimal_container_v2_id,
    "metadata": {
        "contacts": [{**_appendix_2, "role": ["pointOfContact"]}],
        "date_stamp": datetime.date(2024, 10, 3),
    },
    "hierarchy_level": "collection",
    "identification": {
        "title": {"value": "Test container record super-type with minimal MAGIC Discovery Profile properties"},
        "dates": {
            "creation": {"date": datetime.date(2024, 9, 14)},
            "released": {"date": datetime.datetime(2024, 9, 14, 16, 43, 56, tzinfo=datetime.timezone.utc)},
            "publication": {"date": datetime.datetime(2024, 9, 14, 16, 43, 56, tzinfo=datetime.timezone.utc)},
        },
        "edition": "1",
        "identifiers": [
            {
                "identifier": _minimal_container_v2_id,
                "href": f"https://data.bas.ac.uk/items/{_minimal_container_v2_id}",
                "namespace": "data.bas.ac.uk",
            }
        ],
        "abstract": "An example collection to verify container super-type records with the minimal set of properties required by the MAGIC Discovery Profile is handled correctly.\n\nThis record does include a publication date to test the 'true' branch of the released date conditional schema.",
        "contacts": [
            {**_appendix_2, "role": ["pointOfContact"]},
            {
                "organisation": {
                    "name": "UK Research and Innovation",
                    "href": "https://ror.org/001aqnf71",
                    "title": "ror",
                },
                "role": ["rightsHolder"],
            },
        ],
        "maintenance": {"maintenance_frequency": "asNeeded", "progress": "completed"},
        "constraints": [
            {"type": "access", "restriction_code": "unrestricted"},
            {
                "type": "usage",
                "restriction_code": "license",
                "statement": "This information is licensed under the Open Government Licence (OGL 3.0). To view this licence, visit https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/.",
                "href": "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
            },
        ],
        "language": "eng",
        "extents": [
            {
                "identifier": "bounding",
                "geographic": {
                    "bounding_box": {
                        "west_longitude": -180.0,
                        "east_longitude": 180.0,
                        "south_latitude": -90.0,
                        "north_latitude": -60.0,
                    }
                },
            }
        ],
        "domain_consistency": [_appendix_1_v2],
    },
}

configs_v2_all = {"minimal_resource_v2": minimal_resource_v2, "minimal_container_v2": minimal_container_v2}

configs_all = {**configs_v1_all, **configs_v2_all}
