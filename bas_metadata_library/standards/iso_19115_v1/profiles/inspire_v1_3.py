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
            "$id": "https://metadata-standards-testing.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/"
                   "iso-19115-v1/profiles/inspire-v1_3/configuration-schema.json",
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "UK PDC Metadata Record Generator - ISO 19115 v1 Inspire v1.3 configuration schema",
            "description": "Metadata record configuration schema for the Inspire profile (v1.3) of the ISO 19115 (v1) "
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
                    "$ref": "https://metadata-standards-testing.data.bas.ac.uk/"
                            "bas-metadata-generator-configuration-schemas/iso-19115-v1/configuration-schema.json"
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
                                "constraints",
                                "topics",
                                "lineage"
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
                                "identifiers": {
                                    "minItems": 1
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
                                "topics": {
                                    "minItems": 1
                                },
                                "constraints": {
                                    "required": [
                                        "access",
                                        "usage"
                                    ],
                                    "properties": {
                                        "access": {
                                            "contains": {
                                                "required": [
                                                    "inspire_limitations_on_public_access"
                                                ]
                                            }
                                        },
                                        "usage": {
                                            "contains": {
                                                "anyOf": [
                                                    {
                                                        "required": [
                                                            "copyright_licence"
                                                        ]
                                                    },
                                                    {
                                                        "required": [
                                                            "statement"
                                                        ]
                                                    }
                                                ]
                                            }
                                        }
                                    }
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
