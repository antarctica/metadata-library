import datetime

minimal_record_v2 = {
    "hierarchy_level": "dataset",
    "metadata": {
        "language": "eng",
        "character_set": "utf-8",
        "contacts": [{"organisation": {"name": "UK Polar Data Centre"}, "role": ["pointOfContact"]}],
        "date_stamp": datetime.date(2018, 10, 18),
    },
    "identification": {
        "title": {"value": "Test Record"},
        "dates": {"creation": {"date": datetime.date(2018, 1, 1), "date_precision": "year"}},
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

# noinspection DuplicatedCode
base_simple_record_v2 = {
    "file_identifier": "b1a7d1b5-c419-41e7-9178-b1ffd76d5371",
    "hierarchy_level": "dataset",
    "metadata": {
        "language": "eng",
        "character_set": "utf-8",
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
        "maintenance": {"maintenance_frequency": "asNeeded", "progress": "completed"},
        "metadata_standard": {"name": "ISO 19115", "version": "1.0"},
    },
    "reference_system_info": {"code": {"value": "urn:ogc:def:crs:EPSG::4326"}},
    "identification": {
        "title": {"value": "Test Record"},
        "dates": {
            "creation": {"date": datetime.date(2018, 1, 1), "date_precision": "year"},
            "publication": {"date": datetime.datetime(2018, 10, 8, 14, 40, 44, tzinfo=datetime.timezone.utc)},
        },
        "abstract": "Test Record for ISO 19115 metadata standard (no profile) with simple baseline properties only. In this context baseline properties are those that are required, or have default values. Values in this record are non-complex, meaning they are simple character strings rather than anchors. Authorities are not included in elements that support citations.",
        "purpose": "Fictitious test record (ISO 19115, no profile, simple).",
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
                "period": {
                    "start": {"date": datetime.date(2018, 1, 1), "date_precision": "year"},
                    "end": {"date": datetime.datetime(2018, 9, 15, 0, 0)},
                }
            },
        },
        "credit": "No credit.",
        "status": "completed",
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
                "role": ["pointOfContact", "custodian", "publisher"],
            },
        ],
        "maintenance": {"maintenance_frequency": "asNeeded", "progress": "completed"},
        "resource_formats": [
            {"format": "GeoTIFF"},
        ],
        "keywords": [{"terms": [{"term": "Atmospheric conditions"}], "type": "theme"}],
        "constraints": [
            {
                "type": "usage",
                "restriction_code": "license",
                "statement": "This information is licensed under the Open Government Licence v3.0. To view this licence, visit http://www.nationalarchives.gov.uk/doc/open-government-licence/",
            }
        ],
        "supplemental_information": "It is recommended that careful attention be paid to the contents of any data, and that the author be contacted with any questions regarding appropriate use. If you find any errors or omissions, please report them to polardatacentre@bas.ac.uk.",
        "spatial_representation_type": "textTable",
        "lineage": "Example lineage statement",
    },
    "distribution": [
        {
            "distributor": {
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
                "role": ["distributor"],
            },
            "distribution_options": [
                {
                    "format": {"format": "netCDF"},
                    "transfer_option": {
                        "online_resource": {
                            "href": "https://ramadda.data.bas.ac.uk/repository/entry/show?entryid=b1a7d1b5-c419-41e7-9178-b1ffd76d5371",
                            "title": "Get Data",
                            "description": "Download measurement data",
                            "protocol": "WWW:LINK-1.0-http--link",
                            "function": "download",
                        }
                    },
                }
            ],
        }
    ],
}

