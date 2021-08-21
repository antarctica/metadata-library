import datetime

from copy import deepcopy

minimal_record = {
    "language": "eng",
    "character_set": "utf-8",
    "hierarchy_level": "dataset",
    "contacts": [{"organisation": {"name": "UK Polar Data Centre"}, "role": ["pointOfContact"]}],
    "date_stamp": datetime.date(2018, 10, 18),
    "resource": {
        "title": {"value": "Test Record"},
        "dates": [{"date": datetime.date(2018, 1, 1), "date_precision": "year", "date_type": "creation"}],
        "abstract": "Test Record for ISO 19115 metadata standard (no profile) with required properties only.",
        "character_set": "utf-8",
        "language": "eng",
        "topics": ["environment", "climatologyMeteorologyAtmosphere"],
        "extent": {
            "geographic": {
                "bounding_box": {
                    "west_longitude": -45.61521,
                    "east_longitude": -27.04976,
                    "south_latitude": -68.1511,
                    "north_latitude": -54.30761,
                }
            }
        },
    },
}

minimal_record_with_required_doi_citation = deepcopy(minimal_record)  # type: dict
minimal_record_with_required_doi_citation["resource"]["constraints"] = {
    "usage": [
        {"restriction_code": "otherRestrictions", "required_citation": {"doi": "https://doi.org/10.7939/R3QZ22K64"}}
    ]
}

# noinspection DuplicatedCode,HttpUrlsUsage
base_simple_record = {
    "language": "eng",
    "character_set": "utf-8",
    "hierarchy_level": "dataset",
    "contacts": [
        {
            "organisation": {"name": "UK Polar Data Centre"},
            "role": ["pointOfContact"],
            "phone": "+44 (0)1223 221400",
            "address": {
                "delivery_point": "British Antarctic Survey, High Cross, Madingley Road",
                "city": "Cambridge",
                "administrative_area": "Cambridgeshire",
                "postal_code": "CB3 0ET",
                "country": "United Kingdom",
            },
            "email": "polardatacentre@bas.ac.uk",
        }
    ],
    "date_stamp": datetime.date(2018, 10, 18),
    "resource": {
        "title": {"value": "Test Record"},
        "dates": [
            {"date": datetime.date(2018, 1, 1), "date_precision": "year", "date_type": "creation"},
            {
                "date": datetime.datetime(2018, 10, 8, 14, 40, 44, tzinfo=datetime.timezone.utc),
                "date_type": "publication",
            },
        ],
        "abstract": "Test Record for ISO 19115 metadata standard (no profile) with simple baseline properties only. In this context baseline properties are those that are required, or have default values. Values in this record are non-complex, meaning they are simple character strings rather than anchors. Authorities are not included in elements that support citations.",
        "character_set": "utf-8",
        "language": "eng",
        "topics": ["environment", "climatologyMeteorologyAtmosphere"],
        "extent": {
            "geographic": {
                "bounding_box": {
                    "west_longitude": -45.61521,
                    "east_longitude": -27.04976,
                    "south_latitude": -68.1511,
                    "north_latitude": -54.30761,
                }
            },
            "temporal": {
                "period": {"start": datetime.datetime(2018, 9, 14, 0, 0), "end": datetime.datetime(2018, 9, 15, 0, 0)}
            },
        },
        "credit": "No credit.",
        "contacts": [
            {
                "individual": {"name": "Watson, Constance"},
                "organisation": {"name": "British Antarctic Survey"},
                "email": "conwat@bas.ac.uk",
                "role": ["author"],
            },
            {
                "organisation": {"name": "UK Polar Data Centre"},
                "phone": "+44 (0)1223 221400",
                "address": {
                    "delivery_point": "British Antarctic Survey, High Cross, Madingley Road",
                    "city": "Cambridge",
                    "administrative_area": "Cambridgeshire",
                    "postal_code": "CB3 0ET",
                    "country": "United Kingdom",
                },
                "email": "polardatacentre@bas.ac.uk",
                "role": ["pointOfContact", "custodian", "publisher", "distributor"],
            },
        ],
        "maintenance": {"maintenance_frequency": "asNeeded", "progress": "completed"},
        "keywords": [{"terms": [{"term": "Atmospheric conditions"}], "type": "theme"}],
        "constraints": {
            "access": [{"restriction_code": "otherRestrictions"}],
            "usage": [
                {
                    "copyright_licence": {
                        "statement": "This information is licensed under the Open Government Licence v3.0. To view this licence, visit http://www.nationalarchives.gov.uk/doc/open-government-licence/"
                    }
                }
            ],
        },
        "supplemental_information": "It is recommended that careful attention be paid to the contents of any data, and that the author be contacted with any questions regarding appropriate use. If you find any errors or omissions, please report them to polardatacentre@bas.ac.uk.",
        "spatial_representation_type": "textTable",
        "formats": [{"format": "netCDF"}],
        "transfer_options": [
            {
                "online_resource": {
                    "href": "https://ramadda.data.bas.ac.uk/repository/entry/show?entryid=b1a7d1b5-c419-41e7-9178-b1ffd76d5371",
                    "title": "Get Data",
                    "description": "Download measurement data",
                    "function": "download",
                }
            }
        ],
        "lineage": "Example lineage statement",
    },
    "file_identifier": "b1a7d1b5-c419-41e7-9178-b1ffd76d5371",
    "maintenance": {"maintenance_frequency": "asNeeded", "progress": "completed"},
    "metadata_standard": {"name": "ISO 19115", "version": "1.0"},
    "reference_system_info": {"code": {"value": "urn:ogc:def:crs:EPSG::4326"}},
}

