from copy import deepcopy
from datetime import datetime, date

# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# We don't currently allow untrusted/user-provided XML so this is not a risk
from typing import Union

from lxml.etree import Element, SubElement  # nosec

from bas_metadata_library import Namespaces as _Namespaces, MetadataRecordConfig as _MetadataRecordConfig, \
    MetadataRecord as _MetadataRecord, MetadataRecordElement as _MetadataRecordElement


# Utility classes


class Utils(object):
    """
    Utility methods
    """
    @staticmethod
    def format_date_string(date_datetime: Union[date, datetime]) -> str:
        """
        Formats a python date or datetime as an ISO 8601 date or datetime string representation

        E.g. Return 'date(2012, 4, 18)' as '2012-04-18' or 'datetime(2012, 4, 18, 22, 48, 56)' as '2012-4-18T22:48:56'.

        :type date_datetime: date/datetime
        :param date_datetime: python date/datetime

        :rtype str
        :return: ISO 8601 formatted date/datetime
        """
        return date_datetime.isoformat()


# Base classes

class Namespaces(_Namespaces):
    """
    Overloaded base Namespaces class

    Defines the namespaces for this standard
    """
    gmd = 'http://www.isotc211.org/2005/gmd'
    gco = 'http://www.isotc211.org/2005/gco'
    gml = 'http://www.opengis.net/gml/3.2'
    gmx = 'http://www.isotc211.org/2005/gmx'
    srv = 'http://www.isotc211.org/2005/srv'
    xlink = 'http://www.w3.org/1999/xlink'
    xsi = 'http://www.w3.org/2001/XMLSchema-instance'

    _schema_locations = {
        'gmd': 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/gmd/gmd.xsd',
        'gco': 'https://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/gco/gco.xsd',
        'gmx': 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/gmx/gmx.xsd',
        'srv': 'http://inspire.ec.europa.eu/draft-schemas/inspire-md-schemas/srv/1.0/srv.xsd'
    }

    def __init__(self):
        self._namespaces = {
            'gmd': self.gmd,
            'gco': self.gco,
            'gml': self.gml,
            'gmx': self.gmx,
            'srv': self.srv,
            'xlink': self.xlink,
            'xsi': self.xsi
        }