# noinspection DuplicatedCode
base_complex_record_v2 = {
    "file_identifier": "b1a7d1b5-c419-41e7-9178-b1ffd76d5371",
    "hierarchy_level": "dataset",
    "metadata": {
        "language": "eng",
        "character_set": "utf-8",
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
        "maintenance": {"maintenance_frequency": "asNeeded", "progress": "completed"},
        "metadata_standard": {"name": "ISO 19115", "version": "1.0"},
    },
    "reference_system_info": {
        "code": {"value": "urn:ogc:def:crs:EPSG::4326", "href": "http://www.opengis.net/def/crs/EPSG/0/4326"},
        "version": "6.18.3",
        "authority": {
            "title": {"value": "European Petroleum Survey Group (EPSG) Geodetic Parameter Registry"},
            "dates": {"publication": {"date": datetime.date(2008, 11, 12)}},
            "contact": {
                "organisation": {"name": "European Petroleum Survey Group"},
                "email": "EPSGadministrator@iogp.org",
                "online_resource": {"href": "https://www.epsg-registry.org/", "function": "information"},
                "role": ["publisher"],
            },
        },
    },
    "identification": {
        "title": {"value": "Test Record"},
        "dates": {
            "creation": {"date": datetime.date(2018, 1, 1), "date_precision": "year"},
            "publication": {"date": datetime.datetime(2018, 10, 8, 14, 40, 44, tzinfo=datetime.timezone.utc)},
        },
        "abstract": "Test Record for ISO 19115 metadata standard (no profile) with complex baseline properties only. In this context baseline properties are those that are required, or have default values. Values in this record are complex, meaning they use anchors where relevant rather than simple character strings. Authorities are included in elements that support citations.",
        "purpose": "Fictitious test record (ISO 19115, no profile, complex).",
        "character_set": "utf-8",
        "language": "eng",
        "topics": ["environment", "climatologyMeteorologyAtmosphere"],
        "extent": {
            "geographic": {
                "identifier": {
                    "identifier": "ANTARCTICA",
                    "href": "https://gcmdservices.gsfc.nasa.gov/kms/concept/70fb5a3b-35b1-4048-a8be-56a0d865281c",
                    "namespace": "gcmd-keywords-location",
                },
            },
            "temporal": {
                "period": {
                    "start": {"date": datetime.date(2018, 1, 1), "date_precision": "year"},
                    "end": {"date": datetime.datetime(2018, 9, 15, 0, 0)},
                }
            },
        },
        "credit": "No credit.",
        "status": "completed",
        "contacts": [
            {
                "individual": {
                    "name": "Watson, Constance",
                    "href": "https://sandbox.orcid.org/0000-0001-8373-6934",
                    "title": "orcid",
                },
                "organisation": {"name": "British Antarctic Survey"},
                "position": "Atmospheric Chemist",
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
                "role": ["pointOfContact", "custodian", "publisher"],
                "online_resource": {
                    "href": "https://www.bas.ac.uk/team/business-teams/information-services/uk-polar-data-centre/",
                    "function": "information",
                },
            },
        ],
        "maintenance": {"maintenance_frequency": "asNeeded", "progress": "completed"},
        "resource_formats": [
            {
                "format": "GeoTIFF",
                "version": "2",
            },
        ],
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
                    "dates": {"publication": {"date": datetime.date(2018, 8, 16)}},
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
        "constraints": [
            {
                "type": "usage",
                "restriction_code": "license",
                "statement": "This information is licensed under the Open Government Licence v3.0. To view this licence, visit http://www.nationalarchives.gov.uk/doc/open-government-licence/",
                "href": "http://www.nationalarchives.gov.uk/doc/open-government-licence/",
            }
        ],
        "aggregations": [
            {
                "association_type": "crossReference",
                "identifier": {
                    "identifier": "https://doi.org/10.5072/mj04wb80f",
                    "href": "https://doi.org/10.5072/mj04wb80f",
                    "namespace": "doi",
                },
            }
        ],
        "supplemental_information": "It is recommended that careful attention be paid to the contents of any data, and that the author be contacted with any questions regarding appropriate use. If you find any errors or omissions, please report them to polardatacentre@bas.ac.uk.",
        "spatial_representation_type": "textTable",
        "lineage": "Example lineage statement",
    },
    "distribution": [
        {
            "distributor": {
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
                "role": ["distributor"],
                "online_resource": {
                    "href": "https://www.bas.ac.uk/team/business-teams/information-services/uk-polar-data-centre/",
                    "function": "information",
                },
            },
            "distribution_options": [
                {
                    "format": {
                        "format": "netCDF",
                        "href": "https://gcmdservices.gsfc.nasa.gov/kms/concept/2b192915-32a8-4b68-a720-8ca8a84f04ca",
                    },
                    "transfer_option": {
                        "online_resource": {
                            "href": "https://ramadda.data.bas.ac.uk/repository/entry/show?entryid=b1a7d1b5-c419-41e7-9178-b1ffd76d5371",
                            "title": "Get Data",
                            "description": "Download measurement data",
                            "protocol": "WWW:LINK-1.0-http--link",
                            "function": "download",
                        }
                    },
                }
            ],
        }
    ],
}

