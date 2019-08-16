from copy import deepcopy
from datetime import datetime, timezone, date

# Test standard

test_standard_minimal_record = {
    'resource': {
        'title': {
            'value': 'Test Record'
        }
    }
}

test_standard_typical_record = deepcopy(test_standard_minimal_record)
test_standard_typical_record['resource']['title']['href'] = 'https://www.example.com'

test_standard_complete_record = deepcopy(test_standard_typical_record)
test_standard_complete_record['resource']['title']['title'] = 'Test Record'

test_standard_record_with_entities = deepcopy(test_standard_minimal_record)
test_standard_record_with_entities['resource']['title']['value'] = 'Test Record with entites: \'>\' (greater than), ' \
                                                                   '\'å\' (accent [a-ring]) and \'µ\' (micro)'

# ISO 19115 standard

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

iso_19115_v1_minimal_record_with_required_doi_citation = deepcopy(iso_19115_v1_minimal_record)
iso_19115_v1_minimal_record_with_required_doi_citation['resource']['constraints'] = {
    'usage': [
        {
            'restriction_code': 'otherRestrictions',
            'required_citation': {
                'doi': 'https://doi.org/10.7939/r3qz22k64'
            }
        }
    ]
}

iso_19115_v1_base_simple_record = deepcopy(iso_19115_v1_minimal_record)
iso_19115_v1_base_simple_record['file_identifier'] = 'b1a7d1b5-c419-41e7-9178-b1ffd76d5371'
iso_19115_v1_base_simple_record['language'] = 'eng'
iso_19115_v1_base_simple_record['character_set'] = 'utf8'
iso_19115_v1_base_simple_record['hierarchy_level'] = 'dataset'
iso_19115_v1_base_simple_record['contacts'][0]['organisation'] = {
    'name': 'UK Polar Data Centre'
}
iso_19115_v1_base_simple_record['contacts'][0]['phone'] = '+44 (0)1223 221400'
iso_19115_v1_base_simple_record['contacts'][0]['address'] = {
    'delivery_point': 'British Antarctic Survey, High Cross, Madingley Road',
    'city': 'Cambridge',
    'administrative_area': 'Cambridgeshire',
    'postal_code': 'CB3 0ET',
    'country': 'United Kingdom'
}
iso_19115_v1_base_simple_record['contacts'][0]['email'] = 'polardatacentre@bas.ac.uk'
iso_19115_v1_base_simple_record['maintenance'] = {
    'maintenance_frequency': 'asNeeded',
    'progress': 'completed'
}
iso_19115_v1_base_simple_record['metadata_standard'] = {
    'name': 'ISO 19115',
    'version': '1.0'
}
iso_19115_v1_base_simple_record['reference_system_info'] = {
    'code': {
        'value': 'urn:ogc:def:crs:EPSG::4326'
    }
}
iso_19115_v1_base_simple_record['resource']['abstract'] = 'Test Record for ISO 19115 metadata standard (no profile) ' \
    'with simple baseline properties only. In this context baseline properties are those that are required, or have ' \
    'default values. Values in this record are non-complex, meaning they are simple character strings rather than ' \
    'anchors. Authorities are not included in elements that support citations.'
iso_19115_v1_base_simple_record['resource']['dates'].append({
    'date': datetime(2018, 10, 8, 14, 40, 44, tzinfo=timezone.utc),
    'date_type': 'publication'
})
iso_19115_v1_base_simple_record['resource']['contacts'] = [
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
]
iso_19115_v1_base_simple_record['resource']['maintenance'] = {
    'maintenance_frequency': 'asNeeded',
    'progress': 'completed'
}
iso_19115_v1_base_simple_record['resource']['keywords'] = [
    {
        'terms': [
            {
                'term': 'Atmospheric conditions'
            }
        ],
        'type': 'theme'
    }
]
iso_19115_v1_base_simple_record['resource']['constraints'] = {
    'access': [
        {
            'restriction_code': 'otherRestrictions'
        }
    ],
    'usage': [
        {
            'copyright_licence': {
                'code': 'OGL-UK-3.0',
                'statement': 'This information is licensed under the Open Government Licence v3.0. To view this'
                             ' licence, visit http://www.nationalarchives.gov.uk/doc/open-government-licence/'
            }
        }
    ]
}
iso_19115_v1_base_simple_record['resource']['supplemental_information'] = 'It is recommended that careful attention ' \
    'be paid to the contents of any data, and that the author be contacted with any questions regarding appropriate ' \
    'use. If you find any errors or omissions, please report them to polardatacentre@bas.ac.uk.'