class MetadataRecordConfig(_MetadataRecordConfig):
    """
    Overloaded base MetadataRecordConfig class

    Defines the JSON Schema used for this metadata standard
    """
    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)

        self.config = kwargs
        self.schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "UK PDC Metadata Record Generator - ISO 19115 v1 configuration schema",
            "description": "Metadata record configuration schema for the ISO 19115 (v1) metadata standard",
            "definitions": {
                "language": {
                    "type": "string"
                },
                "address": {
                    "type": "object",
                    "required": [],
                    "additionalProperties": False,
                    "properties": {
                        "delivery_point": {
                            "type": "string"
                        },
                        "city": {
                            "type": "string"
                        },
                        "administrative_area": {
                            "type": "string"
                        },
                        "postal_code": {
                            "type": "string"
                        },
                        "country": {
                            "type": "string"
                        }
                    }
                },
                "online_resource": {
                    "type": "object",
                    "required": [
                        "href"
                    ],
                    "additionalProperties": False,
                    "properties": {
                        "href": {
                            "type": "string",
                            "format": "uri"
                        },
                        "title": {
                            "type": "string"
                        },
                        "description": {
                            "type": "string"
                        },
                        "function": {
                            "type": "string",
                            "enum": [
                                "download",
                                "information",
                                "offlineAccess",
                                "order",
                                "search"
                            ]
                        }
                    }
                },
                "contact_identity": {
                    "type": "object",
                    "required": [
                        "name"
                    ],
                    "additionalProperties": False,
                    "properties": {
                        "name": {
                            "type": "string"
                        },
                        "href": {
                            "type": "string",
                            "format": "uri"
                        },
                        "title": {
                            "type": "string"
                        }
                    }
                },
                "contact": {
                    "type": "object",
                    "required": [
                        "role"
                    ],
                    "additionalProperties": False,
                    "properties": {
                        "individual": {
                            "$ref": "#/definitions/contact_identity"
                        },
                        "organisation": {
                            "$ref": "#/definitions/contact_identity"
                        },
                        "email": {
                            "type": "string",
                            "format": "email"
                        },
                        "phone": {
                            "type": "string"
                        },
                        "address": {
                            "$ref": "#/definitions/address"
                        },
                        "online_resource": {
                            "$ref": "#/definitions/online_resource"
                        },
                        "role": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": [
                                    "author",
                                    "custodian",
                                    "distributor",
                                    "originator",
                                    "owner",
                                    "pointOfContact",
                                    "principalInvestigator",
                                    "processor",
                                    "publisher",
                                    "resourceProvider",
                                    "sponsor",
                                    "user",
                                    "coAuthor",
                                    "collaborator",
                                    "contributor",
                                    "editor",
                                    "funder",
                                    "mediator",
                                    "rightsHolder",
                                    "stakeholder"
                                ]
                            }
                        }
                    }
                },
                "maintenance": {
                    "type": "object",
                    "required": [],
                    "additionalProperties": False,
                    "properties": {
                        "maintenance_frequency": {
                            "type": "string",
                            "enum": [
                                "continual",
                                "daily",
                                "weekly",
                                "fortnightly",
                                "monthly",
                                "quarterly",
                                "biannually",
                                "annually",
                                "asNeeded",
                                "irregular",
                                "notPlanned",
                                "unknown"
                            ]
                        },
                        "progress": {
                            "type": "string",
                            "enum": [
                                "completed",
                                "historicalArchive",
                                "obsolete",
                                "onGoing",
                                "planned",
                                "required",
                                "underDevelopment"
                            ]
                        }
                    }
                },
                "title": {
                    "type": "object",
                    "required": [
                        "value"
                    ],
                    "additionalProperties": False,
                    "properties": {
                        "value": {
                            "type": "string"
                        }
                    }
                },
                "dates": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": [
                            "date",
                            "date_type"
                        ],
                        "additionalProperties": False,
                        "properties": {
                            "date": {
                                "$ref": "#/definitions/date"
                            },
                            "date_precision": {
                                "type": "string",
                                "enum": [
                                    "month",
                                    "year"
                                ]
                            },
                            "date_type": {
                                "type": "string",
                                "enum": [
                                    "creation",
                                    "publication",
                                    "revision",
                                    "adopted",
                                    "deprecated",
                                    "distribution",
                                    "expiry",
                                    "inForce",
                                    "lastRevision",
                                    "lastUpdate",
                                    "nextUpdate",
                                    "released",
                                    "superseded",
                                    "unavailable",
                                    "validityBegins",
                                    "validityExpires"
                                ]
                            }
                        }
                    }
                },
                "date": {
                    "type": "string",
                    "format": "date-time"
                },
                "edition": {
                    "type": "string"
                },
                "identifier": {
                    "type": "object",
                    "required": [],
                    "additionalProperties": False,
                    "properties": {
                        "identifier": {
                            "type": "string"
                        },
                        "href": {
                            "type": "string",
                            "format": "uri"
                        },
                        "title": {
                            "type": "string"
                        }
                    }
                },
                "keywords": {
                    "type": "object",
                    "required": [
                        "terms"
                    ],
                    "additionalProperties": False,
                    "properties": {
                        "terms": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": [
                                    "term"
                                ],
                                "additionalProperties": False,
                                "properties": {
                                    "term": {
                                        "type": "string"
                                    },
                                    "href": {
                                        "type": "string",
                                        "format": "uri"
                                    }
                                }
                            }
                        },
                        "type": {
                            "type": "string",
                            "enum": [
                                "discipline",
                                "place",
                                "stratum",
                                "temporal",
                                "theme"
                            ]
                        },
                        "thesaurus": {
                            "$ref": "#/definitions/thesaurus"
                        }
                    }
                },
                "thesaurus": {
                    "type": "object",
                    "required": [],
                    "additionalProperties": False,
                    "properties": {
                        "title": {
                            "anyOf": [
                                {"$ref": "#/definitions/title"},
                                {
                                    "properties": {
                                        "href": {
                                            "type": "string",
                                            "format": "uri"
                                        }
                                    }
                                }
                            ]
                        },
                        "dates": {
                            "$ref": "#/definitions/dates"
                        },
                        "edition": {
                            "$ref": "#/definitions/edition"
                        },
                        "contact": {
                            "$ref": "#/definitions/contact"
                        }
                    }
                },
                "constraint": {
                    "type": "object",
                    "required": [],
                    "additionalProperties": False,
                    "properties": {
                        "restriction_code": {
                            "type": "string",
                            "enum": [
                                "copyright",
                                "patent",
                                "patentPending",
                                "trademark",
                                "license",
                                "intellectualPropertyRights",
                                "restricted",
                                "otherRestrictions"
                            ]
                        },
                        "inspire_limitations_on_public_access": {
                            "type": "string",
                            "enum": [
                                "noLimitations"
                            ]
                        },
                        "copyright_licence": {
                            "type": "object",
                            "required": [],
                            "additionalProperties": False,
                            "properties": {
                                "code": {
                                    "type": "string"
                                },
                                "href": {
                                    "type": "string",
                                    "format": "uri"
                                },
                                "statement": {
                                    "type": "string"
                                }
                            }
                        },
                        "required_citation": {
                            "type": "string"
                        }
                    }
                },
                "geographic_extent": {
                    "type": "object",
                    "required": [],
                    "additionalProperties": False,
                    "properties": {
                        "bounding_box": {
                            "type": "object",
                            "required": [],
                            "additionalProperties": False,
                            "properties": {
                                "west_longitude": {
                                    "type": "number",
                                    "maximum": 180,
                                    "minimum": -180
                                },
                                "east_longitude": {
                                    "type": "number",
                                    "maximum": 180,
                                    "minimum": -180
                                },
                                "south_latitude": {
                                    "type": "number",
                                    "maximum": 90,
                                    "minimum": -90
                                },
                                "north_latitude": {
                                    "type": "number",
                                    "maximum": 90,
                                    "minimum": -90
                                }
                            }
                        }
                    }
                },
                "vertical_extent": {
                    "type": "object",
                    "required": [],
                    "additionalProperties": False,
                    "properties": {
                        "minimum": {
                            "type": "number"
                        },
                        "maximum": {
                            "type": "number"
                        },
                        "identifier": {
                            "type": "string"
                        },
                        "code": {
                            "type": "string"
                        },
                        "name": {
                            "type": "string"
                        },
                        "remarks": {
                            "type": "string"
                        },
                        "scope": {
                            "type": "string"
                        },
                        "domain_of_validity": {
                            "type": "object",
                            "required": [],
                            "additionalProperties": False,
                            "properties": {
                                "href": {
                                    "type": "string",
                                    "format": "uri"
                                }
                            }
                        },
                        "vertical_cs": {
                            "type": "object",
                            "required": [],
                            "additionalProperties": False,
                            "properties": {
                                "href": {
                                    "type": "string",
                                    "format": "uri"
                                }
                            }
                        },
                        "vertical_datum": {
                            "type": "object",
                            "required": [],
                            "additionalProperties": False,
                            "properties": {
                                "href": {
                                    "type": "string",
                                    "format": "uri"
                                }
                            }
                        }
                    }
                },
                "temporal_extent": {
                    "type": "object",
                    "required": [],
                    "additionalProperties": False,
                    "properties": {
                        "period": {
                            "type": "object",
                            "required": [],
                            "additionalProperties": False,
                            "properties": {
                                "start": {
                                    "$ref": "#/definitions/date"
                                },
                                "end": {
                                    "$ref": "#/definitions/date"
                                }
                            }
                        }
                    }
                }
            },
            "type": "object",
            "required": [
                "contacts",
                "date_stamp",
                "resource"
            ],
            "additionalProperties": False,
            "properties": {
                "file_identifier": {
                    "type": "string"
                },
                "language": {
                    "$ref": "#/definitions/language"
                },
                "character_set": {
                    "type": "string"
                },
                "hierarchy_level": {
                    "type": "string",
                    "enum": [
                        "attribute",
                        "attributeType",
                        "collectionHardware",
                        "collectionSession",
                        "dataset",
                        "series",
                        "nonGeographicDataset",
                        "dimensionGroup",
                        "feature",
                        "featureType",
                        "propertyType",
                        "fieldSession",
                        "software",
                        "service",
                        "model",
                        "tile"
                    ]
                },
                "contacts": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/contact"
                    },
                    "minimum": 1
                },
                "date_stamp": {
                    "type": "string",
                    "format": "date-time"
                },
                "maintenance": {
                    "$ref": "#/definitions/maintenance"
                },
                "metadata_standard": {
                    "type": "object",
                    "required": [],
                    "additionalProperties": False,
                    "properties": {
                        "name": {
                            "type": "string"
                        },
                        "version": {
                            "type": "string"
                        }
                    }
                },
                "reference_system_info": {
                    "type": "object",
                    "required": [
                        "code"
                    ],
                    "additionalProperties": False,
                    "properties": {
                        "code": {
                            "type": "object",
                            "required": [
                                "value"
                            ],
                            "additionalProperties": False,
                            "properties": {
                                "value": {
                                    "type": "string"
                                },
                                "href": {
                                    "type": "string",
                                    "format": "uri"
                                }
                            }
                        },
                        "version": {
                            "type": "string"
                        },
                        "authority": {
                            "type": "object",
                            "required": [],
                            "additionalProperties": False,
                            "properties": {
                                "title": {
                                    "$ref": "#/definitions/title"
                                },
                                "dates": {
                                    "$ref": "#/definitions/dates"
                                },
                                "contact": {
                                    "$ref": "#/definitions/contact"
                                }
                            }
                        }
                    }
                },
                "resource": {
                    "type": "object",
                    "required": [
                        "title",
                        "dates",
                        "abstract",
                        "language"
                    ],
                    "additionalProperties": False,
                    "properties": {
                        "title": {
                            "$ref": "#/definitions/title"
                        },
                        "abstract": {
                            "type": "string"
                        },
                        "dates": {
                            "$ref": "#/definitions/dates"
                        },
                        "edition": {
                            "$ref": "#/definitions/edition"
                        },
                        "identifiers": {
                            "type": "array",
                            "items": {
                                "$ref": "#/definitions/identifier"
                            }
                        },
                        "contacts": {
                            "type": "array",
                            "items": {
                                "$ref": "#/definitions/contact"
                            }
                        },
                        "maintenance": {
                            "$ref": "#/definitions/maintenance"
                        },
                        "keywords": {
                            "type": "array",
                            "items": {
                                "$ref": "#/definitions/keywords"
                            }
                        },
                        "constraints": {
                            "type": "object",
                            "required": [],
                            "additionalProperties": False,
                            "properties": {
                                "access": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/definitions/constraint"
                                    }
                                },
                                "usage": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/definitions/constraint"
                                    }
                                }
                            }
                        },
                        "supplemental_information": {
                            "type": "string"
                        },
                        "spatial_representation_type": {
                            "type": "string",
                            "enum": [
                                "vector",
                                "grid",
                                "textTable",
                                "tin",
                                "steroModel",
                                "video"
                            ]
                        },
                        "spatial_resolution": {
                            "type": ["string", "null"]
                        },
                        "language": {
                            "$ref": "#/definitions/language"
                        },
                        "topics": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": [
                                    "farming",
                                    "biota",
                                    "boundaries",
                                    "climatologyMeteorologyAtmosphere",
                                    "economy",
                                    "elevation",
                                    "environment",
                                    "geoscientificInformation",
                                    "health",
                                    "imageryBaseMapsEarthCover",
                                    "intelligenceMilitary",
                                    "inlandWaters",
                                    "location",
                                    "oceans",
                                    "planningCadastre",
                                    "society",
                                    "structure",
                                    "transportation",
                                    "utilitiesCommunication",
                                    "extraTerrestrial",
                                    "disaster"
                                ]
                            }
                        },
                        "extent": {
                            "type": "object",
                            "required": [],
                            "additionalProperties": False,
                            "properties": {
                                "geographic": {
                                    "$ref": "#/definitions/geographic_extent"
                                },
                                "vertical": {
                                    "$ref": "#/definitions/vertical_extent"
                                },
                                "temporal": {
                                    "$ref": "#/definitions/temporal_extent"
                                }
                            }
                        },
                        "formats": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": [
                                    "format"
                                ],
                                "additionalProperties": False,
                                "properties": {
                                    "format": {
                                        "type": "string"
                                    },
                                    "href": {
                                        "type": "string",
                                        "format": "uri"
                                    }
                                }
                            }
                        },
                        "transfer_options": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": [
                                    "online_resource"
                                ],
                                "additionalProperties": False,
                                "properties": {
                                    "size": {
                                        "type": "object",
                                        "additionalProperties": False,
                                        "required": [],
                                        "properties": {
                                            "unit": {
                                                "type": "string"
                                            },
                                            "magnitude": {
                                                "type": "number"
                                            }
                                        }
                                    },
                                    "online_resource": {
                                        "$ref": "#/definitions/online_resource"
                                    }
                                }
                            }
                        },
                        "measures": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": [],
                                "additionalProperties": False,
                                "properties": {
                                    "code": {
                                        "type": "string"
                                    },
                                    "code_space": {
                                        "type": "string"
                                    },
                                    "pass": {
                                        "type": "boolean"
                                    },
                                    "title": {
                                        "anyOf": [
                                            {"$ref": "#/definitions/title"},
                                            {
                                                "properties": {
                                                    "href": {
                                                        "type": "string",
                                                        "format": "uri"
                                                    }
                                                }
                                            }
                                        ]
                                    },
                                    "dates": {
                                        "$ref": "#/definitions/dates"
                                    },
                                    "explanation": {
                                        "type": "string"
                                    }
                                }
                            }
                        },
                        "lineage": {
                            "type": "string"
                        }
                    }
                }
            }
        }

        self.validate()