# noinspection DuplicatedCode,HttpUrlsUsage
base_complex_record = {
    "language": "eng",
    "character_set": "utf-8",
    "hierarchy_level": "dataset",
    "contacts": [
        {
            "organisation": {"name": "UK Polar Data Centre", "href": "https://ror.org/01rhff309", "title": "ror"},
            "role": ["pointOfContact"],
            "phone": "+44 (0)1223 221400",
            "address": {
                "delivery_point": "British Antarctic Survey, High Cross, Madingley Road",
                "city": "Cambridge",
                "administrative_area": "Cambridgeshire",
                "postal_code": "CB3 0ET",
                "country": "United Kingdom",
            },
            "email": "polardatacentre@bas.ac.uk",
            "online_resource": {
                "href": "https://www.bas.ac.uk/team/business-teams/information-services/uk-polar-data-centre/",
                "function": "information",
            },
        }
    ],
    "date_stamp": datetime.date(2018, 10, 18),
    "resource": {
        "title": {"value": "Test Record"},
        "dates": [
            {"date": datetime.date(2018, 1, 1), "date_precision": "year", "date_type": "creation"},
            {
                "date": datetime.datetime(2018, 10, 8, 14, 40, 44, tzinfo=datetime.timezone.utc),
                "date_type": "publication",
            },
        ],
        "abstract": "Test Record for ISO 19115 metadata standard (no profile) with complex baseline properties only. In this context baseline properties are those that are required, or have default values. Values in this record are complex, meaning they use anchors where relevant rather than simple character strings. Authorities are included in elements that support citations.",
        "character_set": "utf-8",
        "language": "eng",
        "topics": ["environment", "climatologyMeteorologyAtmosphere"],
        "extent": {
            "geographic": {
                "bounding_box": {
                    "west_longitude": -45.61521,
                    "east_longitude": -27.04976,
                    "south_latitude": -68.1511,
                    "north_latitude": -54.30761,
                }
            },
            "temporal": {
                "period": {"start": datetime.datetime(2018, 9, 14, 0, 0), "end": datetime.datetime(2018, 9, 15, 0, 0)}
            },
        },
        "credit": "No credit.",
        "contacts": [
            {
                "individual": {
                    "name": "Watson, Constance",
                    "href": "https://sandbox.orcid.org/0000-0001-8373-6934",
                    "title": "orcid",
                },
                "organisation": {"name": "British Antarctic Survey"},
                "email": "conwat@bas.ac.uk",
                "role": ["author"],
                "online_resource": {
                    "href": "https://sandbox.orcid.org/0000-0001-8373-6934",
                    "title": "ORCID record",
                    "description": "ORCID is an open, non-profit, community-driven effort to create and maintain a registry of unique researcher identifiers and a transparent method of linking research activities and outputs to these identifiers.",
                    "function": "information",
                },
            },
            {
                "organisation": {"name": "UK Polar Data Centre", "href": "https://ror.org/01rhff309", "title": "ror"},
                "phone": "+44 (0)1223 221400",
                "address": {
                    "delivery_point": "British Antarctic Survey, High Cross, Madingley Road",
                    "city": "Cambridge",
                    "administrative_area": "Cambridgeshire",
                    "postal_code": "CB3 0ET",
                    "country": "United Kingdom",
                },
                "email": "polardatacentre@bas.ac.uk",
                "role": ["pointOfContact", "custodian", "publisher", "distributor"],
                "online_resource": {
                    "href": "https://www.bas.ac.uk/team/business-teams/information-services/uk-polar-data-centre/",
                    "function": "information",
                },
            },
        ],
        "maintenance": {"maintenance_frequency": "asNeeded", "progress": "completed"},
        "keywords": [
            {
                "terms": [
                    {"term": "Atmospheric conditions", "href": "https://www.eionet.europa.eu/gemet/en/inspire-theme/ac"}
                ],
                "type": "theme",
                "thesaurus": {
                    "title": {
                        "value": "General Multilingual Environmental Thesaurus - INSPIRE themes",
                        "href": "http://www.eionet.europa.eu/gemet/inspire_themes",
                    },
                    "dates": [{"date": datetime.date(2018, 8, 16), "date_type": "publication"}],
                    "edition": "4.1.2",
                    "contact": {
                        "organisation": {
                            "name": "European Environment Information and Observation Network (EIONET), European Environment Agency (EEA)"
                        },
                        "email": "helpdesk@eionet.europa.eu",
                        "online_resource": {
                            "href": "https://www.eionet.europa.eu/gemet/en/themes/",
                            "title": "General Multilingual Environmental Thesaurus (GEMET) themes",
                            "function": "information",
                        },
                        "role": ["publisher"],
                    },
                },
            }
        ],
        "constraints": {
            "access": [{"restriction_code": "otherRestrictions"}],
            "usage": [
                {
                    "copyright_licence": {
                        "statement": "This information is licensed under the Open Government Licence v3.0. To view this licence, visit http://www.nationalarchives.gov.uk/doc/open-government-licence/",
                        "code": "OGL-UK-3.0",
                        "href": "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
                    }
                }
            ],
        },
        "supplemental_information": "It is recommended that careful attention be paid to the contents of any data, and that the author be contacted with any questions regarding appropriate use. If you find any errors or omissions, please report them to polardatacentre@bas.ac.uk.",
        "spatial_representation_type": "textTable",
        "formats": [
            {
                "format": "netCDF",
                "href": "https://gcmdservices.gsfc.nasa.gov/kms/concept/2b192915-32a8-4b68-a720-8ca8a84f04ca",
            }
        ],
        "transfer_options": [
            {
                "online_resource": {
                    "href": "https://ramadda.data.bas.ac.uk/repository/entry/show?entryid=b1a7d1b5-c419-41e7-9178-b1ffd76d5371",
                    "title": "Get Data",
                    "description": "Download measurement data",
                    "function": "download",
                }
            }
        ],
        "lineage": "Example lineage statement",
    },
    "file_identifier": "b1a7d1b5-c419-41e7-9178-b1ffd76d5371",
    "maintenance": {"maintenance_frequency": "asNeeded", "progress": "completed"},
    "metadata_standard": {"name": "ISO 19115", "version": "1.0"},
    "reference_system_info": {
        "code": {"value": "urn:ogc:def:crs:EPSG::4326", "href": "http://www.opengis.net/def/crs/EPSG/0/4326"},
        "version": "6.18.3",
        "authority": {
            "title": {"value": "European Petroleum Survey Group (EPSG) Geodetic Parameter Registry"},
            "dates": [{"date": datetime.date(2008, 11, 12), "date_type": "publication"}],
            "contact": {
                "organisation": {"name": "European Petroleum Survey Group"},
                "email": "EPSGadministrator@iogp.org",
                "online_resource": {"href": "https://www.epsg-registry.org/", "function": "information"},
                "role": ["publisher"],
            },
        },
    },
}

