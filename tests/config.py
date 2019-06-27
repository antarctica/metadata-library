from datetime import datetime, timezone, date

test_standard_minimal_record = {
    'resource': {
        'title': {
            'value': 'Test Record'
        }
    }
}

test_standard_typical_record = {
    'resource': {
        'title': {
            'value': 'Test Record',
            'title': 'Test Record',
            'href': 'https://www.example.com'
        }
    }
}

test_standard_complete_record = {
    'resource': {
        'title': {
            'value': 'Test Record',
            'title': 'Test Record',
            'href': 'https://www.example.com'
        }
    }
}

iso_19115_v1_minimal_record = {
    'contacts': [
        {
            'role': ['pointOfContact']
        }
    ],
    'date_stamp': datetime(2018, 10, 18, 14, 40, 44, tzinfo=timezone.utc),
    'resource': {
        'title': {
            'value': 'Test Record'
        },
        'dates': [
            {
                'date': date(2018, 1, 1),
                'date_precision': 'year',
                'date_type': 'creation'
            }
        ],
        'abstract': 'Test Record for ISO 19115 metadata standard (no profile) with required properties only.',
        'language': 'eng'
    }
}

iso_19115_v1_base_simple_record = {
    'file_identifier': 'b1a7d1b5-c419-41e7-9178-b1ffd76d5371',
    'language': 'eng',
    'character_set': 'utf8',
    'hierarchy_level': 'dataset',
    'contacts': [
        {
            'organisation': {
                'name': 'UK Polar Data Centre'
            },
            'phone': '+44 (0)1223 221400',
            'address': {
                'delivery_point': 'British Antarctic Survey, High Cross, Madingley Road',
                'city': 'Cambridge',
                'administrative_area': 'Cambridgeshire',
                'postal_code': 'CB3 0ET',
                'country': 'United Kingdom'
            },
            'email': 'polardatacentre@bas.ac.uk',
            'role': ['pointOfContact']
        }
    ],
    'date_stamp': datetime(2018, 10, 18, 14, 40, 44, tzinfo=timezone.utc),
    'maintenance': {
        'maintenance_frequency': 'asNeeded',
        'progress': 'completed'
    },
    'metadata_standard': {
        'name': 'ISO 19115',
        'version': '1.0'
    },
    'reference_system_info': {
        'code': {
            'value': 'urn:ogc:def:crs:EPSG::4326'
        }
    },
    'resource': {
        'title': {
            'value': 'Test Record'
        },
        'abstract': 'Test Record for ISO 19115 metadata standard (no profile) with simple baseline properties only. In '
                    'this context baseline properties are those that are required, or have default values. Values in '
                    'this record are non-complex, meaning they are simple character strings rather than anchors. '
                    'Authorities are not included in elements that support citations.',
        'dates': [
            {
                'date': date(2018, 1, 1),
                'date_precision': 'year',
                'date_type': 'creation'
            },
            {
                'date': datetime(2018, 10, 8, 14, 40, 44, tzinfo=timezone.utc),
                'date_type': 'publication'
            }
        ],
        'contacts': [
            {
                'individual': {
                    'name': 'Watson, Constance'
                },
                'organisation': {
                    'name': 'British Antarctic Survey'
                },
                'email': 'conwat@bas.ac.uk',
                'role': ['author']
            },
            {
                'organisation': {
                    'name': 'UK Polar Data Centre'
                },
                'phone': '+44 (0)1223 221400',
                'address': {
                    'delivery_point': 'British Antarctic Survey, High Cross, Madingley Road',
                    'city': 'Cambridge',
                    'administrative_area': 'Cambridgeshire',
                    'postal_code': 'CB3 0ET',
                    'country': 'United Kingdom'
                },
                'email': 'polardatacentre@bas.ac.uk',
                'role': [
                    'pointOfContact',
                    'custodian',
                    'publisher',
                    'distributor'
                ]
            }
        ],
        'maintenance': {
            'maintenance_frequency': 'asNeeded',
            'progress': 'completed'
        },
        'keywords': [
            {
                'terms': [
                    {
                        'term': 'Atmospheric conditions'
                    }
                ],
                'type': 'theme'
            }
        ],
        'constraints': {
            'access': [
                {
                    'restriction_code': 'otherRestrictions'
                }
            ],
            'usage': [
                {
                    'restriction_code': 'copyright',
                    'copyright_licence': {
                        'code': 'OGL-UK-3.0',
                        'statement': 'This information is licensed under the Open Government Licence v3.0. To view this'
                                     ' licence, visit http://www.nationalarchives.gov.uk/doc/open-government-licence/'
                    }
                }
            ]
        },
        'supplemental_information': 'It is recommended that careful attention be paid to the contents of any data, and '
                                    'that the author be contacted with any questions regarding appropriate use. If you '
                                    'find any errors or omissions, please report them to polardatacentre@bas.ac.uk.',
        'spatial_representation_type': 'textTable',
        'spatial_resolution': None,
        'language': 'eng',
        'topics': [
            'environment',
            'climatologyMeteorologyAtmosphere'
        ],
        'extent': {
            'geographic': {
                'bounding_box': {
                    'west_longitude': -45.61521,
                    'east_longitude': -27.04976,
                    'south_latitude': -68.1511,
                    'north_latitude': -54.30761
                }
            },
            'temporal': {
                'period': {
                    'start': date(2018, 9, 14),
                    'end': date(2018, 9, 15)
                }
            }
        },
        'formats': [
            {
                'format': 'netCDF Classic'
            }
        ],
        'transfer_options': [
            {
                'online_resource': {
                    'href': 'https://ramadda.data.bas.ac.uk/repository/entry/show?entryid='
                            'b1a7d1b5-c419-41e7-9178-b1ffd76d5371',
                    'title': 'Get Data',
                    'description': 'Download measurement data',
                    'function': 'download'
                }
            }
        ],
        'lineage': 'Example lineage statement'
    }
}