class MetadataRecord(_MetadataRecord):
    """
    Overloaded base MetadataRecordConfig class

    Defines the root element, and it's sub-elements, for this metadata standard
    """
    def __init__(self, configuration: MetadataRecordConfig):
        self.ns = Namespaces()
        self.attributes = configuration.config
        self.record = self.make_element()

    def make_element(self) -> Element:
        metadata_record = Element(
            f"{{{self.ns.gmd}}}MD_Metadata",
            attrib={f"{{{ self.ns.xsi }}}schemaLocation": self.ns.schema_locations()},
            nsmap=self.ns.nsmap()
        )

        identifier = FileIdentifier(
            record=metadata_record,
            attributes=self.attributes,
            parent_element=metadata_record
        )
        identifier.make_element()

        if 'language' in self.attributes:
            language = Language(
                record=metadata_record,
                attributes=self.attributes
            )
            language.make_element()

        if 'character_set' in self.attributes:
            character_set = CharacterSet(
                record=metadata_record,
                attributes=self.attributes
            )
            character_set.make_element()

        if 'hierarchy_level' in self.attributes:
            hierarchy_level = HierarchyLevel(
                record=metadata_record,
                attributes=self.attributes
            )
            hierarchy_level.make_element()

        for contact_attributes in self.attributes['contacts']:
            for role in contact_attributes['role']:
                _contact = contact_attributes.copy()
                _contact['role'] = role

                contact = Contact(
                    record=metadata_record,
                    attributes=self.attributes,
                    parent_element=metadata_record,
                    element_attributes=_contact
                )
                contact.make_element()

        date_stamp = DateStamp(
            record=metadata_record,
            attributes=self.attributes
        )
        date_stamp.make_element()

        if 'maintenance' in self.attributes:
            metadata_maintenance = MetadataMaintenance(
                record=metadata_record,
                attributes=self.attributes,
                parent_element=metadata_record,
                element_attributes=self.attributes['maintenance']
            )
            metadata_maintenance.make_element()

        if 'metadata_standard' in self.attributes:
            metadata_standard = MetadataStandard(
                record=metadata_record,
                attributes=self.attributes,
                parent_element=metadata_record,
                element_attributes=self.attributes['metadata_standard']
            )
            metadata_standard.make_element()

        if 'reference_system_info' in self.attributes:
            reference_system_info = ReferenceSystemInfo(
                record=metadata_record,
                attributes=self.attributes,
                parent_element=metadata_record,
                element_attributes=self.attributes['reference_system_info']
            )
            reference_system_info.make_element()

        data_identification = DataIdentification(
            record=metadata_record,
            attributes=self.attributes
        )
        data_identification.make_element()

        if 'formats' in self.attributes['resource'] or 'transfer_options' in self.attributes['resource']:
            data_distribution = DataDistribution(
                record=metadata_record,
                attributes=self.attributes
            )
            data_distribution.make_element()

        if 'measures' in self.attributes['resource'] or 'lineage' in self.attributes['resource']:
            data_quality = DataQuality(
                record=metadata_record,
                attributes=self.attributes
            )
            data_quality.make_element()

        return metadata_record