# noinspection DuplicatedCode,HttpUrlsUsage
complete_record = {
    "language": "eng",
    "character_set": "utf-8",
    "hierarchy_level": "dataset",
    "contacts": [
        {
            "organisation": {"name": "UK Polar Data Centre", "href": "https://ror.org/01rhff309", "title": "ror"},
            "role": ["pointOfContact"],
            "phone": "+44 (0)1223 221400",
            "address": {
                "delivery_point": "British Antarctic Survey, High Cross, Madingley Road",
                "city": "Cambridge",
                "administrative_area": "Cambridgeshire",
                "postal_code": "CB3 0ET",
                "country": "United Kingdom",
            },
            "email": "polardatacentre@bas.ac.uk",
            "online_resource": {
                "href": "https://www.bas.ac.uk/team/business-teams/information-services/uk-polar-data-centre/",
                "function": "information",
            },
        }
    ],
    "date_stamp": datetime.date(2018, 10, 18),
    "resource": {
        "title": {"value": "Test Record"},
        "dates": [
            {"date": datetime.date(2018, 1, 1), "date_precision": "year", "date_type": "creation"},
            {"date": datetime.date(2018, 1, 1), "date_precision": "year", "date_type": "revision"},
            {
                "date": datetime.datetime(2018, 10, 8, 14, 40, 44, tzinfo=datetime.timezone.utc),
                "date_type": "publication",
            },
            {"date": datetime.datetime(2018, 10, 8, 14, 40, 44, tzinfo=datetime.timezone.utc), "date_type": "released"},
        ],
        "abstract": "Test Record for ISO 19115 metadata standard (no profile) with properties that could typically be included in a record. This does not mean all properties permitted the standard are included, as these are too numerous. Values in this record are complex, meaning they use anchors where relevant rather than simple character strings. Authorities are included in elements that support citations. Identifiers in this record are fake.",
        "character_set": "utf-8",
        "language": "eng",
        "topics": ["environment", "climatologyMeteorologyAtmosphere"],
        "extent": {
            "geographic": {
                "bounding_box": {
                    "west_longitude": -45.61521,
                    "east_longitude": -27.04976,
                    "south_latitude": -68.1511,
                    "north_latitude": -54.30761,
                }
            },
            "temporal": {
                "period": {"start": datetime.datetime(2018, 9, 14, 0, 0), "end": datetime.datetime(2018, 9, 15, 0, 0)}
            },
            "vertical": {
                "minimum": 20.0,
                "maximum": 40.0,
                "identifier": "ogp-crs-5714",
                "code": "urn:ogc:def:crs:EPSG::5714",
                "name": "MSL height",
                "remarks": "Not specific to any location or epoch.",
                "scope": "Hydrography.",
                "domain_of_validity": {"href": "urn:ogc:def:area:EPSG::1262"},
                "vertical_cs": {"href": "urn:ogc:def:cs:EPSG::6498"},
                "vertical_datum": {"href": "urn:ogc:def:datum:EPSG::5100"},
            },
        },
        "credit": "No credit.",
        "contacts": [
            {
                "individual": {
                    "name": "Watson, Constance",
                    "href": "https://sandbox.orcid.org/0000-0001-8373-6934",
                    "title": "orcid",
                },
                "organisation": {"name": "British Antarctic Survey"},
                "email": "conwat@bas.ac.uk",
                "role": ["author"],
                "online_resource": {
                    "href": "https://sandbox.orcid.org/0000-0001-8373-6934",
                    "title": "ORCID record",
                    "description": "ORCID is an open, non-profit, community-driven effort to create and maintain a registry of unique researcher identifiers and a transparent method of linking research activities and outputs to these identifiers.",
                    "function": "information",
                },
            },
            {
                "individual": {
                    "name": "Cinnamon, John",
                    "href": "https://sandbox.orcid.org/0000-0001-5652-1129",
                    "title": "orcid",
                },
                "organisation": {"name": "British Antarctic Survey"},
                "email": "conwat@bas.ac.uk",
                "online_resource": {
                    "href": "https://sandbox.orcid.org/0000-0001-5652-1129",
                    "title": "ORCID record",
                    "description": "ORCID is an open, non-profit, community-driven effort to create and maintain a registry of unique researcher identifiers and a transparent method of linking research activities and outputs to these identifiers.",
                    "function": "information",
                },
                "role": ["collaborator"],
            },
            {
                "organisation": {"name": "UK Polar Data Centre", "href": "https://ror.org/01rhff309", "title": "ror"},
                "phone": "+44 (0)1223 221400",
                "address": {
                    "delivery_point": "British Antarctic Survey, High Cross, Madingley Road",
                    "city": "Cambridge",
                    "administrative_area": "Cambridgeshire",
                    "postal_code": "CB3 0ET",
                    "country": "United Kingdom",
                },
                "email": "polardatacentre@bas.ac.uk",
                "role": ["pointOfContact", "custodian", "publisher", "distributor"],
                "online_resource": {
                    "href": "https://www.bas.ac.uk/team/business-teams/information-services/uk-polar-data-centre/",
                    "function": "information",
                },
            },
            {
                "organisation": {"name": "Mapping and Geograpgic Information Centre, British Antarctic Survey"},
                "phone": "+44 (0)1223 221400",
                "address": {
                    "delivery_point": "British Antarctic Survey, High Cross, Madingley Road",
                    "city": "Cambridge",
                    "administrative_area": "Cambridgeshire",
                    "postal_code": "CB3 0ET",
                    "country": "United Kingdom",
                },
                "email": "magic@bas.ac.uk",
                "role": ["distributor"],
            },
        ],
        "maintenance": {"maintenance_frequency": "asNeeded", "progress": "completed"},
        "keywords": [
            {
                "terms": [
                    {"term": "Atmospheric conditions", "href": "https://www.eionet.europa.eu/gemet/en/inspire-theme/ac"}
                ],
                "type": "theme",
                "thesaurus": {
                    "title": {
                        "value": "General Multilingual Environmental Thesaurus - INSPIRE themes",
                        "href": "http://www.eionet.europa.eu/gemet/inspire_themes",
                    },
                    "dates": [{"date": datetime.date(2018, 8, 16), "date_type": "publication"}],
                    "edition": "4.1.2",
                    "contact": {
                        "organisation": {
                            "name": "European Environment Information and Observation Network (EIONET), European Environment Agency (EEA)"
                        },
                        "email": "helpdesk@eionet.europa.eu",
                        "online_resource": {
                            "href": "https://www.eionet.europa.eu/gemet/en/themes/",
                            "title": "General Multilingual Environmental Thesaurus (GEMET) themes",
                            "function": "information",
                        },
                        "role": ["publisher"],
                    },
                },
            }
        ],
        "constraints": {
            "access": [{"restriction_code": "otherRestrictions", "statement": "Custom access restrictions statement"}],
            "usage": [
                {
                    "copyright_licence": {
                        "statement": "This information is licensed under the Open Government Licence v3.0. To view this licence, visit http://www.nationalarchives.gov.uk/doc/open-government-licence/",
                        "code": "OGL-UK-3.0",
                        "href": "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
                    }
                },
                {
                    "required_citation": {
                        "statement": 'Cite this information as: "Campbell, S. (2014). Auster Antarctic aircraft. University of Alberta Libraries. https://doi.org/10.7939/r3qz22k64"'
                    }
                },
                {"statement": "Custom use limitations statement"},
            ],
        },
        "supplemental_information": "It is recommended that careful attention be paid to the contents of any data, and that the author be contacted with any questions regarding appropriate use. If you find any errors or omissions, please report them to polardatacentre@bas.ac.uk.",
        "spatial_representation_type": "textTable",
        "formats": [
            {
                "format": "netCDF",
                "href": "https://gcmdservices.gsfc.nasa.gov/kms/concept/2b192915-32a8-4b68-a720-8ca8a84f04ca",
            }
        ],
        "transfer_options": [
            {
                "online_resource": {
                    "href": "https://ramadda.data.bas.ac.uk/repository/entry/show?entryid=b1a7d1b5-c419-41e7-9178-b1ffd76d5371",
                    "title": "Get Data",
                    "description": "Download measurement data",
                    "function": "download",
                },
                "size": {"unit": "MB", "magnitude": 40.0},
            },
            {
                "online_resource": {
                    "href": "https://www.bodc.ac.uk/data/bodc_database/nodb/data_collection/6618/",
                    "title": "View Information",
                    "description": "Download background information and context",
                    "function": "information",
                }
            },
        ],
        "lineage": "Example lineage statement",
        "edition": "2",
        "identifiers": [
            {
                "identifier": "https://doi.org/10.5072/r3qz22k64",
                "href": "https://doi.org/10.5072/r3qz22k64",
                "title": "doi",
            },
            {
                "identifier": "NE/E007895/1",
                "href": "https://gtr.ukri.org/projects?ref=NE%2FE007895%2F1",
                "title": "award",
            },
        ],
    },
    "file_identifier": "b1a7d1b5-c419-41e7-9178-b1ffd76d5371",
    "maintenance": {"maintenance_frequency": "asNeeded", "progress": "completed"},
    "metadata_standard": {"name": "ISO 19115", "version": "1.0"},
    "reference_system_info": {
        "code": {"value": "urn:ogc:def:crs:EPSG::4326", "href": "http://www.opengis.net/def/crs/EPSG/0/4326"},
        "version": "6.18.3",
        "authority": {
            "title": {"value": "European Petroleum Survey Group (EPSG) Geodetic Parameter Registry"},
            "dates": [{"date": datetime.date(2008, 11, 12), "date_type": "publication"}],
            "contact": {
                "organisation": {"name": "European Petroleum Survey Group"},
                "email": "EPSGadministrator@iogp.org",
                "online_resource": {"href": "https://www.epsg-registry.org/", "function": "information"},
                "role": ["publisher"],
            },
        },
    },
}

configs_safe = {
    "minimal": minimal_record,
    "base-simple": base_simple_record,
    "base-complex": base_complex_record,
    "complete": complete_record,
}
configs_unsafe = {
    "minimal-required-doi-citation": minimal_record_with_required_doi_citation,
}
configs_all = {**configs_safe, **configs_unsafe}