# noinspection DuplicatedCode,HttpUrlsUsage
complete_record_v2 = {
    "file_identifier": "b1a7d1b5-c419-41e7-9178-b1ffd76d5371",
    "hierarchy_level": "dataset",
    "metadata": {
        "language": "eng",
        "character_set": "utf-8",
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
        "maintenance": {"maintenance_frequency": "asNeeded", "progress": "completed"},
        "metadata_standard": {"name": "ISO 19115", "version": "1.0"},
    },
    "reference_system_info": {
        "code": {"value": "urn:ogc:def:crs:EPSG::4326", "href": "http://www.opengis.net/def/crs/EPSG/0/4326"},
        "version": "6.18.3",
        "authority": {
            "title": {"value": "European Petroleum Survey Group (EPSG) Geodetic Parameter Registry"},
            "dates": {"publication": {"date": datetime.date(2008, 11, 12)}},
            "contact": {
                "organisation": {"name": "European Petroleum Survey Group"},
                "email": "EPSGadministrator@iogp.org",
                "online_resource": {"href": "https://www.epsg-registry.org/", "function": "information"},
                "role": ["publisher"],
            },
        },
    },
    "identification": {
        "title": {"value": "Test Record"},
        "dates": {
            "creation": {"date": datetime.date(2018, 1, 1), "date_precision": "year"},
            "revision": {"date": datetime.date(2018, 1, 1), "date_precision": "year"},
            "publication": {"date": datetime.datetime(2018, 10, 8, 14, 40, 44, tzinfo=datetime.timezone.utc)},
            "released": {"date": datetime.datetime(2018, 10, 8, 14, 40, 44, tzinfo=datetime.timezone.utc)},
        },
        "abstract": "Test Record for ISO 19115 metadata standard (no profile) with properties that could typically be included in a record. This does not mean all properties permitted the standard are included, as these are too numerous. Values in this record are complex, meaning they use anchors where relevant rather than simple character strings. Authorities are included in elements that support citations. Identifiers in this record are fake.",
        "purpose": "Fictitious test record (ISO 19115, no profile, complete).",
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
                "period": {
                    "start": {"date": datetime.datetime(2018, 3, 15, 0, 0)},
                    "end": {"date": datetime.date(2018, 3, 1), "date_precision": "month"},
                }
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
        "status": "completed",
        "contacts": [
            {
                "individual": {
                    "name": "Watson, Constance",
                    "href": "https://sandbox.orcid.org/0000-0001-8373-6934",
                    "title": "orcid",
                },
                "organisation": {"name": "British Antarctic Survey"},
                "position": "Atmospheric Chemist",
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
                "position": "Friend",
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
                "role": ["pointOfContact", "custodian", "publisher"],
                "online_resource": {
                    "href": "https://www.bas.ac.uk/team/business-teams/information-services/uk-polar-data-centre/",
                    "function": "information",
                },
            },
        ],
        "maintenance": {"maintenance_frequency": "asNeeded", "progress": "completed"},
        "graphic_overviews": [
            {
                "identifier": "thumbnail",
                "href": "https://example.com/img/thumbnail.jpeg",
                "description": "General overview of resource",
                "mime_type": "image/jpeg",
            },
            {
                "identifier": "cover-front",
                "href": "https://example.com/img/cover-front.jpeg",
                "description": "Front cover of resource",
                "mime_type": "image/jpeg",
            },
            {
                "identifier": "cover-back",
                "href": "https://example.com/img/cover-back.jpeg",
                "description": "Back cover of resource",
                "mime_type": "image/jpeg",
            },
        ],
        "resource_formats": [
            {
                "format": "GeoTIFF",
                "version": "2",
                "amendment_number": "1.4",
                "specification": "Final",
                "file_decompression_technique": "ZIP",
            },
            {
                "format": "NetCDF",
                "version": "4",
                "amendment_number": "1.1",
                "specification": "NCEI NetCDF Templates v2.0",
                "file_decompression_technique": "ZIP",
            },
        ],
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
                    "dates": {"publication": {"date": datetime.date(2018, 8, 16)}},
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
        "constraints": [
            {"type": "access", "restriction_code": "unrestricted"},
            {
                "type": "usage",
                "restriction_code": "license",
                "statement": "This information is licensed under the Open Government Licence v3.0. To view this licence, visit http://www.nationalarchives.gov.uk/doc/open-government-licence/",
                "href": "http://www.nationalarchives.gov.uk/doc/open-government-licence/",
            },
            {
                "type": "usage",
                "restriction_code": "otherRestrictions",
                "statement": 'You must cite this information as: "Campbell, S. (2014). Auster Antarctic aircraft. University of Alberta Libraries. https://doi.org/10.7939/r3qz22k64"',
                "href": "https://doi.org/10.7939/r3qz22k64",
            },
            {"type": "access", "restriction_code": "otherRestrictions", "statement": "constraint without href"},
            {
                "type": "access",
                "restriction_code": "otherRestrictions",
                "href": "http://example.com/#constraint-without-statement",
            },
        ],
        "aggregations": [
            {
                "association_type": "crossReference",
                "identifier": {
                    "identifier": "https://doi.org/10.5072/mj04wb80f",
                    "href": "https://doi.org/10.5072/mj04wb80f",
                    "namespace": "doi",
                },
            },
            {
                "association_type": "isComposedOf",
                "initiative_type": "collection",
                "identifier": {
                    "identifier": "https://doi.org/10.5072/erve7txmv",
                    "href": "https://doi.org/10.5072/erve7txmv",
                    "namespace": "doi",
                },
            },
        ],
        "supplemental_information": "It is recommended that careful attention be paid to the contents of any data, and that the author be contacted with any questions regarding appropriate use. If you find any errors or omissions, please report them to polardatacentre@bas.ac.uk.",
        "spatial_representation_type": "textTable",
        "spatial_resolution": 1000000,
        "lineage": "Example lineage statement",
        "edition": "2",
        "other_citation_details": "Author, A., Author, B., & Author, C. (2022). The title (Version 1.0) [Data set]. Publisher. https://doi.org/the-doi",
        "identifiers": [
            {
                "identifier": "https://doi.org/10.5072/r3qz22k64",
                "href": "https://doi.org/10.5072/r3qz22k64",
                "namespace": "doi",
            },
            {
                "identifier": "NE/E007895/1",
                "href": "https://gtr.ukri.org/projects?ref=NE%2FE007895%2F1",
                "namespace": "award",
            },
        ],
    },
    "distribution": [
        {
            "distributor": {
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
                "role": ["distributor"],
                "online_resource": {
                    "href": "https://www.bas.ac.uk/team/business-teams/information-services/uk-polar-data-centre/",
                    "function": "information",
                },
            },
            "distribution_options": [
                {
                    "format": {
                        "format": "netCDF",
                        "version": "4",
                        "href": "https://gcmdservices.gsfc.nasa.gov/kms/concept/2b192915-32a8-4b68-a720-8ca8a84f04ca",
                        "amendment_number": "1.2",
                        "specification": "Final",
                        "file_decompression_technique": "ZIP",
                    },
                    "transfer_option": {
                        "online_resource": {
                            "href": "https://ramadda.data.bas.ac.uk/repository/entry/show?entryid=b1a7d1b5-c419-41e7-9178-b1ffd76d5371",
                            "title": "Get Data",
                            "description": "Download measurement data",
                            "protocol": "WWW:LINK-1.0-http--link",
                            "function": "download",
                        },
                        "size": {"unit": "MB", "magnitude": 40.0},
                    },
                }
            ],
        },
        {
            "distributor": {
                "organisation": {"name": "Mapping and Geographic Information Centre, British Antarctic Survey"},
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
            "distribution_options": [
                {
                    "format": {
                        "format": "PDF",
                        "version": "1.6",
                        "href": "https://www.iana.org/assignments/media-types/application/pdf",
                    },
                    "transfer_option": {
                        "size": {"unit": "KB", "magnitude": 371},
                        "online_resource": {
                            "href": "https://data.bas.ac.uk/download/1a13e804-ceca-4f7b-9001-6e976872eec0",
                            "title": "PDF",
                            "description": "Download information as an Adobe PDF.",
                            "protocol": "WWW:LINK-1.0-http--link",
                            "function": "download",
                        },
                    },
                },
                {
                    "format": {
                        "format": "PNG",
                        "version": "1",
                        "href": "https://www.iana.org/assignments/media-types/image/png",
                    },
                    "transfer_option": {
                        "size": {"unit": "MB", "magnitude": 2.74},
                        "online_resource": {
                            "href": "https://data.bas.ac.uk/download/e6db2605-f9bd-422a-b864-caa6d69cdcaf",
                            "title": "PNG",
                            "description": "Download information as a PNG image.",
                            "protocol": "WWW:LINK-1.0-http--link",
                            "function": "download",
                        },
                    },
                },
            ],
        },
    ],
}

minimal_record_v3 = minimal_record_v2
base_simple_record_v3 = base_simple_record_v2
base_complex_record_v3 = base_complex_record_v2
complete_record_v3 = complete_record_v2

configs_safe_v2 = {
    "minimal_v2": minimal_record_v2,
    "base-simple_v2": base_simple_record_v2,
    "base-complex_v2": base_complex_record_v2,
    "complete_v2": complete_record_v2,
}
configs_v2_all = {**configs_safe_v2}

configs_safe_v3 = {
    "minimal_v3": minimal_record_v3,
    "base-simple_v3": base_simple_record_v3,
    "base-complex_v3": base_complex_record_v3,
    "complete_v3": complete_record_v3,
}
configs_v3_all = {**configs_safe_v3}

configs_safe_all = {**configs_safe_v2, **configs_safe_v3}
configs_all = {**configs_v2_all, **configs_v3_all}