class MetadataRecordElement(_MetadataRecordElement):
    """
    Overloaded base MetadataRecordElement class

    Sets the type hint of the record attribute to the MetadataRecord class for this metadata standard
    """
    def __init__(
        self,
        record: _MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.ns = Namespaces()


class CodeListElement(MetadataRecordElement):
    """
    Derived MetadataRecordElement class defining an ISO code list element
    """
    def __init__(
        self,
        record: _MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.code_list_values = []
        self.code_list = None
        self.element = None
        self.element_code = None
        self.attribute = None

    def make_element(self):
        code_list_element = SubElement(self.parent_element, self.element)
        if self.attribute in self.element_attributes \
                and self.element_attributes[self.attribute] in self.code_list_values:
            code_list_value = SubElement(
                code_list_element,
                self.element_code,
                attrib={
                    'codeList': self.code_list,
                    'codeListValue': self.element_attributes[self.attribute]
                }
            )
            code_list_value.text = self.element_attributes[self.attribute]


# Element Classes


class FileIdentifier(MetadataRecordElement):
    def make_element(self):
        if 'file_identifier' in self.attributes:
            file_identifier_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}fileIdentifier")
            file_identifier_value = SubElement(file_identifier_element, f"{{{self.ns.gco}}}CharacterString")
            file_identifier_value.text = self.attributes['file_identifier']


class Language(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.code_list_values = ['eng']
        self.code_list = 'http://www.loc.gov/standards/iso639-2/php/code_list.php'
        self.element = f"{{{self.ns.gmd}}}language"
        self.element_code = f"{{{self.ns.gmd}}}LanguageCode"
        self.attribute = 'language'


class CharacterSet(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.code_list_values = ['utf8']
        self.code_list = 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/' \
                         'codelist/gmxCodelists.xml#MD_CharacterSetCode'
        self.element = f"{{{self.ns.gmd}}}characterSet"
        self.element_code = f"{{{self.ns.gmd}}}MD_CharacterSetCode"
        self.attribute = 'character_set'


class ScopeCode(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.code_list_values = [
            'attribute',
            'attributeType',
            'collectionHardware',
            'collectionSession',
            'dataset',
            'series',
            'nonGeographicDataset',
            'dimensionGroup',
            'feature',
            'featureType',
            'propertyType',
            'fieldSession',
            'software',
            'service',
            'model',
            'tile'
        ]
        self.code_list = 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/' \
                         'codelist/gmxCodelists.xml#MD_ScopeCode'
        self.element = f"{{{self.ns.gmd}}}level"
        self.element_code = f"{{{self.ns.gmd}}}MD_ScopeCode"
        self.attribute = 'hierarchy_level'


class HierarchyLevel(ScopeCode):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.element = f"{{{self.ns.gmd}}}hierarchyLevel"

    def make_element(self):
        super().make_element()
        hierarchy_level_name_element = SubElement(self.record, f"{{{self.ns.gmd}}}hierarchyLevelName")
        if self.attribute in self.attributes and self.attributes[self.attribute] in self.code_list_values:
            hierarchy_level_name_value = SubElement(
                hierarchy_level_name_element,
                f"{{{self.ns.gco}}}CharacterString"
            )
            hierarchy_level_name_value.text = self.attributes[self.attribute]


class Contact(MetadataRecordElement):
    def make_element(self):
        contact_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}contact")

        responsible_party = ResponsibleParty(
            record=self.record,
            attributes=self.attributes,
            parent_element=contact_element,
            element_attributes=self.element_attributes
        )
        responsible_party.make_element()


class ResponsibleParty(MetadataRecordElement):
    def make_element(self):
        responsible_party_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}CI_ResponsibleParty")

        if 'individual' in self.element_attributes and 'name' in self.element_attributes['individual']:
            individual_element = SubElement(responsible_party_element, f"{{{self.ns.gmd}}}individualName")
            if 'href' in self.element_attributes['individual']:
                anchor = AnchorElement(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=individual_element,
                    element_attributes=self.element_attributes['individual'],
                    element_value=self.element_attributes['individual']['name']
                )
                anchor.make_element()
            else:
                individual_value = SubElement(individual_element, f"{{{self.ns.gco}}}CharacterString")
                individual_value.text = self.element_attributes['individual']['name']

        if 'organisation' in self.element_attributes and 'name' in self.element_attributes['organisation']:
            organisation_element = SubElement(responsible_party_element, f"{{{self.ns.gmd}}}organisationName")
            if 'href' in self.element_attributes['organisation']:
                anchor = AnchorElement(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=organisation_element,
                    element_attributes=self.element_attributes['organisation'],
                    element_value=self.element_attributes['organisation']['name']
                )
                anchor.make_element()
            else:
                organisation_name_value = SubElement(
                    organisation_element,
                    f"{{{self.ns.gco}}}CharacterString"
                )
                organisation_name_value.text = self.element_attributes['organisation']['name']

        if 'phone' in self.element_attributes or 'address' in self.element_attributes \
                or 'email' in self.element_attributes or 'online_resource' in self.element_attributes:
            contact_wrapper = SubElement(responsible_party_element, f"{{{self.ns.gmd}}}contactInfo")
            contact_element = SubElement(contact_wrapper, f"{{{self.ns.gmd}}}CI_Contact")

            if 'phone' in self.element_attributes:
                phone_wrapper = SubElement(contact_element, f"{{{self.ns.gmd}}}phone")
                phone_element = SubElement(phone_wrapper, f"{{{self.ns.gmd}}}CI_Telephone")
                phone_voice = SubElement(phone_element, f"{{{self.ns.gmd}}}voice")
                phone_voice_value = SubElement(phone_voice, f"{{{self.ns.gco}}}CharacterString")
                phone_voice_value.text = self.element_attributes['phone']

            if 'address' in self.element_attributes or 'email' in self.element_attributes:
                address_wrapper = SubElement(contact_element, f"{{{self.ns.gmd}}}address")
                address_element = SubElement(address_wrapper, f"{{{self.ns.gmd}}}CI_Address")

                if 'address' in self.element_attributes:
                    if 'delivery_point' in self.element_attributes['address']:
                        delivery_point_element = SubElement(address_element, f"{{{self.ns.gmd}}}deliveryPoint")
                        delivery_point_value = SubElement(
                            delivery_point_element,
                            f"{{{self.ns.gco}}}CharacterString"
                        )
                        delivery_point_value.text = self.element_attributes['address']['delivery_point']
                    if 'city' in self.element_attributes['address']:
                        city_element = SubElement(address_element, f"{{{self.ns.gmd}}}city")
                        city_value = SubElement(city_element, f"{{{self.ns.gco}}}CharacterString")
                        city_value.text = self.element_attributes['address']['city']
                    if 'administrative_area' in self.element_attributes['address']:
                        administrative_area_element = SubElement(
                            address_element,
                            f"{{{self.ns.gmd}}}administrativeArea"
                        )
                        administrative_area_value = SubElement(
                            administrative_area_element,
                            f"{{{self.ns.gco}}}CharacterString"
                        )
                        administrative_area_value.text = self.element_attributes['address']['administrative_area']
                    if 'postal_code' in self.element_attributes['address']:
                        postal_code_element = SubElement(address_element, f"{{{self.ns.gmd}}}postalCode")
                        postal_code_value = SubElement(postal_code_element, f"{{{self.ns.gco}}}CharacterString")
                        postal_code_value.text = self.element_attributes['address']['postal_code']
                    if 'country' in self.element_attributes['address']:
                        country_element = SubElement(address_element, f"{{{self.ns.gmd}}}country")
                        country_value = SubElement(country_element, f"{{{self.ns.gco}}}CharacterString")
                        country_value.text = self.element_attributes['address']['country']

                if 'email' in self.element_attributes:
                    email_element = SubElement(address_element, f"{{{self.ns.gmd}}}electronicMailAddress")
                    email_value = SubElement(email_element, f"{{{self.ns.gco}}}CharacterString")
                    email_value.text = self.element_attributes['email']
                else:
                    SubElement(
                        address_element,
                        f"{{{self.ns.gmd}}}electronicMailAddress",
                        attrib={f"{{{self.ns.gco}}}nilReason": 'unknown'}
                    )

            if 'online_resource' in self.element_attributes:
                online_resource_wrapper = SubElement(
                    contact_element,
                    f"{{{self.ns.gmd}}}onlineResource"
                )
                online_resource = OnlineResource(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=online_resource_wrapper,
                    element_attributes=self.element_attributes['online_resource']
                )
                online_resource.make_element()

        if 'role' in self.element_attributes:
            role = Role(
                record=self.record,
                attributes=self.attributes,
                parent_element=responsible_party_element,
                element_attributes=self.element_attributes
            )
            role.make_element()


class OnlineResource(MetadataRecordElement):
    def make_element(self):
        online_resource_element = SubElement(
            self.parent_element,
            f"{{{self.ns.gmd}}}CI_OnlineResource"
        )

        if 'href' in self.element_attributes:
            linkage = Linkage(
                record=self.record,
                attributes=self.attributes,
                parent_element=online_resource_element,
                element_attributes=self.element_attributes
            )
            linkage.make_element()

        if 'title' in self.element_attributes:
            title_wrapper = SubElement(online_resource_element, f"{{{self.ns.gmd}}}name")
            title_element = SubElement(title_wrapper, f"{{{self.ns.gco}}}CharacterString")
            title_element.text = self.element_attributes['title']

        if 'description' in self.element_attributes:
            title_wrapper = SubElement(online_resource_element, f"{{{self.ns.gmd}}}description")
            title_element = SubElement(title_wrapper, f"{{{self.ns.gco}}}CharacterString")
            title_element.text = self.element_attributes['description']

        if 'function' in self.element_attributes:
            function = OnlineRole(
                record=self.record,
                attributes=self.attributes,
                parent_element=online_resource_element,
                element_attributes=self.element_attributes
            )
            function.make_element()


class Linkage(MetadataRecordElement):
    def make_element(self):
        linkage_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}linkage")
        if 'href' in self.element_attributes:
            url_value = SubElement(linkage_element, f"{{{self.ns.gmd}}}URL")
            url_value.text = self.element_attributes['href']


class Role(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.code_list_values = [
            "author",
            "custodian",
            "distributor",
            "originator",
            "owner",
            "pointOfContact",
            "principalInvestigator",
            "processor",
            "publisher",
            "resourceProvider",
            "sponsor",
            "user",
            "coAuthor",
            "collaborator",
            "contributor",
            "editor",
            "funder",
            "mediator",
            "rightsHolder",
            "stakeholder"
        ]
        self.code_list = 'https://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#CI_RoleCode'
        self.element = f"{{{self.ns.gmd}}}role"
        self.element_code = f"{{{self.ns.gmd}}}CI_RoleCode"
        self.attribute = 'role'


class OnlineRole(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.code_list_values = [
            'download',
            'information',
            'offlineAccess',
            'order',
            'search'
        ]
        self.code_list = 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/' \
                         'codelist/gmxCodelists.xml#CI_OnLineFunctionCode'
        self.element = f"{{{self.ns.gmd}}}function"
        self.element_code = f"{{{self.ns.gmd}}}CI_OnLineFunctionCode"
        self.attribute = 'function'


class DateStamp(MetadataRecordElement):
    def make_element(self):
        date_stamp_element = SubElement(self.record, f"{{{self.ns.gmd}}}dateStamp")
        date_stamp_value = SubElement(date_stamp_element, f"{{{self.ns.gco}}}DateTime")
        date_stamp_value.text = Utils.format_date_string(self.attributes['date_stamp'])


class MetadataMaintenance(MetadataRecordElement):
    def make_element(self):
        if 'maintenance' in self.attributes:
            metadata_maintenance_element = SubElement(
                self.parent_element,
                f"{{{self.ns.gmd}}}metadataMaintenance"
            )

            maintenance_information = MaintenanceInformation(
                record=self.record,
                attributes=self.attributes,
                parent_element=metadata_maintenance_element,
                element_attributes=self.attributes['maintenance']
            )
            maintenance_information.make_element()


class MaintenanceInformation(MetadataRecordElement):
    def make_element(self):
        maintenance_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}MD_MaintenanceInformation")

        if 'maintenance_frequency' in self.element_attributes:
            maintenance_and_update_frequency = MaintenanceAndUpdateFrequency(
                record=self.record,
                attributes=self.attributes,
                parent_element=maintenance_element,
                element_attributes=self.element_attributes
            )
            maintenance_and_update_frequency.make_element()

        if 'progress' in self.element_attributes:
            maintenance_process = MaintenanceProgress(
                record=self.record,
                attributes=self.attributes,
                parent_element=maintenance_element,
                element_attributes=self.element_attributes
            )
            maintenance_process.make_element()


class MaintenanceAndUpdateFrequency(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.code_list_values = [
            'continual',
            'daily',
            'weekly',
            'fortnightly',
            'monthly',
            'quarterly',
            'biannually',
            'annually',
            'asNeeded',
            'irregular',
            'notPlanned',
            'unknown'
        ]
        self.code_list = 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/' \
                         'codelist/gmxCodelists.xml#MD_MaintenanceFrequencyCode'
        self.element = f"{{{self.ns.gmd}}}maintenanceAndUpdateFrequency"
        self.element_code = f"{{{self.ns.gmd}}}MD_MaintenanceFrequencyCode"
        self.attribute = 'maintenance_frequency'


class MaintenanceProgress(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.code_list_values = [
            'completed',
            'historicalArchive',
            'obsolete',
            'onGoing',
            'planned',
            'required',
            'underDevelopment'
        ]
        self.code_list = 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/' \
                         'codelist/gmxCodelists.xml#MD_ProgressCode'
        self.element = f"{{{self.ns.gmd}}}maintenanceNote"
        self.element_code = f"{{{self.ns.gmd}}}MD_ProgressCode"
        self.attribute = 'progress'


class MetadataStandard(MetadataRecordElement):
    def make_element(self):
        if 'name' in self.element_attributes:
            metadata_standard_name_element = SubElement(
                self.parent_element,
                f"{{{self.ns.gmd}}}metadataStandardName"
            )
            metadata_standard_name_value = SubElement(
                metadata_standard_name_element,
                f"{{{self.ns.gco}}}CharacterString"
            )
            metadata_standard_name_value.text = self.element_attributes['name']

        if 'version' in self.element_attributes:
            metadata_standard_version_element = SubElement(
                self.parent_element,
                f"{{{self.ns.gmd}}}metadataStandardVersion"
            )
            metadata_standard_version_value = SubElement(
                metadata_standard_version_element,
                f"{{{self.ns.gco}}}CharacterString"
            )
            metadata_standard_version_value.text = self.element_attributes['version']


class ReferenceSystemInfo(MetadataRecordElement):
    def make_element(self):
        reference_system_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}referenceSystemInfo")
        reference_system_element = SubElement(reference_system_wrapper, f"{{{self.ns.gmd}}}MD_ReferenceSystem")
        reference_system_identifier_wrapper = SubElement(
            reference_system_element,
            f"{{{self.ns.gmd}}}referenceSystemIdentifier"
        )
        reference_system_identifier_element = SubElement(
            reference_system_identifier_wrapper,
            f"{{{self.ns.gmd}}}RS_Identifier"
        )

        if 'authority' in self.element_attributes:
            reference_system_identifier_authority_element = SubElement(
                reference_system_identifier_element,
                f"{{{self.ns.gmd}}}authority"
            )
            citation = Citation(
                record=self.record,
                attributes=self.attributes,
                parent_element=reference_system_identifier_authority_element,
                element_attributes=self.element_attributes['authority']
            )
            citation.make_element()

        if 'code' in self.element_attributes:
            reference_system_identifier_code_element = SubElement(
                reference_system_identifier_element,
                f"{{{self.ns.gmd}}}code"
            )
            if 'href' in self.element_attributes['code']:
                anchor = AnchorElement(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=reference_system_identifier_code_element,
                    element_attributes=self.element_attributes['code'],
                    element_value=self.element_attributes['code']['value']
                )
                anchor.make_element()
            else:
                reference_system_identifier_code_value = SubElement(
                    reference_system_identifier_code_element,
                    f"{{{self.ns.gco}}}CharacterString"
                )
                reference_system_identifier_code_value.text = self.element_attributes['code']['value']

        if 'version' in self.element_attributes:
            reference_system_identifier_version_element = SubElement(
                reference_system_identifier_element,
                f"{{{self.ns.gmd}}}version"
            )
            reference_system_identifier_version_value = SubElement(
                reference_system_identifier_version_element,
                f"{{{self.ns.gco}}}CharacterString"
            )
            reference_system_identifier_version_value.text = self.element_attributes['version']


class Citation(MetadataRecordElement):
    def make_element(self):
        citation_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}CI_Citation")

        if 'title' in self.element_attributes:
            title_element = SubElement(citation_element, f"{{{self.ns.gmd}}}title")
            if 'href' in self.element_attributes['title']:
                anchor = AnchorElement(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=title_element,
                    element_attributes=self.element_attributes['title'],
                    element_value=self.element_attributes['title']['value']
                )
                anchor.make_element()
            else:
                title_value = SubElement(title_element, f"{{{self.ns.gco}}}CharacterString")
                title_value.text = self.element_attributes['title']['value']

        if 'dates' in self.element_attributes:
            for date_attributes in self.element_attributes['dates']:
                citation_date = Date(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=citation_element,
                    element_attributes=date_attributes
                )
                citation_date.make_element()

        if 'edition' in self.element_attributes:
            edition_element = SubElement(citation_element, f"{{{self.ns.gmd}}}edition")
            edition_value = SubElement(edition_element, f"{{{self.ns.gco}}}CharacterString")
            edition_value.text = str(self.element_attributes['edition'])

        if 'identifiers' in self.element_attributes:
            for identifier_attributes in self.element_attributes['identifiers']:
                identifier = Identifier(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=citation_element,
                    element_attributes=identifier_attributes
                )
                identifier.make_element()

        if 'contact' in self.element_attributes:
            citated_responsible_party_element = SubElement(
                citation_element,
                f"{{{self.ns.gmd}}}citedResponsibleParty"
            )

            # Citations can only have a single contact so collapse roles array down to a single value
            _contact_element_attributes = self.element_attributes['contact']
            if type(self.element_attributes['contact']['role']) is list:
                if len(self.element_attributes['contact']['role']) > 1:
                    raise ValueError('Contacts can only have a single role. Citations can only have a single contact.')
                _contact_element_attributes = deepcopy(self.element_attributes['contact'])
                _contact_element_attributes['role'] = _contact_element_attributes['role'][0]

            responsible_party = ResponsibleParty(
                record=self.record,
                attributes=self.attributes,
                parent_element=citated_responsible_party_element,
                element_attributes=_contact_element_attributes
            )
            responsible_party.make_element()


class Date(MetadataRecordElement):
    def make_element(self):
        date_container_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}date")
        date_container_element = SubElement(date_container_wrapper, f"{{{self.ns.gmd}}}CI_Date")

        date_element = SubElement(date_container_element, f"{{{self.ns.gmd}}}date")

        date_value_element = f"{{{self.ns.gco}}}Date"
        if type(self.element_attributes['date']) is datetime:
            date_value_element = f"{{{self.ns.gco}}}DateTime"

        date_value = SubElement(date_element, date_value_element)
        date_value.text = Utils.format_date_string(self.element_attributes['date'])

        if 'date_precision' in self.element_attributes:
            if self.element_attributes['date_precision'] == 'year':
                date_value.text = str(self.element_attributes['date'].year)

        date_type = DateType(
            record=self.record,
            attributes=self.attributes,
            parent_element=date_container_element,
            element_attributes=self.element_attributes
        )
        date_type.make_element()


class DateType(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.code_list_values = [
            'creation',
            'publication',
            'revision',
            'expiry',
            'lastUpdate',
            'lastRevision',
            'nextUpdate',
            'unavailable',
            'inForce',
            'adopted',
            'deprecated',
            'superseded',
            'validityBegins',
            'validityExpires',
            'released',
            'distribution'
        ]
        self.code_list = 'https://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#CI_DateTypeCode'
        self.element = f"{{{self.ns.gmd}}}dateType"
        self.element_code = f"{{{self.ns.gmd}}}CI_DateTypeCode"
        self.attribute = 'date_type'


class Identifier(MetadataRecordElement):
    def make_element(self):
        identifier_container = SubElement(self.parent_element, f"{{{self.ns.gmd}}}identifier")
        identifier_wrapper = SubElement(identifier_container, f"{{{self.ns.gmd}}}MD_Identifier")
        identifier_element = SubElement(identifier_wrapper, f"{{{self.ns.gmd}}}code")

        if 'href' in self.element_attributes:
            anchor = AnchorElement(
                record=self.record,
                attributes=self.attributes,
                parent_element=identifier_element,
                element_attributes=self.element_attributes,
                element_value=self.element_attributes['identifier']
            )
            anchor.make_element()
        else:
            identifier_value = SubElement(identifier_element, f"{{{self.ns.gco}}}CharacterString")
            identifier_value.text = self.element_attributes['identifier']


class AnchorElement(MetadataRecordElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None,
        element_value: str = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.text = element_value

    def make_element(self):
        attributes = {}

        if 'href' in self.element_attributes:
            attributes[f"{{{self.ns.xlink}}}href"] = self.element_attributes['href']
            attributes[f"{{{self.ns.xlink}}}actuate"] = 'onRequest'
        if 'title' in self.element_attributes:
            attributes[f"{{{self.ns.xlink}}}title"] = self.element_attributes['title']

        anchor = SubElement(self.parent_element, f"{{{self.ns.gmx}}}Anchor", attrib=attributes)
        if self.text is not None:
            anchor.text = self.text


class DataIdentification(MetadataRecordElement):
    def make_element(self):
        data_identification_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}identificationInfo")
        data_identification_element = SubElement(
            data_identification_wrapper,
            f"{{{self.ns.gmd}}}MD_DataIdentification"
        )

        citation_wrapper = SubElement(data_identification_element, f"{{{self.ns.gmd}}}citation")
        citation = Citation(
            record=self.record,
            attributes=self.attributes,
            parent_element=citation_wrapper,
            element_attributes=self.element_attributes['resource']
        )
        citation.make_element()

        abstract = Abstract(
            record=self.record,
            attributes=self.attributes,
            parent_element=data_identification_element,
            element_attributes=self.attributes['resource']
        )
        abstract.make_element()

        if 'contacts' in self.attributes['resource']:
            for point_of_contact_attributes in self.attributes['resource']['contacts']:
                for role in point_of_contact_attributes['role']:
                    if role != 'distributor':
                        _point_of_contact = point_of_contact_attributes.copy()
                        _point_of_contact['role'] = role

                        point_of_contact = PointOfContact(
                            record=self.record,
                            attributes=self.attributes,
                            parent_element=data_identification_element,
                            element_attributes=_point_of_contact
                        )
                        point_of_contact.make_element()

        if 'maintenance' in self.attributes['resource']:
            resource_maintenance = ResourceMaintenance(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=self.element_attributes['resource']['maintenance']
            )
            resource_maintenance.make_element()

        if 'keywords' in self.attributes['resource']:
            for keyword_attributes in self.attributes['resource']['keywords']:
                descriptive_keywords = DescriptiveKeywords(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=data_identification_element,
                    element_attributes=keyword_attributes
                )
                descriptive_keywords.make_element()

        if 'constraints' in self.attributes['resource']:
            constraints = ResourceConstraints(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=self.attributes['resource']['constraints']
            )
            constraints.make_element()

        if 'supplemental_information' in self.attributes['resource']:
            supplemental_information = SupplementalInformation(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=self.attributes['resource']
            )
            supplemental_information.make_element()

        if 'spatial_representation_type' in self.attributes['resource']:
            spatial_representation_type = SpatialRepresentationType(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=self.attributes['resource']
            )
            spatial_representation_type.make_element()

        if 'spatial_resolution' in self.attributes['resource']:
            spatial_resolution = SpatialResolution(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=self.attributes['resource']
            )
            spatial_resolution.make_element()

        language = Language(
            record=self.record,
            attributes=self.attributes,
            parent_element=data_identification_element,
            element_attributes=self.attributes['resource']
        )
        language.make_element()

        if 'topics' in self.attributes['resource']:
            for topic_attribute in self.attributes['resource']['topics']:
                topic = TopicCategory(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=data_identification_element,
                    element_attributes={'topic': topic_attribute}
                )
                topic.make_element()

        if 'extent' in self.attributes['resource']:
            extent = Extent(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=self.attributes['resource']['extent']
            )
            extent.make_element()


class Abstract(MetadataRecordElement):
    def make_element(self):
        abstract_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}abstract")
        abstract_value = SubElement(abstract_element, f"{{{self.ns.gco}}}CharacterString")
        abstract_value.text = self.element_attributes['abstract']


class PointOfContact(MetadataRecordElement):
    def make_element(self):
        point_of_contact_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}pointOfContact")

        responsible_party = ResponsibleParty(
            record=self.record,
            attributes=self.attributes,
            parent_element=point_of_contact_element,
            element_attributes=self.element_attributes
        )
        responsible_party.make_element()