iso_19115_v1_base_simple_record['resource']['spatial_representation_type'] = 'textTable'
iso_19115_v1_base_simple_record['resource']['spatial_resolution'] = None
iso_19115_v1_base_simple_record['resource']['topics'] = [
    'environment',
    'climatologyMeteorologyAtmosphere'
]
iso_19115_v1_base_simple_record['resource']['extent'] = {
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
}
iso_19115_v1_base_simple_record['resource']['formats'] = [
    {
        'format': 'netCDF'
    }
]
iso_19115_v1_base_simple_record['resource']['transfer_options'] = [
    {
        'online_resource': {
            'href': 'https://ramadda.data.bas.ac.uk/repository/entry/show?entryid='
                    'b1a7d1b5-c419-41e7-9178-b1ffd76d5371',
            'title': 'Get Data',
            'description': 'Download measurement data',
            'function': 'download'
        }
    }
]
iso_19115_v1_base_simple_record['resource']['lineage'] = 'Example lineage statement'

iso_19115_v1_base_complex_record = deepcopy(iso_19115_v1_base_simple_record)
iso_19115_v1_base_complex_record['contacts'][0]['organisation']['href'] = 'http://isni.org/isni/0000000405983800'
iso_19115_v1_base_complex_record['contacts'][0]['organisation']['title'] = 'isni'
iso_19115_v1_base_complex_record['contacts'][0]['online_resource'] = {
    'href': 'https://www.bas.ac.uk/team/business-teams/information-services/uk-polar-data-centre/',
    'function': 'information'
}
iso_19115_v1_base_complex_record['reference_system_info']['code']['href'] = 'http://www.opengis.net/def/crs/EPSG/0/4326'
iso_19115_v1_base_complex_record['reference_system_info']['version'] = '6.18.3'
iso_19115_v1_base_complex_record['reference_system_info']['authority'] = {
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
iso_19115_v1_base_complex_record['resource']['abstract'] = 'Test Record for ISO 19115 metadata standard (no profile) ' \
    'with complex baseline properties only. In this context baseline properties are those that are required, or have ' \
    'default values. Values in this record are complex, meaning they use anchors where relevant rather than simple ' \
    'character strings. Authorities are included in elements that support citations.'
iso_19115_v1_base_complex_record['resource']['contacts'][0]['individual']['href'] = \
    'https://sandbox.orcid.org/0000-0001-8373-6934'
iso_19115_v1_base_complex_record['resource']['contacts'][0]['individual']['title'] = 'orcid'
iso_19115_v1_base_complex_record['resource']['contacts'][0]['online_resource'] = {
    'href': 'https://sandbox.orcid.org/0000-0001-8373-6934',
    'title': 'ORCID record',
    'description': 'ORCID is an open, non-profit, community-driven effort to create and maintain a '
                   'registry of unique researcher identifiers and a transparent method of linking '
                   'research activities and outputs to these identifiers.',
    'function': 'information'
}
iso_19115_v1_base_complex_record['resource']['contacts'][1]['organisation']['href'] = \
    'http://isni.org/isni/0000000405983800'
iso_19115_v1_base_complex_record['resource']['contacts'][1]['organisation']['title'] = 'isni'
iso_19115_v1_base_complex_record['resource']['contacts'][1]['online_resource'] = {
    'href': 'https://www.bas.ac.uk/team/business-teams/information-services/uk-polar-data-centre/',
    'function': 'information'
}
iso_19115_v1_base_complex_record['resource']['keywords'][0]['terms'][0]['href'] = \
    'https://www.eionet.europa.eu/gemet/en/inspire-theme/ac'
iso_19115_v1_base_complex_record['resource']['keywords'][0]['thesaurus'] = {
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
iso_19115_v1_base_complex_record['resource']['constraints']['usage'][0]['copyright_licence']['href'] = \
    'http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/'
iso_19115_v1_base_complex_record['resource']['formats'][0]['href'] = \
    'https://gcmdservices.gsfc.nasa.gov/kms/concept/2b192915-32a8-4b68-a720-8ca8a84f04ca'

iso_19115_v1_complete_record = deepcopy(iso_19115_v1_base_complex_record)
iso_19115_v1_complete_record['resource']['abstract'] = 'Test Record for ISO 19115 metadata standard (no profile) ' \
    'with properties that could typically be included in a record. This does not mean all properties permitted the ' \
    'standard are included, as these are too numerous. Values in this record are complex, meaning they use anchors ' \
    'where relevant rather than simple character strings. Authorities are included in elements that support ' \
    'citations. Identifiers in this record are fake.'
iso_19115_v1_complete_record['resource']['dates'].insert(1, {
    'date': date(2018, 1, 1),
    'date_precision': 'year',
    'date_type': 'revision'
})
iso_19115_v1_complete_record['resource']['dates'].append({
    'date': datetime(2018, 10, 8, 14, 40, 44, tzinfo=timezone.utc),
    'date_type': 'released'
})
iso_19115_v1_complete_record['resource']['edition'] = '2'
iso_19115_v1_complete_record['resource']['identifiers'] = [
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
]
iso_19115_v1_complete_record['resource']['contacts'].insert(1, {
    'individual': {
        'name': 'Cinnamon, John',
        'href': 'https://sandbox.orcid.org/0000-0001-5652-1129',
        'title': 'orcid'
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
})
iso_19115_v1_complete_record['resource']['contacts'].append({
    'organisation': {
        'name': 'Natural Environment Research Council',
        'href': 'http://isni.org/isni/0000000094781573',
        'title': 'isni'
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
})
iso_19115_v1_complete_record['resource']['constraints']['access'][0]['statement'] = \
    'Custom access restrictions statement'
iso_19115_v1_complete_record['resource']['constraints']['usage'].append({
    'required_citation': {
        'statement': 'Cite this information as: "Campbell, S. (2014). Auster Antarctic aircraft. '
                     'University of Alberta Libraries. https://doi.org/10.7939/r3qz22k64"'
    }
})
iso_19115_v1_complete_record['resource']['constraints']['usage'].append({
    'statement': 'Custom use limitations statement'
})
iso_19115_v1_complete_record['resource']['extent']['vertical'] = {
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
}
iso_19115_v1_complete_record['resource']['transfer_options'][0]['size'] = {
                    'unit': 'MB',
                    'magnitude': 40
                }
iso_19115_v1_complete_record['resource']['transfer_options'].append({
    'online_resource': {
        'href': 'https://www.bodc.ac.uk/data/bodc_database/nodb/data_collection/6618/',
        'title': 'View Information',
        'description': 'Download background information and context',
        'function': 'information'
    }
})

# ISO 19115 Standard - Inspire profile

iso_19115_v1_inspire_v1_3_minimal_record = deepcopy(iso_19115_v1_minimal_record)
iso_19115_v1_inspire_v1_3_minimal_record['language'] = 'eng'
iso_19115_v1_inspire_v1_3_minimal_record['hierarchy_level'] = 'dataset'
iso_19115_v1_inspire_v1_3_minimal_record['contacts'][0]['organisation'] = {
    'name': 'UK Polar Data Centre'
}
iso_19115_v1_inspire_v1_3_minimal_record['contacts'][0]['email'] = 'polardatacentre@bas.ac.uk'
iso_19115_v1_inspire_v1_3_minimal_record['resource']['identifiers'] = [
    {
        'identifier': 'https://doi.org/10.5072/r3qz22k64',
        'href': 'https://doi.org/10.5072/r3qz22k64',
        'title': 'doi'
    }
]
iso_19115_v1_inspire_v1_3_minimal_record['resource']['contacts'] = [{
    'organisation': {
        'name': 'UK Polar Data Centre'
    },
    'email': 'polardatacentre@bas.ac.uk',
    'role': [
        'pointOfContact'
    ]
}]
iso_19115_v1_inspire_v1_3_minimal_record['resource']['keywords'] = [
    {
        'terms': [
            {
                'term': 'Atmospheric conditions'
            }
        ],
        'type': 'theme',
        'thesaurus': {
            'title': {
                'value': 'General Multilingual Environmental Thesaurus - INSPIRE themes'
            },
            'dates': [
                {
                    'date': date(2018, 8, 16),
                    'date_type': 'publication'
                }
            ]
        }
    }
]
iso_19115_v1_inspire_v1_3_minimal_record['resource']['constraints'] = {
    'access': [
        {
            'restriction_code': 'otherRestrictions',
            'inspire_limitations_on_public_access': 'noLimitations'
        }
    ],
    'usage': [
        {
            'copyright_licence': {
                'code': 'OGL-UK-3.0',
                'statement': 'This information is licensed under the Open Government Licence v3.0. To view this'
                             ' licence, visit http://www.nationalarchives.gov.uk/doc/open-government-licence/'
            }
        }
    ]
}
iso_19115_v1_inspire_v1_3_minimal_record['resource']['topics'] = [
    "environment"
]
iso_19115_v1_inspire_v1_3_minimal_record['resource']['extent'] = {
    'geographic': {
        'bounding_box': {
            'west_longitude': -45.61521,
            'east_longitude': -27.04976,
            'south_latitude': -68.1511,
            'north_latitude': -54.30761
        }
    }
}
iso_19115_v1_inspire_v1_3_minimal_record['resource']['measures'] = [
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
]
iso_19115_v1_inspire_v1_3_minimal_record['resource']['lineage'] = 'Example lineage statement'

iso_19115_v1_gemini_complete_record = deepcopy(iso_19115_v1_complete_record)
iso_19115_v1_gemini_complete_record['metadata_standard'] = {
    'name': 'ISO 19115 (UK GEMINI)',
    'version': '1.0 (2.3)'
}
iso_19115_v1_gemini_complete_record['resource']['abstract'] = 'Test Record for ISO 19115 metadata standard ' \
    '(Inspire/Gemini profile) with properties that could typically be included in a record. This does not mean all ' \
    'properties permitted the standard are included, as these are too numerous. Values in this record are complex, ' \
    'meaning they use anchors where relevant rather than simple character strings. Authorities are included in ' \
    'elements that support citations. Identifiers in this record are fake.'
iso_19115_v1_gemini_complete_record['resource']['constraints']['access'][0]['inspire_limitations_on_public_access'] = \
    'noLimitations'
iso_19115_v1_gemini_complete_record['resource']['measures'] = [
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
]
