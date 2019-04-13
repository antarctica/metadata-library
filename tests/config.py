from datetime import datetime, timezone

test_record = {
    'file_identifier': '123',
    'language': 'eng',
    'character_set': 'utf8',
    'hierarchy-level': 'dataset',
    'contact': {
        'organisation': {
            'name': 'UK Polar Data Centre'
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
        'url': 'https://www.bas.ac.uk/team/business-teams/information-services/uk-polar-data-centre/'
    },
    'date-stamp': datetime(2018, 10, 8, 14, 40, 44, tzinfo=timezone.utc),
    'metadata-maintenance': {
        'maintenance-frequency': 'asNeeded',
        'progress': 'completed'
    },
    'metadata-standard': {
        'name': 'ISO 19115 (UK GEMINI)',
        'version': '1.0 (2.3)'
    }
}