class ResourceMaintenance(MetadataRecordElement):
    def make_element(self):
        resource_maintenance_element = SubElement(
            self.parent_element,
            f"{{{self.ns.gmd}}}resourceMaintenance"
        )
        maintenance_information = MaintenanceInformation(
            record=self.record,
            attributes=self.attributes,
            parent_element=resource_maintenance_element,
            element_attributes=self.element_attributes
        )
        maintenance_information.make_element()


class DescriptiveKeywords(MetadataRecordElement):
    def make_element(self):
        keywords_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}descriptiveKeywords")
        keywords_element = SubElement(keywords_wrapper, f"{{{self.ns.gmd}}}MD_Keywords")

        for term in self.element_attributes['terms']:
            term_element = SubElement(keywords_element, f"{{{self.ns.gmd}}}keyword")
            if 'href' in term:
                anchor = AnchorElement(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=term_element,
                    element_attributes=term,
                    element_value=term['term']
                )
                anchor.make_element()
            else:
                term_value = SubElement(term_element, f"{{{self.ns.gco}}}CharacterString")
                term_value.text = term['term']

        if 'type' in self.element_attributes:
            keyword_type = DescriptiveKeywordsType(
                record=self.record,
                attributes=self.attributes,
                parent_element=keywords_element,
                element_attributes=self.element_attributes
            )
            keyword_type.make_element()

        if 'thesaurus' in self.element_attributes:
            thesaurus = Thesaurus(
                record=self.record,
                attributes=self.attributes,
                parent_element=keywords_element,
                element_attributes=self.element_attributes['thesaurus']
            )
            thesaurus.make_element()