iso_19115_v1_base_complex_record = {
    'file_identifier': 'b1a7d1b5-c419-41e7-9178-b1ffd76d5371',
    'language': 'eng',
    'character_set': 'utf8',
    'hierarchy_level': 'dataset',
    'contacts': [
        {
            'organisation': {
                'name': 'UK Polar Data Centre',
                'href': 'http://isni.org/isni/0000000405983800',
                'title': 'ISNI record'
            },
            'phone': '+44 (0)1223 221400',
            'address': {
                'delivery_point': 'British Antarctic Survey, High Cross, Madingley Road',
                'city': 'Cambridge',
                'administrative_area': 'Cambridgeshire',
                'postal_code': 'CB3 0ET',
                'country': 'United Kingdom'
            },
            'email': 'polardatacentre@bas.ac.uk',
            'online_resource': {
                'href': 'https://www.bas.ac.uk/team/business-teams/information-services/uk-polar-data-centre/',
                'function': 'information'
            },
            'role': ['pointOfContact']
        }
    ],
    'date_stamp': datetime(2018, 10, 18, 14, 40, 44, tzinfo=timezone.utc),
    'maintenance': {
        'maintenance_frequency': 'asNeeded',
        'progress': 'completed'
    },
    'metadata_standard': {
        'name': 'ISO 19115',
        'version': '1.0'
    },
    'reference_system_info': {
        'code': {
            'value': 'urn:ogc:def:crs:EPSG::4326',
            'href': 'http://www.opengis.net/def/crs/EPSG/0/4326'
        },
        'version': '6.18.3',
        'authority': {
            'title': {
                'value': 'European Petroleum Survey Group (EPSG) Geodetic Parameter Registry'
            },
            'dates': [{
                'date': date(2008, 11, 12),
                'date_type': 'publication'
            }],
            'contact': {
                'organisation': {
                    'name': 'European Petroleum Survey Group'
                },
                'email': 'EPSGadministrator@iogp.org',
                'online_resource': {
                    'href': 'https://www.epsg-registry.org/',
                    'function': 'information'
                },
                'role': ['publisher']
            }
        }
    },
    'resource': {
        'title': {
            'value': 'Test Record'
        },
        'abstract': 'Test Record for ISO 19115 metadata standard (no profile) with complex baseline properties only. '
                    'In this context baseline properties are those that are required, or have default values. Values '
                    'in this record are complex, meaning they use anchors where relevant rather than simple character '
                    'strings. Authorities are included in elements that support citations.',
        'dates': [
            {
                'date': date(2018, 1, 1),
                'date_precision': 'year',
                'date_type': 'creation'
            },
            {
                'date': datetime(2018, 10, 8, 14, 40, 44, tzinfo=timezone.utc),
                'date_type': 'publication'
            }
        ],
        'contacts': [
            {
                'individual': {
                    'name': 'Watson, Constance',
                    'href': 'https://sandbox.orcid.org/0000-0001-8373-6934',
                    'title': 'ORCID record'
                },
                'organisation': {
                    'name': 'British Antarctic Survey'
                },
                'email': 'conwat@bas.ac.uk',
                'online_resource': {
                    'href': 'https://sandbox.orcid.org/0000-0001-8373-6934',
                    'title': 'ORCID record',
                    'description': 'ORCID is an open, non-profit, community-driven effort to create and maintain a '
                                   'registry of unique researcher identifiers and a transparent method of linking '
                                   'research activities and outputs to these identifiers.',
                    'function': 'information'
                },
                'role': ['author']
            },
            {
                'organisation': {
                    'name': 'UK Polar Data Centre',
                    'href': 'http://isni.org/isni/0000000405983800',
                    'title': 'ISNI record'
                },
                'phone': '+44 (0)1223 221400',
                'address': {
                    'delivery_point': 'British Antarctic Survey, High Cross, Madingley Road',
                    'city': 'Cambridge',
                    'administrative_area': 'Cambridgeshire',
                    'postal_code': 'CB3 0ET',
                    'country': 'United Kingdom'
                },
                'email': 'polardatacentre@bas.ac.uk',
                'online_resource': {
                    'href': 'https://www.bas.ac.uk/team/business-teams/information-services/uk-polar-data-centre/',
                    'function': 'information'
                },
                'role': [
                    'pointOfContact',
                    'custodian',
                    'publisher',
                    'distributor'
                ]
            }
        ],
        'maintenance': {
            'maintenance_frequency': 'asNeeded',
            'progress': 'completed'
        },
        'keywords': [
            {
                'terms': [
                    {
                        'term': 'Atmospheric conditions',
                        'href': 'https://www.eionet.europa.eu/gemet/en/inspire-theme/ac'
                    }
                ],
                'type': 'theme',
                'thesaurus': {
                    'title': {
                        'value': 'General Multilingual Environmental Thesaurus - INSPIRE themes',
                        'href': 'http://www.eionet.europa.eu/gemet/inspire_themes'
                    },
                    'dates': [
                        {
                            'date': date(2018, 8, 16),
                            'date_type': 'publication'
                        }
                    ],
                    'edition': '4.1.2',
                    'contact': {
                        'organisation': {
                            'name': 'European Environment Information and Observation Network (EIONET), '
                                    'European Environment Agency (EEA)'
                        },
                        "email": "helpdesk@eionet.europa.eu",
                        'online_resource': {
                            'href': 'https://www.eionet.europa.eu/gemet/en/themes/',
                            'title': 'General Multilingual Environmental Thesaurus (GEMET) themes',
                            'function': 'information'
                        },
                        'role': ['publisher']
                    },
                }
            }
        ],
        'constraints': {
            'access': [
                {
                    'restriction_code': 'otherRestrictions'
                }
            ],
            'usage': [
                {
                    'restriction_code': 'copyright',
                    'copyright_licence': {
                        'code': 'OGL-UK-3.0',
                        'href': 'http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                        'statement': 'This information is licensed under the Open Government Licence v3.0. To view this'
                                     ' licence, visit http://www.nationalarchives.gov.uk/doc/open-government-licence/'
                    }
                }
            ]
        },
        'supplemental_information': 'It is recommended that careful attention be paid to the contents of any data, and '
                                    'that the author be contacted with any questions regarding appropriate use. If you '
                                    'find any errors or omissions, please report them to polardatacentre@bas.ac.uk.',
        'spatial_representation_type': 'textTable',
        'spatial_resolution': None,
        'language': 'eng',
        'topics': [
            'environment',
            'climatologyMeteorologyAtmosphere'
        ],
        'extent': {
            'geographic': {
                'bounding_box': {
                    'west_longitude': -45.61521,
                    'east_longitude': -27.04976,
                    'south_latitude': -68.1511,
                    'north_latitude': -54.30761
                }
            },
            'temporal': {
                'period': {
                    'start': date(2018, 9, 14),
                    'end': date(2018, 9, 15)
                }
            }
        },
        'formats': [
            {
                'format': 'netCDF Classic',
                'href': 'https://www.unidata.ucar.edu/software/netcdf/docs/netcdf_introduction.html#classic_format'
            }
        ],
        'transfer_options': [
            {
                'online_resource': {
                    'href': 'https://ramadda.data.bas.ac.uk/repository/entry/show?entryid='
                            'b1a7d1b5-c419-41e7-9178-b1ffd76d5371',
                    'title': 'Get Data',
                    'description': 'Download measurement data',
                    'function': 'download'
                }
            }
        ],
        'lineage': 'Example lineage statement'
    }
}

