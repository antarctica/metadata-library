import datetime

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
_appendix_1 = {
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
        "domain_consistency": [_appendix_1],
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
        "domain_consistency": [_appendix_1],
    },
}

configs_v1_all = {"minimal_product_v1": minimal_product_v1, "minimal_collection_v1": minimal_collection_v1}

configs_all = {**configs_v1_all}