class DescriptiveKeywordsType(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.code_list_values = [
            'discipline',
            'place',
            'stratum',
            'temporal',
            'theme'
        ]
        self.code_list = 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/' \
                         'codelist/gmxCodelists.xml#MD_KeywordTypeCode'
        self.element = f"{{{self.ns.gmd}}}type"
        self.element_code = f"{{{self.ns.gmd}}}MD_KeywordTypeCode"
        self.attribute = 'type'


class Thesaurus(MetadataRecordElement):
    def make_element(self):
        thesaurus_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}thesaurusName")

        citation = Citation(
            record=self.record,
            attributes=self.attributes,
            parent_element=thesaurus_element,
            element_attributes=self.element_attributes
        )
        citation.make_element()


class ResourceConstraints(MetadataRecordElement):
    def make_element(self):
        if 'access' in self.element_attributes:
            for access_constraint_attributes in self.element_attributes['access']:
                constraints_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}resourceConstraints")
                constraints_element = SubElement(constraints_wrapper, f"{{{self.ns.gmd}}}MD_LegalConstraints")

                access_constraint = AccessConstraint(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=constraints_element,
                    element_attributes=access_constraint_attributes
                )
                access_constraint.make_element()

                if 'inspire_limitations_on_public_access' in access_constraint_attributes:
                    constraints_element.set('id', 'InspireLimitationsOnPublicAccess')

                    public_access_limitation = InspireLimitationsOnPublicAccess(
                        record=self.record,
                        attributes=self.attributes,
                        parent_element=constraints_element,
                        element_attributes=access_constraint_attributes
                    )
                    public_access_limitation.make_element()

        if 'usage' in self.element_attributes:
            for usage_constraint_attributes in self.element_attributes['usage']:
                constraints_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}resourceConstraints")
                constraints_element = SubElement(constraints_wrapper, f"{{{self.ns.gmd}}}MD_LegalConstraints")

                use_constraint = UseConstraint(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=constraints_element,
                    element_attributes=usage_constraint_attributes
                )
                use_constraint.make_element()

                if 'copyright_licence' in usage_constraint_attributes:
                    constraints_element.set('id', 'copyright')

                    other_constraint_element = SubElement(
                        constraints_element,
                        f"{{{self.ns.gmd}}}otherConstraints"
                    )

                    if 'href' in usage_constraint_attributes['copyright_licence']:
                        copyright_statement = AnchorElement(
                            record=self.record,
                            attributes=self.attributes,
                            parent_element=other_constraint_element,
                            element_attributes=usage_constraint_attributes['copyright_licence'],
                            element_value=usage_constraint_attributes['copyright_licence']['statement']
                        )
                        copyright_statement.make_element()
                    else:
                        copyright_statement = SubElement(
                            other_constraint_element,
                            f"{{{self.ns.gco}}}CharacterString"
                        )
                        copyright_statement.text = usage_constraint_attributes['copyright_licence']['statement']

                if 'required_citation' in usage_constraint_attributes:
                    constraints_element.set('id', 'citation')

                    other_constraint_element = SubElement(
                        constraints_element,
                        f"{{{self.ns.gmd}}}otherConstraints"
                    )
                    other_constraint_wrapper = SubElement(
                        other_constraint_element,
                        f"{{{self.ns.gco}}}CharacterString"
                    )
                    other_constraint_wrapper.text = f"Cite this information as: " \
                        f"\"{usage_constraint_attributes['required_citation']}\""