iso_19115_v1_complete_record = {
    'file_identifier': 'b1a7d1b5-c419-41e7-9178-b1ffd76d5371',
    'language': 'eng',
    'character_set': 'utf8',
    'hierarchy_level': 'dataset',
    'contacts': [
        {
            'organisation': {
                'name': 'UK Polar Data Centre',
                'href': 'http://isni.org/isni/0000000405983800',
                'title': 'ISNI record'
            },
            'phone': '+44 (0)1223 221400',
            'address': {
                'delivery_point': 'British Antarctic Survey, High Cross, Madingley Road',
                'city': 'Cambridge',
                'administrative_area': 'Cambridgeshire',
                'postal_code': 'CB3 0ET',
                'country': 'United Kingdom'
            },
            'email': 'polardatacentre@bas.ac.uk',
            'online_resource': {
                'href': 'https://www.bas.ac.uk/team/business-teams/information-services/uk-polar-data-centre/',
                'function': 'information'
            },
            'role': ['pointOfContact']
        }
    ],
    'date_stamp': datetime(2018, 10, 18, 14, 40, 44, tzinfo=timezone.utc),
    'maintenance': {
        'maintenance_frequency': 'asNeeded',
        'progress': 'completed'
    },
    'metadata_standard': {
        'name': 'ISO 19115',
        'version': '1.0'
    },
    'reference_system_info': {
        'code': {
            'value': 'urn:ogc:def:crs:EPSG::4326',
            'href': 'http://www.opengis.net/def/crs/EPSG/0/4326'
        },
        'version': '6.18.3',
        'authority': {
            'title': {
                'value': 'European Petroleum Survey Group (EPSG) Geodetic Parameter Registry'
            },
            'dates': [{
                'date': date(2008, 11, 12),
                'date_type': 'publication'
            }],
            'contact': {
                'organisation': {
                    'name': 'European Petroleum Survey Group'
                },
                'email': 'EPSGadministrator@iogp.org',
                'online_resource': {
                    'href': 'https://www.epsg-registry.org/',
                    'function': 'information'
                },
                'role': ['publisher']
            }
        }
    },
    'resource': {
        'title': {
            'value': 'Test Record'
        },
        'abstract': 'Test Record for ISO 19115 metadata standard (no profile) with properties that could typically be '
                    'included in a record. This does not mean all properties permitted the standard are included, as '
                    'these are too numerous. Values in this record are complex, meaning they use anchors where '
                    'relevant rather than simple character strings. Authorities are included in elements that support '
                    'citations. Identifiers in this record are fake.',
        'dates': [
            {
                'date': date(2018, 1, 1),
                'date_precision': 'year',
                'date_type': 'creation'
            },
            {
                'date': date(2018, 1, 1),
                'date_precision': 'year',
                'date_type': 'revision'
            },
            {
                'date': datetime(2018, 10, 8, 14, 40, 44, tzinfo=timezone.utc),
                'date_type': 'publication'
            },
            {
                'date': datetime(2018, 10, 8, 14, 40, 44, tzinfo=timezone.utc),
                'date_type': 'released'
            }
        ],
        'edition': '1',
        'identifiers': [
            {
                'identifier': 'https://doi.org/10.5072/r3qz22k64',
                'href': 'https://doi.org/10.5072/r3qz22k64',
                'title': 'doi'
            },
            {
                'identifier': 'NE/E007895/1',
                'href': 'https://gtr.ukri.org/projects?ref=NE%2FE007895%2F1',
                'title': 'award'
            }
        ],
        'contacts': [
            {
                'individual': {
                    'name': 'Watson, Constance',
                    'href': 'https://sandbox.orcid.org/0000-0001-8373-6934',
                    'title': 'ORCID record'
                },
                'organisation': {
                    'name': 'British Antarctic Survey'
                },
                'email': 'conwat@bas.ac.uk',
                'online_resource': {
                    'href': 'https://sandbox.orcid.org/0000-0001-8373-6934',
                    'title': 'ORCID record',
                    'description': 'ORCID is an open, non-profit, community-driven effort to create and maintain a '
                                   'registry of unique researcher identifiers and a transparent method of linking '
                                   'research activities and outputs to these identifiers.',
                    'function': 'information'
                },
                'role': ['author']
            },
            {
                'individual': {
                    'name': 'Cinnamon, John',
                    'href': 'https://sandbox.orcid.org/0000-0001-5652-1129',
                    'title': 'ORCID record'
                },
                'organisation': {
                    'name': 'British Antarctic Survey'
                },
                'email': 'conwat@bas.ac.uk',
                'online_resource': {
                    'href': 'https://sandbox.orcid.org/0000-0001-5652-1129',
                    'title': 'ORCID record',
                    'description': 'ORCID is an open, non-profit, community-driven effort to create and maintain a '
                                   'registry of unique researcher identifiers and a transparent method of linking '
                                   'research activities and outputs to these identifiers.',
                    'function': 'information'
                },
                'role': ['collaborator']
            },
            {
                'organisation': {
                    'name': 'UK Polar Data Centre',
                    'href': 'http://isni.org/isni/0000000405983800',
                    'title': 'ISNI record'
                },
                'phone': '+44 (0)1223 221400',
                'address': {
                    'delivery_point': 'British Antarctic Survey, High Cross, Madingley Road',
                    'city': 'Cambridge',
                    'administrative_area': 'Cambridgeshire',
                    'postal_code': 'CB3 0ET',
                    'country': 'United Kingdom'
                },
                'email': 'polardatacentre@bas.ac.uk',
                'online_resource': {
                    'href': 'https://www.bas.ac.uk/team/business-teams/information-services/uk-polar-data-centre/',
                    'function': 'information'
                },
                'role': [
                    'pointOfContact',
                    'custodian',
                    'publisher',
                    'distributor'
                ]
            },
            {
                'organisation': {
                    'name': 'Natural Environment Research Council',
                    'href': 'http://isni.org/isni/0000000094781573',
                    'title': 'ISNI record'
                },
                'phone': '+44 (0)1793 411500',
                'address': {
                    'delivery_point': 'Natural Environment Research Council, Polaris House, North Star Avenue',
                    'city': 'Swindon',
                    'administrative_area': 'Hampshire',
                    'postal_code': 'SN2 1EU',
                    'country': 'United Kingdom'
                },
                'email': 'researchgrants@nerc.ukri.org',
                'online_resource': {
                    'href': 'https://nerc.ukri.org',
                    'function': 'information'
                },
                'role': [
                    'funder'
                ]
            }
        ],
        'maintenance': {
            'maintenance_frequency': 'asNeeded',
            'progress': 'completed'
        },
        'keywords': [
            {
                'terms': [
                    {
                        'term': 'Atmospheric conditions',
                        'href': 'https://www.eionet.europa.eu/gemet/en/inspire-theme/ac'
                    }
                ],
                'type': 'theme',
                'thesaurus': {
                    'title': {
                        'value': 'General Multilingual Environmental Thesaurus - INSPIRE themes',
                        'href': 'http://www.eionet.europa.eu/gemet/inspire_themes'
                    },
                    'dates': [
                        {
                            'date': date(2018, 8, 16),
                            'date_type': 'publication'
                        }
                    ],
                    'edition': '4.1.2',
                    'contact': {
                        'organisation': {
                            'name': 'European Environment Information and Observation Network (EIONET), '
                                    'European Environment Agency (EEA)'
                        },
                        "email": "helpdesk@eionet.europa.eu",
                        'online_resource': {
                            'href': 'https://www.eionet.europa.eu/gemet/en/themes/',
                            'title': 'General Multilingual Environmental Thesaurus (GEMET) themes',
                            'function': 'information'
                        },
                        'role': ['publisher']
                    },
                }
            }
        ],
        'constraints': {
            'access': [
                {
                    'restriction_code': 'otherRestrictions'
                }
            ],
            'usage': [
                {
                    'restriction_code': 'copyright',
                    'copyright_licence': {
                        'code': 'OGL-UK-3.0',
                        'href': 'http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                        'statement': 'This information is licensed under the Open Government Licence v3.0. To view this'
                                     ' licence, visit http://www.nationalarchives.gov.uk/doc/open-government-licence/'
                    }
                }
            ]
        },
        'supplemental_information': 'It is recommended that careful attention be paid to the contents of any data, and '
                                    'that the author be contacted with any questions regarding appropriate use. If you '
                                    'find any errors or omissions, please report them to polardatacentre@bas.ac.uk.',
        'spatial_representation_type': 'textTable',
        'spatial_resolution': None,
        'language': 'eng',
        'topics': [
            'environment',
            'climatologyMeteorologyAtmosphere'
        ],
        'extent': {
            'geographic': {
                'bounding_box': {
                    'west_longitude': -45.61521,
                    'east_longitude': -27.04976,
                    'south_latitude': -68.1511,
                    'north_latitude': -54.30761
                }
            },
            'vertical': {
                'minimum': 20,
                'maximum': 40,
                'identifier': 'ogp-crs-5714',
                'code': 'urn:ogc:def:crs:EPSG::5714',
                'name': 'MSL height',
                'remarks': 'Not specific to any location or epoch.',
                'scope': 'Hydrography.',
                'domain_of_validity': {
                    'href': 'urn:ogc:def:area:EPSG::1262'
                },
                'vertical_cs': {
                    'href': 'urn:ogc:def:cs:EPSG::6498'
                },
                'vertical_datum': {
                    'href': 'urn:ogc:def:datum:EPSG::5100'
                }
            },
            'temporal': {
                'period': {
                    'start': date(2018, 9, 14),
                    'end': date(2018, 9, 15)
                }
            }
        },
        'formats': [
            {
                'format': 'netCDF Classic',
                'href': 'https://www.unidata.ucar.edu/software/netcdf/docs/netcdf_introduction.html#classic_format'
            }
        ],
        'transfer_options': [
            {
                'size': {
                    'unit': 'MB',
                    'magnitude': 40
                },
                'online_resource': {
                    'href': 'https://ramadda.data.bas.ac.uk/repository/entry/show?entryid='
                            'b1a7d1b5-c419-41e7-9178-b1ffd76d5371',
                    'title': 'Get Data',
                    'description': 'Download measurement data',
                    'function': 'download'
                }
            },
            {
                'online_resource': {
                    'href': 'https://www.bodc.ac.uk/data/bodc_database/nodb/data_collection/6618/',
                    'title': 'View Information',
                    'description': 'Download background information and context',
                    'function': 'information'
                }
            },
        ],
        'lineage': 'Example lineage statement'
    }
}

