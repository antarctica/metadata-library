from bas_metadata_library import MetadataRecordConfig as _MetadataRecordConfig


# Base classes

class MetadataRecordConfig(_MetadataRecordConfig):
    """
    Overloaded base MetadataRecordConfig class

    Defines the JSON Schema used for this metadata standard
    """
    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)

        self.config = kwargs
        self.schema = {
            "$id": "",
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "UK PDC Metadata Record Generator - ISO 19115 v1 Inspire configuration schema",
            "description": "Metadata record configuration schema for the Inspire profile of the ISO 19115 (v1) "
                           "metadata standard",
            "definitions": {
                "contact": {
                    "required": [
                        "organisation",
                        "email"
                    ]
                },
                "keywords": {
                    "properties": {
                        "thesaurus": {
                            "$ref": "#/definitions/thesaurus"
                        }
                    }
                },
                "thesaurus": {
                    "required": [
                        "title",
                        "dates"
                    ],
                    "properties": {
                        "contact": {
                            "$ref": "#/definitions/contact"
                        }
                    }
                }
            },
            "allOf": [
                {
                    "$ref": "https://metadata-standards.data.bas.ac.uk/generic-configuration-schemas/iso-19115-v1/"
                            "configuration_schema.json"
                },
                {
                    "required": [
                        "language",
                        "hierarchy_level"
                    ],
                    "properties": {
                        "hierarchy_level": {
                            "enum": [
                                "dataset",
                                "series",
                                "service"
                            ]
                        },
                        "contacts": {
                            "items": {
                                "$ref": "#/definitions/contact"
                            }
                        },
                        "reference_system_info": {
                            "properties": {
                                "authority": {
                                    "properties": {
                                        "contact": {
                                            "$ref": "#/definitions/contact"
                                        }
                                    }
                                }
                            }
                        },
                        "resource": {
                            "required": [
                                "extent",
                                "constraints"
                            ],
                            "properties": {
                                "dates": {
                                    "contains": {
                                        "properties": {
                                            "date_type": {
                                                "enum": [
                                                    "creation"
                                                ]
                                            }
                                        }
                                    }
                                },
                                "contacts": {
                                    "items": {
                                        "$ref": "#/definitions/contact"
                                    },
                                    "contains": {
                                        "properties": {
                                            "role": {
                                                "contains": {
                                                    "enum": [
                                                        "pointOfContact"
                                                    ]
                                                }
                                            }
                                        }
                                    }
                                },
                                "keywords": {
                                    "items": {
                                        "$ref": "#/definitions/keywords"
                                    },
                                    "contains": {
                                        "properties": {
                                            "thesaurus": {
                                                "properties": {
                                                    "title": {
                                                        "properties": {
                                                            "value": {
                                                                "enum": [
                                                                    "General Multilingual Environmental Thesaurus - INSPIRE themes"
                                                                ]
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                },
                                "identifiers": {
                                    "minItems": 1
                                },
                                "extent": {
                                    "anyOf": [
                                        {
                                            "required": [
                                                "geographic"
                                            ]
                                        },
                                        {
                                            "required": [
                                                "vertical"
                                            ]
                                        },
                                        {
                                            "required": [
                                                "temporal"
                                            ]
                                        }
                                    ]
                                },
                                "measures": {
                                    "contains": {
                                        "properties": {
                                            "code": {
                                                "enum": [
                                                    "Conformity_001"
                                                ]
                                            },
                                            "code_space": {
                                                "enum": [
                                                    "INSPIRE"
                                                ]
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            ]
        }