class AccessConstraint(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.code_list_values = [
            'copyright',
            'patent',
            'patentPending',
            'trademark',
            'license',
            'intellectualPropertyRights',
            'restricted',
            'otherRestrictions'
        ]
        self.code_list = 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/' \
                         'codelist/gmxCodelists.xml#MD_RestrictionCode'
        self.element = f"{{{self.ns.gmd}}}accessConstraints"
        self.element_code = f"{{{self.ns.gmd}}}MD_RestrictionCode"
        self.attribute = 'restriction_code'


class UseConstraint(AccessConstraint):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.element = f"{{{self.ns.gmd}}}useConstraints"


class InspireLimitationsOnPublicAccess(MetadataRecordElement):
    def make_element(self):
        other_constraints_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}otherConstraints")

        other_constraints_value = AnchorElement(
            record=self.record,
            attributes=self.attributes,
            parent_element=other_constraints_element,
            element_attributes={
                'href': f"http://inspire.ec.europa.eu/metadata-codelist/LimitationsOnPublicAccess/"
                f"{self.element_attributes['inspire_limitations_on_public_access']}"
            },
            element_value=self.element_attributes['inspire_limitations_on_public_access']
        )
        other_constraints_value.make_element()


class SupplementalInformation(MetadataRecordElement):
    def make_element(self):
        if 'supplemental_information' in self.element_attributes:
            supplemental_info_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}supplementalInformation")
            supplemental_info_value = SubElement(supplemental_info_element, f"{{{self.ns.gco}}}CharacterString")
            supplemental_info_value.text = self.element_attributes['supplemental_information']


class SpatialRepresentationType(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.code_list_values = [
            'vector',
            'grid',
            'textTable',
            'tin',
            'stereoModel',
            'video'
        ]
        self.code_list = 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/' \
                         'codelist/gmxCodelists.xml#MD_SpatialRepresentationTypeCode'
        self.element = f"{{{self.ns.gmd}}}spatialRepresentationType"
        self.element_code = f"{{{self.ns.gmd}}}MD_SpatialRepresentationTypeCode"
        self.attribute = 'spatial_representation_type'


class SpatialResolution(MetadataRecordElement):
    def make_element(self):
        resolution_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}spatialResolution")
        resolution_element = SubElement(resolution_wrapper, f"{{{self.ns.gmd}}}MD_Resolution")

        if self.element_attributes['spatial_resolution'] is None:
            SubElement(
                resolution_element,
                f"{{{self.ns.gmd}}}distance",
                attrib={f"{{{self.ns.gco}}}nilReason": 'inapplicable'}
            )


class TopicCategory(MetadataRecordElement):
    def make_element(self):
        topic_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}topicCategory")
        topic_value = SubElement(topic_element, f"{{{self.ns.gmd}}}MD_TopicCategoryCode")
        topic_value.text = self.element_attributes['topic']


class Extent(MetadataRecordElement):
    def make_element(self):
        extent_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}extent")
        extent_element = SubElement(extent_wrapper, f"{{{self.ns.gmd}}}EX_Extent")

        if 'geographic' in self.element_attributes:
            geographic_extent = GeographicExtent(
                record=self.record,
                attributes=self.attributes,
                parent_element=extent_element,
                element_attributes=self.element_attributes['geographic']
            )
            geographic_extent.make_element()

        if 'vertical' in self.element_attributes:
            vertical_extent = VerticalExtent(
                record=self.record,
                attributes=self.attributes,
                parent_element=extent_element,
                element_attributes=self.element_attributes['vertical']
            )
            vertical_extent.make_element()

        if 'temporal' in self.element_attributes:
            temporal_extent = TemporalExtent(
                record=self.record,
                attributes=self.attributes,
                parent_element=extent_element,
                element_attributes=self.element_attributes['temporal']
            )
            temporal_extent.make_element()


class GeographicExtent(MetadataRecordElement):
    def make_element(self):
        geographic_extent_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}geographicElement")

        if 'bounding_box' in self.element_attributes:
            bounding_box = BoundingBox(
                record=self.record,
                attributes=self.attributes,
                parent_element=geographic_extent_element,
                element_attributes=self.element_attributes['bounding_box']
            )
            bounding_box.make_element()


class BoundingBox(MetadataRecordElement):
    def make_element(self):
        bounding_box_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}EX_GeographicBoundingBox")

        west_element = SubElement(bounding_box_element, f"{{{self.ns.gmd}}}westBoundLongitude")
        west_value = SubElement(west_element, f"{{{self.ns.gco}}}Decimal")
        west_value.text = str(self.element_attributes['west_longitude'])

        east_element = SubElement(bounding_box_element, f"{{{self.ns.gmd}}}eastBoundLongitude")
        east_value = SubElement(east_element, f"{{{self.ns.gco}}}Decimal")
        east_value.text = str(self.element_attributes['east_longitude'])

        south_element = SubElement(bounding_box_element, f"{{{self.ns.gmd}}}southBoundLatitude")
        south_value = SubElement(south_element, f"{{{self.ns.gco}}}Decimal")
        south_value.text = str(self.element_attributes['south_latitude'])

        north_element = SubElement(bounding_box_element, f"{{{self.ns.gmd}}}northBoundLatitude")
        north_value = SubElement(north_element, f"{{{self.ns.gco}}}Decimal")
        north_value.text = str(self.element_attributes['north_latitude'])


class VerticalExtent(MetadataRecordElement):
    def make_element(self):
        vertical_extent_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}verticalElement")
        vertical_extent_element = SubElement(vertical_extent_wrapper, f"{{{self.ns.gmd}}}EX_VerticalExtent")

        if 'minimum' in self.element_attributes:
            minimum_element = SubElement(vertical_extent_element, f"{{{self.ns.gmd}}}minimumValue")
            minimum_value = SubElement(minimum_element, f"{{{self.ns.gco}}}Real")
            minimum_value.text = str(self.element_attributes['minimum'])
        else:
            SubElement(
                vertical_extent_element,
                f"{{{self.ns.gmd}}}minimumValue",
                attrib={f"{{{self.ns.gco}}}nilReason": 'unknown'}
            )

        if 'maximum' in self.element_attributes:
            maximum_element = SubElement(vertical_extent_element, f"{{{self.ns.gmd}}}maximumValue")
            maximum_value = SubElement(maximum_element, f"{{{self.ns.gco}}}Real")
            maximum_value.text = str(self.element_attributes['maximum'])
        else:
            SubElement(
                vertical_extent_element,
                f"{{{self.ns.gmd}}}maximumValue",
                attrib={f"{{{self.ns.gco}}}nilReason": 'unknown'}
            )

        if 'code' in self.element_attributes:
            vertical_crs = VerticalCRS(
                record=self.record,
                attributes=self.attributes,
                parent_element=vertical_extent_element,
                element_attributes=self.element_attributes
            )
            vertical_crs.make_element()


class VerticalCRS(MetadataRecordElement):
    def make_element(self):
        vertical_crs_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}verticalCRS")
        vertical_crs_element = SubElement(
            vertical_crs_wrapper,
            f"{{{self.ns.gml}}}VerticalCRS",
            attrib={f"{{{self.ns.gml}}}id": self.element_attributes['identifier']}
        )
        vertical_crs_code = SubElement(
            vertical_crs_element,
            f"{{{self.ns.gml}}}identifier",
            attrib={'codeSpace': 'OGP'}
        )
        vertical_crs_code.text = self.element_attributes['code']

        name = SubElement(vertical_crs_element, f"{{{self.ns.gml}}}name")
        name.text = self.element_attributes['name']

        remarks = SubElement(vertical_crs_element, f"{{{self.ns.gml}}}remarks")
        remarks.text = self.element_attributes['remarks']

        SubElement(
            vertical_crs_element,
            f"{{{self.ns.gml}}}domainOfValidity",
            attrib={
                f"{{{self.ns.xlink}}}href": self.element_attributes['domain_of_validity']['href']
            }
        )

        scope = SubElement(vertical_crs_element, f"{{{self.ns.gml}}}scope")
        scope.text = self.element_attributes['scope']

        SubElement(
            vertical_crs_element,
            f"{{{self.ns.gml}}}verticalCS",
            attrib={
                f"{{{self.ns.xlink}}}href": self.element_attributes['vertical_cs']['href']
            }
        )

        SubElement(
            vertical_crs_element,
            f"{{{self.ns.gml}}}verticalDatum",
            attrib={
                f"{{{self.ns.xlink}}}href": self.element_attributes['vertical_datum']['href']
            }
        )


class TemporalExtent(MetadataRecordElement):
    def make_element(self):
        temporal_extent_container = SubElement(self.parent_element, f"{{{self.ns.gmd}}}temporalElement")
        temporal_extent_wrapper = SubElement(temporal_extent_container, f"{{{self.ns.gmd}}}EX_TemporalExtent")
        temporal_extent_element = SubElement(temporal_extent_wrapper, f"{{{self.ns.gmd}}}extent")

        if 'period' in self.element_attributes:
            time_period_element = SubElement(
                temporal_extent_element,
                f"{{{self.ns.gml}}}TimePeriod",
                attrib={f"{{{self.ns.gml}}}id": 'boundingExtent'}
            )
            begin_position_element = SubElement(time_period_element, f"{{{self.ns.gml}}}beginPosition")
            begin_position_element.text = Utils.format_date_string(self.element_attributes['period']['start'])

            end_position_element = SubElement(time_period_element, f"{{{self.ns.gml}}}endPosition")
            end_position_element.text = Utils.format_date_string(self.element_attributes['period']['end'])