test_record = {
iso_19115_v1_gemini_complete_record = {
    'file_identifier': 'b1a7d1b5-c419-41e7-9178-b1ffd76d5371',
    'language': 'eng',
    'character_set': 'utf8',
    'hierarchy_level': 'dataset',
    'contacts': [
        {
            'organisation': {
                'name': 'UK Polar Data Centre',
                'href': 'http://isni.org/isni/0000000405983800',
                'title': 'ISNI record'
            },
            'phone': '+44 (0)1223 221400',
            'address': {
                'delivery_point': 'British Antarctic Survey, High Cross, Madingley Road',
                'city': 'Cambridge',
                'administrative_area': 'Cambridgeshire',
                'postal_code': 'CB3 0ET',
                'country': 'United Kingdom'
            },
            'email': 'polardatacentre@bas.ac.uk',
            'online_resource': {
                'href': 'https://www.bas.ac.uk/team/business-teams/information-services/uk-polar-data-centre/',
                'function': 'information'
            },
            'role': ['pointOfContact']
        }
    ],
    'date_stamp': datetime(2018, 10, 8, 14, 40, 44, tzinfo=timezone.utc),
    'date_stamp': datetime(2018, 10, 18, 14, 40, 44, tzinfo=timezone.utc),
    'maintenance': {
        'maintenance_frequency': 'asNeeded',
        'progress': 'completed'
    },
    'metadata_standard': {
        'name': 'ISO 19115 (UK GEMINI)',
        'version': '1.0 (2.3)'
    },
    'reference_system_info': {
        'code': {
            'value': 'urn:ogc:def:crs:EPSG::4326',
            'href': 'http://www.opengis.net/def/crs/EPSG/0/4326'
        },
        'version': '6.18.3',
        'authority': {
            'title': {
                'value': 'European Petroleum Survey Group (EPSG) Geodetic Parameter Registry'
            },
            'dates': [{
                'date': date(2008, 11, 12),
                'date_type': 'publication'
            }],
            'contact': {
                'organisation': {
                    'name': 'European Petroleum Survey Group'
                },
                'email': 'EPSGadministrator@iogp.org',
                'online_resource': {
                    'href': 'https://www.epsg-registry.org/',
                    'function': 'information'
                },
                'role': ['publisher']
            }
        }
    },
    'resource': {
        'title': {
            'value': 'Analysis of d18O and salinity from sea ice and meltwater pool water samples collected in April '
                     '2016 in the Weddell Sea and Scotia Sea of the Southern Ocean during the marine survey JR15006'
            'value': 'Test Record'
        },
        'abstract': 'The dataset contains oxygen stable isotope and salinity measurements from water samples collected '
                    'from sea ice and meltwater pools in April 2016 in the region of South Georgia, Signy and deep '
                    'within the Weddell Sea pack ice during the marine survey JR15006. The d18O and salinity '
                    'measurements from sea ice and meltwater sources complement the same analysis from CTD casts and '
                    'underway non-toxic flow water system on the RRS James Clark Ross during the JR15006. Establishing '
                    'd18O and salinity values for saline water and oceanic freshwater components can be used to '
                    'identify sources and changes of freshwater contributions to the ocean.',
        'abstract': 'Test Record for ISO 19115 metadata standard (Inspire/Gemini profile) with properties that could '
                    'typically be included in a record. This does not mean all properties permitted the standard are '
                    'included, as these are too numerous. Values in this record are complex, meaning they use anchors '
                    'where relevant rather than simple character strings. Authorities are included in elements that '
                    'support citations. Identifiers in this record are fake.',
        'dates': [
            {
                'date': date(2018, 1, 1),
                'date_precision': 'year',
                'date_type': 'creation'
            },
            {
                'date': date(2018, 1, 1),
                'date_precision': 'year',
                'date_type': 'revision'
            },
            {
                'date': datetime(2018, 10, 8, 14, 40, 44, tzinfo=timezone.utc),
                'date_type': 'publication'
            },
            {
                'date': datetime(2018, 12, 8, 14, 40, 44, tzinfo=timezone.utc),
                'date': datetime(2018, 10, 8, 14, 40, 44, tzinfo=timezone.utc),
                'date_type': 'released'
            }
        ],
        'edition': '1',
        'identifiers': [
            {
                'identifier': 'https://doi.org/10.5285/3cf26ab6-7f47-4868-a87d-c62a2eefea1f',
                'href': 'https://doi.org/10.5285/3cf26ab6-7f47-4868-a87d-c62a2eefea1f',
                'identifier': 'https://doi.org/10.5072/r3qz22k64',
                'href': 'https://doi.org/10.5072/r3qz22k64',
                'title': 'doi'
            },
            {
                'identifier': 'NE/I022973/1',
                'href': 'https://gtr.ukri.org/projects?ref=NE%2FI022973%2F1',
                'identifier': 'NE/E007895/1',
                'href': 'https://gtr.ukri.org/projects?ref=NE%2FE007895%2F1',
                'title': 'award'
            }
        ],
        'contacts': [
            {
                'individual': {
                    'name': 'Michael Meredith',
                    'href': 'https://orcid.org/0000-0002-7342-7756',
                    'name': 'Watson, Constance',
                    'href': 'https://sandbox.orcid.org/0000-0001-8373-6934',
                    'title': 'ORCID record'
                },
                'organisation': {
                    'name': 'British Antarctic Survey'
                },
                'email': 'mmm@bas.ac.uk',
                'online_resource': {
                    'href': 'https://orcid.org/0000-0002-7342-7756',
                    'title': 'ORCID record',
                    'description': 'ORCID is an open, non-profit, community-driven effort to create and maintain a '
                                   'registry of unique researcher identifiers and a transparent method of linking '
                                   'research activities and outputs to these identifiers.',
                    'function': 'information'
                },
                'role': ['author']
            },
            {
                'individual': {
                    'name': 'Carol Arrowsmith',
                    'href': 'https://orcid.org/0000-0003-3849-5179',
                    'title': 'ORCID record'
                },
                'organisation': {
                    'name': 'British Geological Survey'
                },
                'email': 'noreply@bas.ac.uk',
                'email': 'conwat@bas.ac.uk',
                'online_resource': {
                    'href': 'https://orcid.org/0000-0003-3849-5179',
                    'href': 'https://sandbox.orcid.org/0000-0001-8373-6934',
                    'title': 'ORCID record',
                    'description': 'ORCID is an open, non-profit, community-driven effort to create and maintain a '
                                   'registry of unique researcher identifiers and a transparent method of linking '
                                   'research activities and outputs to these identifiers.',
                    'function': 'information'
                },
                'role': ['author']
            },
            {
                'individual': {
                    'name': 'Melanie Leng',
                    'href': 'https://orcid.org/0000-0003-1115-5166',
                    'name': 'Cinnamon, John',
                    'href': 'https://sandbox.orcid.org/0000-0001-5652-1129',
                    'title': 'ORCID record'
                },
                'organisation': {
                    'name': 'British Geological Survey'
                    'name': 'British Antarctic Survey'
                },
                'email': 'noreply@bas.ac.uk',
                'email': 'conwat@bas.ac.uk',
                'online_resource': {
                    'href': 'https://orcid.org/0000-0003-1115-5166',
                    'href': 'https://sandbox.orcid.org/0000-0001-5652-1129',
                    'title': 'ORCID record',
                    'description': 'ORCID is an open, non-profit, community-driven effort to create and maintain a '
                                   'registry of unique researcher identifiers and a transparent method of linking '
                                   'research activities and outputs to these identifiers.',
                    'function': 'information'
                },
                'role': ['author']
                'role': ['collaborator']
            },
            {
                'organisation': {
                    'name': 'UK Polar Data Centre',
                    'href': 'http://isni.org/isni/0000000405983800',
                    'title': 'ISNI record'
                },
                'phone': '+44 (0)1223 221400',
                'address': {
                    'delivery_point': 'British Antarctic Survey, High Cross, Madingley Road',
                    'city': 'Cambridge',
                    'administrative_area': 'Cambridgeshire',
                    'postal_code': 'CB3 0ET',
                    'country': 'United Kingdom'
                },
                'email': 'polardatacentre@bas.ac.uk',
                'online_resource': {
                    'href': 'https://www.bas.ac.uk/team/business-teams/information-services/uk-polar-data-centre/',
                    'function': 'information'
                },
                'role': [
                    'pointOfContact',
                    'custodian',
                    'publisher',
                    'distributor'
                ]
            },
            {
                'organisation': {
                    'name': 'Natural Environment Research Council',
                    'href': 'http://isni.org/isni/0000000094781573',
                    'title': 'ISNI record'
                },
                'phone': '+44 (0)1793 411500',
                'address': {
                    'delivery_point': 'Natural Environment Research Council, Polaris House, North Star Avenue',
                    'city': 'Swindon',
                    'administrative_area': 'Hampshire',
                    'postal_code': 'SN2 1EU',
                    'country': 'United Kingdom'
                },
                'email': 'researchgrants@nerc.ukri.org',
                'online_resource': {
                    'href': 'https://nerc.ukri.org',
                    'function': 'information'
                },
                'role': [
                    'funder'
                ]
            }
        ],
        'maintenance': {
            'maintenance_frequency': 'asNeeded',
            'progress': 'completed'
        },
        'keywords': [
            {
                'terms': [
                    {
                        'term': 'Oceanographic geographical features',
                        'href': 'https://www.eionet.europa.eu/gemet/en/inspire-theme/of'
                    },
                    {
                        'term': 'Sea regions',
                        'href': 'https://www.eionet.europa.eu/gemet/en/inspire-theme/sr'
                    },
                    {
                        'term': 'Land Cover',
                        'href': 'https://www.eionet.europa.eu/gemet/en/inspire-theme/lc'
                        'term': 'Atmospheric conditions',
                        'href': 'https://www.eionet.europa.eu/gemet/en/inspire-theme/ac'
                    }
                ],
                'type': 'theme',
                'thesaurus': {
                    'title': {
                        'value': 'General Multilingual Environmental Thesaurus - INSPIRE themes',
                        'href': 'http://www.eionet.europa.eu/gemet/inspire_themes'
                    },
                    'dates': [
                        {
                            'date': date(2018, 8, 16),
                            'date_type': 'publication'
                        }
                    ],
                    'edition': '4.1.2',
                    'contact': {
                        'organisation': {
                            'name': 'European Environment Information and Observation Network (EIONET), '
                                    'European Environment Agency (EEA)'
                        },
                        "email": "helpdesk@eionet.europa.eu",
                        'online_resource': {
                            'href': 'https://www.eionet.europa.eu/gemet/en/themes/',
                            'title': 'General Multilingual Environmental Thesaurus (GEMET) themes',
                            'function': 'information'
                        },
                        'role': ['publisher']
                    },
                }
            },
            {
                'terms': [
                    {
                        'term': 'EARTH SCIENCE > Hydrosphere > Snow/Ice > Snow Melt'
                    },
                    {
                        'term': 'EARTH SCIENCE > Hydrosphere > Surface Water'
                    },
                    {
                        'term': 'EARTH SCIENCE > Oceans > Sea Ice > Isotopes'
                    },
                    {
                        'term': 'EARTH SCIENCE > Oceans > Sea Ice > Pack Ice'
                    },
                    {
                        'term': 'EARTH SCIENCE > Oceans > Sea Ice > Salinity'
                    }
                ],
                'type': 'theme',
                'thesaurus': {
                    'title': {
                        'value': 'Global Change Master Directory (GCMD) Science Keywords',
                        'href': 'https://earthdata.nasa.gov/about/gcmd/global-change-master-directory-gcmd-keywords'
                    },
                    'dates': [
                        {
                            'date': date(2018, 3, 15),
                            'date_type': 'publication'
                        }
                    ],
                    'edition': '8.6',
                    'contact': {
                        'organisation': {
                            'name': 'Global Change Data Center, Science and Exploration Directorate, Goddard Space '
                                    'Flight Center (GSFC) National Aeronautics and Space Administration (NASA)'
                        },
                        "email": "support@earthdata.nasa.gov",
                        'address': {
                            'city': 'Greenbelt',
                            'administrative_area': 'MD',
                            'country': 'United States of America'
                        },
                        'online_resource': {
                            'href': 'https://earthdata.nasa.gov/about/gcmd/global-change-master-directory-gcmd-keywords',
                            'title': 'Global Change Master Directory (GCMD) Keywords',
                            'description': 'The information provided on this page seeks to define how the GCMD '
                                           'Keywords are structured, used and accessed. It also provides information '
                                           'on how users can participate in the further development of the keywords.',
                            'function': 'information'
                        },
                        'role': ['publisher']
                    }
                }
            },
            {
                'terms': [
                    {
                        'term': 'd18O'
                    },
                    {
                        'term': 'meltwater pool'
                    },
                    {
                        'term': 'salinity'
                    },
                    {
                        'term': 'sea ice'
                    }
                ],
                'type': 'theme'
            }
        ],
        'constraints': {
            'access': [
                {
                    'restriction_code': 'otherRestrictions',
                    'inspire_limitations_on_public_access': 'noLimitations'
                }
            ],
            'usage': [
                {
                    'restriction_code': 'otherRestrictions',
                    'copyright_licence': {
                        'code': 'OGL-UK-3.0',
                        'href': 'http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
                        'statement': 'This information is licensed under the Open Government Licence v3.0. To view this'
                                     ' licence, visit http://www.nationalarchives.gov.uk/doc/open-government-licence/'
                    }
                },
                {
                    'restriction_code': 'otherRestrictions',
                    'required_citation': 'Bougamont, M. (2018). Ice flow model output for Pine Island Glacier '
                                         '(West Antarctica), from numerical inversions of ice surface velocities '
                                         'observed in 1996 and 2014 [Data set]. UK Polar Data Centre, Natural '
                                         'Environment Research Council, UK Research and Innovation. '
                                         'https://doi.org/10.5285/3cf26ab6-7f47-4868-a87d-c62a2eefea1f'
                }
            ]
        },
        'supplemental_information': 'It is recommended that careful attention be paid to the contents of any data, and '
                                    'that the author be contacted with any questions regarding appropriate use. If you '
                                    'find any errors or omissions, please report them to polardatacentre@bas.ac.uk.',
        'spatial_representation_type': 'textTable',
        'spatial_resolution': None,
        'language': 'eng',
        'topics': [
            'environment',
            'inlandWaters',
            'oceans'
            'climatologyMeteorologyAtmosphere'
        ],
        'extent': {
            'geographic': {
                'bounding_box': {
                    'west_longitude': -45.61521,
                    'east_longitude': -27.04976,
                    'south_latitude': -68.1511,
                    'north_latitude': -54.30761
                }
            },
            'vertical': {
                'identifier': 'ogp-crs-5715',
                'code': 'urn:ogc:def:crs:EPSG::5715',
                'name': 'MSL depth',
                'minimum': 20,
                'maximum': 40,
                'identifier': 'ogp-crs-5714',
                'code': 'urn:ogc:def:crs:EPSG::5714',
                'name': 'MSL height',
                'remarks': 'Not specific to any location or epoch.',
                'scope': 'Hydrography.',
                'domain_of_validity': {
                    'href': 'urn:ogc:def:area:EPSG::1262'
                },
                'vertical_cs': {
                    'href': 'urn:ogc:def:cs:EPSG::6498'
                },
                'vertical_datum': {
                    'href': 'urn:ogc:def:datum:EPSG::5100'
                }
            },
            'temporal': {
                'period': {
                    'start': date(2016, 3, 31),
                    'end': date(2016, 4, 26)
                    'start': date(2018, 9, 14),
                    'end': date(2018, 9, 15)
                }
            }
        },
        'formats': [
            {
                'format': 'Microsoft Excel Workbook',
                'href': 'https://www.iana.org/assignments/media-types/application/'
                        'vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                'format': 'netCDF Classic',
                'href': 'https://www.unidata.ucar.edu/software/netcdf/docs/netcdf_introduction.html#classic_format'
            }
        ],
        'transfer_options': [
            {
                'online_resource': {
                    'href': 'https://www.bodc.ac.uk/data/bodc_database/nodb/data_collection/6618/',
                    'title': 'Get Data',
                    'description': 'Download underlying CTD data',
                    'function': 'download'
                }
            },
            {
                'size': {
                    'unit': 'KB',
                    'magnitude': 70
                    'unit': 'MB',
                    'magnitude': 40
                },
                'online_resource': {
                    'href': 'https://ramadda.data.bas.ac.uk/repository/entry/show?entryid='
                            '63af1e57-8f20-4fb1-a55c-bd0e703f8a56',
                            'b1a7d1b5-c419-41e7-9178-b1ffd76d5371',
                    'title': 'Get Data',
                    'description': 'Download measurement data',
                    'function': 'download'
                }
            }
            },
            {
                'online_resource': {
                    'href': 'https://www.bodc.ac.uk/data/bodc_database/nodb/data_collection/6618/',
                    'title': 'View Information',
                    'description': 'Download background information and context',
                    'function': 'information'
                }
            },
        ],
        'measures': [
            {
                'code': 'Conformity_001',
                'code_space': 'INSPIRE',
                'pass': True,
                'title': {
                    'value': 'Commission Regulation (EU) No 1089/2010 of 23 November 2010 implementing Directive '
                             '2007/2/EC of the European Parliament and of the Council as regards interoperability of '
                             'spatial data sets and services',
                    'href': 'http://data.europa.eu/eli/reg/2010/1089'
                },
                'dates': [
                    {
                        'date': date(2010, 12, 8),
                        'date_type': 'publication'
                    }
                ],
                'explanation': 'See the referenced specification'
            }
        ],
        'lineage': 'At all sample locations, 2 or more salinity bottles and d18O vials were filled following the usual '
                   'procedure. The d18O vials were rinsed 3 times, filled and dried before being closed with a stopper '
                   'and sealed with the crimper. Oxygen isotope (d18O) measurements were made using the CO2 '
                   'equilibration method with an Isoprime 100 mass spectrometer plus Aquaprep device. 90 samples '
                   '(200µl of water) were loaded into Labco Limited exetainers (3.7ml) and placed in the heated '
                   'sample tray at 40°C. The exetainers were then evacuated to remove atmosphere then flushed '
                   'with CO2 and left to equilibrate for between 12 (first sample) - 37 (last sample) hours. Each '
                   'individual gas sample was then admitted to the cryogenic water trap where any water vapour is '
                   'removed. The dry sample gas was then expanded into the dual inlet where it was measured on the '
                   'transducer before being expanded in the dual inlet bellows. Ionvantage software then balances the '
                   'reference bellows relative to this volume. The sample and reference CO2 gases enter alternatively '
                   'into the Isoprime100 through the dual changeover valve for isotope ratio measurement. In each run '
                   'two laboratory standards (CA-HI and CA-LO) plus up to 2 secondary standards were analysed in '
                   'triplicate. The value of these laboratory standards has been accurately determined by comparison '
                   'with international calibration and reference materials (VSMOW2, SLAP2 and GISP) and so the 18O/16O '
                   'ratios (versus VSMOW2) of the unknown samples can be calculated and are expressed in delta units, '
                   'd18O (parts per mille). Errors are < +/- 0.05 per mil.'
        'lineage': 'Example lineage statement'
    }
}
