from datetime import datetime, timezone

test_record = {
    'file_identifier': '123',
    'language': 'eng',
    'character_set': 'utf8',
    'hierarchy-level': 'dataset',
    'contact': {
        'organisation': {
            'name': 'UK Polar Data Centre',
            'href': 'http://isni.org/isni/0000000405983800',
            'title': 'ISNI record'
        },
        'phone': '+44 (0)1223 221400',
        'address': {
            'delivery-point': 'British Antarctic Survey, High Cross, Madingley Road',
            'city': 'Cambridge',
            'administrative-area': 'Cambridgeshire',
            'postal-code': 'CB3 0ET',
            'country': 'United Kingdom'
        },
        'email': 'polardatacentre@bas.ac.uk',
        'online-resource': {
            'href': 'https://www.bas.ac.uk/team/business-teams/information-services/uk-polar-data-centre/',
        }
    },
    'date-stamp': datetime(2018, 10, 8, 14, 40, 44, tzinfo=timezone.utc),
    'maintenance': {
        'maintenance-frequency': 'asNeeded',
        'progress': 'completed'
    },
    'metadata-standard': {
        'name': 'ISO 19115 (UK GEMINI)',
        'version': '1.0 (2.3)'
    },
    'reference-system-info': {
        'code': 'urn:ogc:def:crs:EPSG:4326',
        'version': '6.18.3'
    },
    'resource': {
        'title': {
            'value': 'Analysis of d18O and salinity from sea ice and meltwater pool water samples collected in April '
                     '2016 in the Weddell Sea and Scotia Sea of the Southern Ocean during the marine survey JR15006'
        },
        'abstract': 'The dataset contains oxygen stable isotope and salinity measurements from water samples collected '
                    'from sea ice and meltwater pools in April 2016 in the region of South Georgia, Signy and deep '
                    'within the Weddell Sea pack ice during the marine survey JR15006. &#13; The d18O and salinity '
                    'measurements from sea ice and meltwater sources complement the same analysis from CTD casts and '
                    'underway non-toxic flow water system on the RRS James Clark Ross during the JR15006. Establishing '
                    'd18O and salinity values for saline water and oceanic freshwater components can be used to '
                    'identify sources and changes of freshwater contributions to the ocean.&#13;',
        'dates': [
            {
                'date': datetime(2018, 1, 1),
                'date-precision': 'year',
                'date-type': 'creation'
            },
            {
                'date': datetime(2018, 1, 1),
                'date-precision': 'year',
                'date-type': 'revision'
            },
            {
                'date': datetime(2018, 10, 8, 14, 40, 44, tzinfo=timezone.utc),
                'date-type': 'publication'
            },
            {
                'date': datetime(2018, 12, 8, 14, 40, 44, tzinfo=timezone.utc),
                'date-type': 'released'
            }
        ],
        'edition': '1',
        'identifiers': [
            {
                'identifier': 'https://data.bas.ac.uk/metadata.php?id=b1a7d1b5-c419-41e7-9178-b1ffd76d5371'
            },
            {
                'identifier': 'https://doi.org/10.5285/3cf26ab6-7f47-4868-a87d-c62a2eefea1f',
                'href': 'https://doi.org/10.5285/3cf26ab6-7f47-4868-a87d-c62a2eefea1f',
                'title': 'DOI'
            }
        ],
        'contacts': [
            {
                'individual': {
                    'name': 'Michael Meredith',
                    'href': 'https://orcid.org/0000-0002-7342-7756',
                    'title': 'ORCID record'
                },
                'organisation': {
                    'name': 'British Antarctic Survey'
                },
                'email': 'mmm@bas.ac.uk',
                'online-resource': {
                    'href': 'https://orcid.org/0000-0002-7342-7756',
                    'title': 'ORCID record',
                    'description': 'ORCID is an open, non-profit, community-driven effort to create and maintain a '
                                   'registry of unique researcher identifiers and a transparent method of linking '
                                   'research activities and outputs to these identifiers.',
                },
                'role': 'originator'
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
                'email': 'no-reply@bas.ac.uk',
                'online-resource': {
                    'href': 'https://orcid.org/0000-0003-3849-5179',
                    'title': 'ORCID record',
                    'description': 'ORCID is an open, non-profit, community-driven effort to create and maintain a '
                                   'registry of unique researcher identifiers and a transparent method of linking '
                                   'research activities and outputs to these identifiers.',
                },
                'role': 'originator'
            },
            {
                'individual': {
                    'name': 'Melanie Leng',
                    'href': 'https://orcid.org/0000-0003-1115-5166',
                    'title': 'ORCID record'
                },
                'organisation': {
                    'name': 'British Geological Survey'
                },
                'email': 'no-reply@bas.ac.uk',
                'online-resource': {
                    'href': 'https://orcid.org/0000-0003-1115-5166',
                    'title': 'ORCID record',
                    'description': 'ORCID is an open, non-profit, community-driven effort to create and maintain a '
                                   'registry of unique researcher identifiers and a transparent method of linking '
                                   'research activities and outputs to these identifiers.',
                },
                'role': 'originator'
            },
            {
                'organisation': {
                    'name': 'UK Polar Data Centre',
                    'href': 'http://isni.org/isni/0000000405983800',
                    'title': 'ISNI record'
                },
                'phone': '+44 (0)1223 221400',
                'address': {
                    'delivery-point': 'British Antarctic Survey, High Cross, Madingley Road',
                    'city': 'Cambridge',
                    'administrative-area': 'Cambridgeshire',
                    'postal-code': 'CB3 0ET',
                    'country': 'United Kingdom'
                },
                'email': 'polardatacentre@bas.ac.uk',
                'online-resource': {
                    'href': 'https://www.bas.ac.uk/team/business-teams/information-services/uk-polar-data-centre/',
                },
                'role': [
                    'pointOfContact',
                    'custodian',
                    'publisher'
                ]
            }
        ],
        'maintenance': {
            'maintenance-frequency': 'asNeeded',
            'progress': 'completed'
        },
    }
}
