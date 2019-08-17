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
            "$id": "https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/"
                   "iso-19115-v1/profiles/uk-pdc-discovery-v1/configuration-schema.json",
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "UK PDC Metadata Record Generator - ISO 19115 v1 UK PDC Discovery v1 configuration schema",
            "description": "Metadata record configuration schema for the UK PDC Discovery metadata profile (v1) of the "
                           "ISO 19115 (v1) metadata standard",
            "definitions": {
                "contact": {
                    "anyOf": [
                        {
                            "required": [
                                "individual"
                            ]
                        },
                        {
                            "required": [
                                "organisation"
                            ]
                        }
                    ],
                    "properties": {
                        "individual": {
                            "$ref": "#/definitions/contact_identity"
                        },
                        "organisation": {
                            "$ref": "#/definitions/contact_identity"
                        },
                        "online_resource": {
                            "$ref": "#/definitions/online_resource"
                        }
                    }
                },
                "contact_identity": {
                    "required": [
                        "href",
                        "title"
                    ],
                    "properties": {
                        "title": {
                            "enum": [
                                "isni",
                                "orcid"
                            ]
                        }
                    }
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
                },
                "online_resource": {
                    "required": [
                        "function"
                    ]
                }
            },
            "allOf": [
                {
                    "$ref": "https://metadata-standards.data.bas.ac.uk/"
                            "bas-metadata-generator-configuration-schemas/iso-19115-v1/profiles/inspire-v1_3/"
                            "configuration-schema.json"
                },
                {
                    "required": [
                        "file_identifier",
                        "character_set",
                        "maintenance",
                        "metadata_standard"
                    ],
                    "properties": {
                        "file_identifier": {
                            "pattern": "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
                        },
                        "character_set": {
                            "enum": [
                                "utf8"
                            ]
                        },
                        "hierarchy_level": {
                            "enum": [
                                "dataset"
                            ]
                        },
                        "contacts": {
                            "items": {
                                "$ref": "#/definitions/contact"
                            }
                        },
                        "metadata_standard": {
                            "required": [
                                "name",
                                "version"
                            ],
                            "properties": {
                                "name": {
                                    "enum": [
                                        "ISO 19115 (UK GEMINI)"
                                    ]
                                },
                                "version": {
                                    "enum": [
                                        "1.0 (2.3)"
                                    ]
                                }
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
                                "maintenance",
                                "edition",
                                "supplemental_information",
                                "lineage"
                            ],
                            "properties": {
                                "dates": {
                                    "allOf": [
                                        {
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
                                        {
                                            "contains": {
                                                "properties": {
                                                    "date_type": {
                                                        "enum": [
                                                            "released"
                                                        ]
                                                    }
                                                }
                                            }
                                        }
                                    ]
                                },
                                "identifiers": {
                                    "items": {
                                        "required": [
                                            "title"
                                        ],
                                        "properties": {
                                            "title": {
                                                "enum": [
                                                    "self",
                                                    "doi",
                                                    "award",
                                                    "publication"
                                                ]
                                            }
                                        }
                                    },
                                    "contains": {
                                        "properties": {
                                            "title": {
                                                "enum": [
                                                    "self"
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
                                        "allOf": [
                                            {
                                                "properties": {
                                                    "organisation": {
                                                        "properties": {
                                                            "name": {
                                                                "enum": [
                                                                    "UK Polar Data Centre"
                                                                ]
                                                            }
                                                        }
                                                    },
                                                    "role": {
                                                        "contains": {
                                                            "enum": [
                                                                "pointOfContact"
                                                            ]
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "properties": {
                                                    "organisation": {
                                                        "properties": {
                                                            "name": {
                                                                "enum": [
                                                                    "UK Polar Data Centre"
                                                                ]
                                                            }
                                                        }
                                                    },
                                                    "role": {
                                                        "contains": {
                                                            "enum": [
                                                                "custodian"
                                                            ]
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "properties": {
                                                    "organisation": {
                                                        "properties": {
                                                            "name": {
                                                                "enum": [
                                                                    "UK Polar Data Centre"
                                                                ]
                                                            }
                                                        }
                                                    },
                                                    "role": {
                                                        "contains": {
                                                            "enum": [
                                                                "publisher"
                                                            ]
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "properties": {
                                                    "organisation": {
                                                        "properties": {
                                                            "name": {
                                                                "enum": [
                                                                    "UK Polar Data Centre"
                                                                ]
                                                            }
                                                        }
                                                    },
                                                    "role": {
                                                        "contains": {
                                                            "enum": [
                                                                "publisher"
                                                            ]
                                                        }
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                },
                                "keywords": {
                                    "items": {
                                        "$ref": "#/definitions/keywords"
                                    }
                                },
                                "supplemental_information": {
                                    "enum": [
                                        "It is recommended that careful attention be paid to the contents of any "
                                        "data, and that the author be contacted with any questions regarding "
                                        "appropriate use. If you find any errors or omissions, please report them "
                                        "to polardatacentre@bas.ac.uk."
                                    ]
                                },
                                "transfer_options": {
                                    "items": {
                                        "properties": {
                                            "online_resource": {
                                                "$ref": "#/definitions/online_resource"
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