class DataDistribution(MetadataRecordElement):
    def make_element(self):
        data_distribution_wrapper = SubElement(self.record, f"{{{self.ns.gmd}}}distributionInfo")
        data_distribution_element = SubElement(data_distribution_wrapper, f"{{{self.ns.gmd}}}MD_Distribution")

        if 'formats' in self.attributes['resource']:
            for format_attributes in self.attributes['resource']['formats']:
                distribution_format = DistributionFormat(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=data_distribution_element,
                    element_attributes=format_attributes
                )
                distribution_format.make_element()

        if 'contacts' in self.attributes['resource']:
            for point_of_contact_attributes in self.attributes['resource']['contacts']:
                for role in point_of_contact_attributes['role']:
                    if role == 'distributor':
                        _point_of_contact = point_of_contact_attributes.copy()
                        _point_of_contact['role'] = role

                        distributor = Distributor(
                            record=self.record,
                            attributes=self.attributes,
                            parent_element=data_distribution_element,
                            element_attributes=_point_of_contact
                        )
                        distributor.make_element()

        if 'transfer_options' in self.attributes['resource']:
            for transfer_attributes in self.attributes['resource']['transfer_options']:
                transfer_options = TransferOptions(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=data_distribution_element,
                    element_attributes=transfer_attributes
                )
                transfer_options.make_element()


class DistributionFormat(MetadataRecordElement):
    def make_element(self):
        distribution_format_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}distributionFormat")
        distribution_format_element = SubElement(distribution_format_wrapper, f"{{{self.ns.gmd}}}MD_Format")

        format_name_element = SubElement(distribution_format_element, f"{{{self.ns.gmd}}}name")
        if 'href' in self.element_attributes:
            anchor = AnchorElement(
                record=self.record,
                attributes=self.attributes,
                parent_element=format_name_element,
                element_attributes=self.element_attributes,
                element_value=self.element_attributes['format']
            )
            anchor.make_element()
        else:
            format_name_value = SubElement(format_name_element, f"{{{self.ns.gco}}}CharacterString")
            format_name_value.text = self.element_attributes['format']

        if 'version' in self.element_attributes:
            format_version_element = SubElement(distribution_format_element, f"{{{self.ns.gmd}}}version")
            format_version_value = SubElement(format_version_element, f"{{{self.ns.gco}}}CharacterString")
            format_version_value.text = self.element_attributes['version']
        else:
            SubElement(
                distribution_format_element,
                f"{{{self.ns.gmd}}}version",
                attrib={f"{{{self.ns.gco}}}nilReason": 'unknown'}
            )


class Distributor(MetadataRecordElement):
    def make_element(self):
        distributor_container = SubElement(self.parent_element, f"{{{self.ns.gmd}}}distributor")
        distributor_wrapper = SubElement(distributor_container, f"{{{self.ns.gmd}}}MD_Distributor")
        distributor_element = SubElement(distributor_wrapper, f"{{{self.ns.gmd}}}distributorContact")

        responsible_party = ResponsibleParty(
            record=self.record,
            attributes=self.attributes,
            parent_element=distributor_element,
            element_attributes=self.element_attributes
        )
        responsible_party.make_element()


class TransferOptions(MetadataRecordElement):
    def make_element(self):
        transfer_options_container = SubElement(self.parent_element, f"{{{self.ns.gmd}}}transferOptions")
        transfer_options_wrapper = SubElement(
            transfer_options_container,
            f"{{{self.ns.gmd}}}MD_DigitalTransferOptions"
        )

        if 'size' in self.element_attributes:
            if 'unit' in self.element_attributes['size']:
                transfer_size_unit_element = SubElement(
                    transfer_options_wrapper,
                    f"{{{self.ns.gmd}}}unitsOfDistribution"
                )
                transfer_size_unit_value = SubElement(
                    transfer_size_unit_element,
                    f"{{{self.ns.gco}}}CharacterString"
                )
                transfer_size_unit_value.text = self.element_attributes['size']['unit']
            if 'magnitude' in self.element_attributes['size']:
                transfer_size_magnitude_element = SubElement(
                    transfer_options_wrapper,
                    f"{{{self.ns.gmd}}}transferSize"
                )
                transfer_size_magnitude_value = SubElement(
                    transfer_size_magnitude_element,
                    f"{{{self.ns.gco}}}Real"
                )
                transfer_size_magnitude_value.text = str(self.element_attributes['size']['magnitude'])

        transfer_options_element = SubElement(transfer_options_wrapper, f"{{{self.ns.gmd}}}onLine")
        online_resource = OnlineResource(
            record=self.record,
            attributes=self.attributes,
            parent_element=transfer_options_element,
            element_attributes=self.element_attributes['online_resource']
        )
        online_resource.make_element()


class DataQuality(MetadataRecordElement):
    def make_element(self):
        data_quality_wrapper = SubElement(self.record, f"{{{self.ns.gmd}}}dataQualityInfo")
        data_quality_element = SubElement(data_quality_wrapper, f"{{{self.ns.gmd}}}DQ_DataQuality")

        scope = Scope(
            record=self.record,
            attributes=self.attributes,
            parent_element=data_quality_element
        )
        scope.make_element()

        if 'measures' in self.attributes['resource']:
            for measure_attributes in self.attributes['resource']['measures']:
                report = Report(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=data_quality_element,
                    element_attributes=measure_attributes
                )
                report.make_element()

        lineage = Lineage(
            record=self.record,
            attributes=self.attributes,
            parent_element=data_quality_element,
            element_attributes=self.attributes['resource']
        )
        lineage.make_element()


class Scope(MetadataRecordElement):
    def make_element(self):
        scope_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}scope")
        scope_element = SubElement(scope_wrapper, f"{{{self.ns.gmd}}}DQ_Scope")

        scope_code = ScopeCode(
            record=self.record,
            attributes=self.attributes,
            parent_element=scope_element
        )
        scope_code.make_element()


class Report(MetadataRecordElement):
    def make_element(self):
        report_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}report")
        report_element = SubElement(report_wrapper, f"{{{self.ns.gmd}}}DQ_DomainConsistency")

        identification_wrapper = SubElement(report_element, f"{{{self.ns.gmd}}}measureIdentification")
        identification_element = SubElement(identification_wrapper, f"{{{self.ns.gmd}}}RS_Identifier")

        identification_code_element = SubElement(identification_element, f"{{{self.ns.gmd}}}code")
        identification_code_value = SubElement(identification_code_element, f"{{{self.ns.gco}}}CharacterString")
        identification_code_value.text = self.element_attributes['code']

        identification_code_space_element = SubElement(identification_element, f"{{{self.ns.gmd}}}codeSpace")
        identification_code_space_value = SubElement(
            identification_code_space_element,
            f"{{{self.ns.gco}}}CharacterString"
        )
        identification_code_space_value.text = self.element_attributes['code_space']

        result_wrapper = SubElement(report_element, f"{{{self.ns.gmd}}}result")
        result_element = SubElement(result_wrapper, f"{{{self.ns.gmd}}}DQ_ConformanceResult")

        specification_element = SubElement(result_element, f"{{{self.ns.gmd}}}specification")
        citation = Citation(
            record=self.record,
            attributes=self.attributes,
            parent_element=specification_element,
            element_attributes=self.element_attributes
        )
        citation.make_element()

        explanation_element = SubElement(result_element, f"{{{self.ns.gmd}}}explanation")
        explanation_value = SubElement(explanation_element, f"{{{self.ns.gco}}}CharacterString")
        explanation_value.text = self.element_attributes['explanation']

        pass_element = SubElement(result_element, f"{{{self.ns.gmd}}}pass")
        pass_value = SubElement(pass_element, f"{{{self.ns.gco}}}Boolean")
        pass_value.text = str(self.element_attributes['pass']).lower()


class Lineage(MetadataRecordElement):
    def make_element(self):
        if 'lineage' in self.element_attributes:
            lineage_container = SubElement(self.parent_element, f"{{{self.ns.gmd}}}lineage")
            lineage_wrapper = SubElement(lineage_container, f"{{{self.ns.gmd}}}LI_Lineage")
            lineage_element = SubElement(lineage_wrapper, f"{{{self.ns.gmd}}}statement")
            lineage_value = SubElement(lineage_element, f"{{{self.ns.gco}}}CharacterString")
            lineage_value.text = self.element_attributes['lineage']
