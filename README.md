# BAS Metadata Library

Python library for generating metadata records.

## Overview

### Purpose

This library is designed to assist in generating metadata records for the discovery of datasets, services, features 
and related resources. This project is intended to be used as a dependency within other tools and services, to avoid 
the need to duplicate the implementation of complex and verbose metadata standards.

At a high level, this library allows a configuration object, representing the fields/structure of a standard, to be 
encoded into the formal representation set out by that standard (typically in XML). It also allows a formal 
representation to be decoded back into a configuration object, which can be more easily used or manipulated in software.

### Supported standards

| Standard                                                        | Implementation                                                  | Library Namespace                                   | Introduced In                                                                                      |
| --------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| [ISO 19115:2003](https://www.iso.org/standard/26020.html)       | [ISO 19139:2007](https://www.iso.org/standard/32557.html)       | `bas_metadata_library.standards.iso_19115_1_v1`     | [#46](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/issues/46)   |
| [ISO 19115-2:2009](https://www.iso.org/standard/39229.html)     | [ISO 19139-2:2012](https://www.iso.org/standard/57104.html)     | `bas_metadata_library.standards.iso_19115_2_v1`     | [#50](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/issues/50)   |
| [IEC 61174:2015](https://webstore.iec.ch/publication/23128)     | [IEC 61174:2015](https://webstore.iec.ch/publication/23128)     | `bas_metadata_library.standards.iec_pas_61174_0_v1` | [#139](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/issues/139) |
| [IEC PAS 61174:2021](https://webstore.iec.ch/publication/67774) | [IEC PAS 61174:2021](https://webstore.iec.ch/publication/67774) | `bas_metadata_library.standards.iec_pas_61174_1_v1` | [#139](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/issues/144) |

**Note:** In this library, the *ISO 19115:2003* standard is referred to as *ISO-19115-1* (`iso_19115_1_v1`) for
consistency with *ISO 19115-2:2009* (referred to as *ISO-19115-2*, `iso_19115_2_v1`). In the future, the
[ISO 19115-1:2014](https://www.iso.org/standard/53798.html) standard will be referred to as *ISO-19115-3*.

### Supported profiles

| Standard | Profile  | Implementation  | Library Namespace | Introduced In |
| -------- | -------- | --------------- | ----------------- | ------------- |
| -        | -        | -               | -                 | -             |

**Note:** Support for profiles has been removed to allow underlying standards to be implemented more easily, and to
wait until stable profiles for UK PDC Discovery metadata have been developed and approved.

### Supported configuration versions

| Standard           | Profile | Configuration Version                                                                                                     | Status     | Notes                               |
| ------------------ | ------- | ------------------------------------------------------------------------------------------------------------------------- | ---------- | ----------------------------------- |
| ISO 19115:2003     | -       | [`v1`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-1-v1.json)     | Deprecated | Deprecated version replaced by `v2` |
| ISO 19115:2003     | -       | [`v2`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-1-v2.json)     | Live       | Stable version                      |
| ISO 19115-2:2009   | -       | [`v1`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v1.json)     | Deprecated | Deprecated version replaced by `v2` |
| ISO 19115-2:2009   | -       | [`v2`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v2.json)     | Live       | Stable version                      |
| IEC 61174:2015     | -       | [`v1`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iec-pas-61174-0-v1.json) | Alpha      | Experimental                        |
| IEC PAS 61174:2021 | -       | [`v1`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iec-pas-61174-1-v1.json) | Alpha      | Experimental                        |

### Supported standards coverage

This library is built around the needs of the British Antarctic Survey and the NERC (UK) Polar Data Centre. This means 
only standards, and elements of these standards, used by BAS or the UK PDC are supported. However, additions that would
enable this library to be useful to other organisations and use-case are welcome as contributions providing they do not
add significant complexity or maintenance.

| Standard           | Coverage | Coverage Summary                                                                                 |
| ------------------ | -------- | ------------------------------------------------------------------------------------------------ |
| ISO 19115:2003     | Good     | All mandatory elements are supported with a good number of commonly used additional elements     |
| ISO 19115-2:2009   | Minimal  | With the exception of the root element, no additional elements from this extension are supported |
| IEC 61174:2015     | Minimal  | All mandatory elements supported plus a limited number of optional route information attributes  |
| IEC PAS 61174:2021 | Minimal  | All mandatory elements supported plus a limited number of optional route information attributes  |

#### Coverage for IEC 61174

As required by the IEC 61174 standard, this library supports the following properties within this standard:

| Element                                        | Reference | Obligation |
| ---------------------------------------------- | --------- | ---------- |
| `route`                                        | *4.5.2*   | Mandatory  | 
| `route.routeInfo.routeAuthor`                  | *4.5.3*   | Optional   | 
| `route.routeInfo.routeName`                    | *4.5.3*   | Mandatory  | 
| `route.routeInfo.routeStatus`                  | *4.5.3*   | Optional   | 
| `route.waypoints`                              | *4.5.4*   | Mandatory  | 
| `route.waypoints.*.waypoint.id`                | *4.5.6*   | Mandatory  | 
| `route.waypoints.*.waypoint.revision`          | *4.5.6*   | Mandatory  | 
| `route.waypoints.*.waypoint.position.lat`      | *4.5.6*   | Mandatory  | 
| `route.waypoints.*.waypoint.position.lon`      | *4.5.6*   | Mandatory  | 
| `route.waypoints.*.waypoint.position.geometry` | *4.5.6*   | Optional   | 

This list is exhaustive. No extensions are supported.

References in the above table relate to the IEC PAS 61174:2021 standards document: 
https://webstore.iec.ch/publication/67774. 

Full citation:

> IEC 61174:2015, Maritime navigation and radiocommunication equipment and systems – Electronic chart display and 
> information system (ECDIS) – Operational and performance requirements, methods of testing and required test results

## Installation

This package can be installed using Pip from [PyPi](https://pypi.org/project/bas-metadata-library):

```
$ pip install bas-metadata-library
```

## Usage

### Encode an ISO 19115 metadata record

To generate an ISO 19115 metadata record from a Python record configuration and return it as an XML document:

```python
from datetime import date

from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV2, MetadataRecord

minimal_record_config = {
    "hierarchy_level": "dataset",
    "metadata": {
        "language": "eng",
        "character_set": "utf-8",
        "contacts": [{"organisation": {"name": "UK Polar Data Centre"}, "role": ["pointOfContact"]}],
        "date_stamp": date(2018, 10, 18),
    },
    "identification": {
        "title": {"value": "Test Record"},
        "dates": {"creation": {"date": date(2018, 1, 1), "date_precision": "year"}},
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
configuration = MetadataRecordConfigV2(**minimal_record_config)
record = MetadataRecord(configuration=configuration)
document = record.generate_xml_document()

# output document
print(document.decode())
```

### Encode an IEC 61174 route information record

To encode to a RTZ file:

```python
from bas_metadata_library.standards.iec_pas_61174_0_v1 import MetadataRecordConfigV1, MetadataRecord

minimal_record_config = {"route_name": "minimal-test-route",
    "waypoints": [
        {"id": 1001, "revision": 0, "position": {"lat": 5, "lon": 50}},
        {"id": 1002, "revision": 0, "position": {"lat": 5, "lon": 50}},
        {"id": 1003, "revision": 0, "position": {"lat": 5, "lon": 50}},
    ],
}
configuration = MetadataRecordConfigV1(**minimal_record_config)
record = MetadataRecord(configuration=configuration)
document = record.generate_xml_document()

# output document
print(document.decode())
```

To encode to a RTZP package:

```python
from pathlib import Path

from bas_metadata_library.standards.iec_pas_61174_0_v1 import MetadataRecordConfigV1, MetadataRecord

minimal_record_config = {"route_name": "minimal-test-route",
    "waypoints": [
        {"id": 1001, "revision": 0, "position": {"lat": 5, "lon": 50}},
        {"id": 1002, "revision": 0, "position": {"lat": 5, "lon": 50}},
        {"id": 1003, "revision": 0, "position": {"lat": 5, "lon": 50}},
    ],
}
configuration = MetadataRecordConfigV1(**minimal_record_config)
record = MetadataRecord(configuration=configuration)
record.generate_rtzp_archive(file=Path('/path/to/file.rtzp'))
```

### Decode an ISO 19115 metadata record

```python
from bas_metadata_library.standards.iso_19115_2 import MetadataRecord

with open(f"minimal-record.xml") as record_file:
    record_data = record_file.read()

record = MetadataRecord(record=record_data)
configuration = record.make_config()
minimal_record_config = configuration.config

# output configuration
print(minimal_record_config)
```

### Decode an IEC 61174 route information record

To decode from a RTZ file:

```python
from bas_metadata_library.standards.iec_pas_61174_0_v1 import MetadataRecord

with open(f"minimal-record.rtz") as record_file:
    record_data = record_file.read()

record = MetadataRecord(record=record_data)
configuration = record.make_config()
minimal_record_config = configuration.config

# output configuration
print(minimal_record_config)
```

To decode from a RTZP package:

```python
from pathlib import Path

from bas_metadata_library.standards.iec_pas_61174_0_v1 import MetadataRecord

record = MetadataRecord()
record.load_from_rtzp_archive(file=Path('/path/to/file.rtzp'))
configuration = record.make_config()
minimal_record_config = configuration.config

# output configuration
print(minimal_record_config)
```

### Loading a record configuration from JSON

**The example below is for the ISO 19115 standard but this applies to all standards.**

The `load()` and `loads()` methods on the configuration class can be used to load a record configuration encoded as a
JSON file or JSON string respectively:

```python
from pathlib import Path

from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV2

configuration = MetadataRecordConfigV2()
configuration.load(file=Path("/path/to/file.json"))
```

### Dumping a record configuration to JSON

**The example below is for the ISO 19115 standard but this applies to all standards.**

The `dump()` and `dumps()` methods on the configuration class can be used to dump a record configuration to a JSON 
encoded file or string respectively:

```python
from datetime import date
from pathlib import Path

from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV2

minimal_record_config = {
    "hierarchy_level": "dataset",
    "metadata": {
        "language": "eng",
        "character_set": "utf-8",
        "contacts": [{"organisation": {"name": "UK Polar Data Centre"}, "role": ["pointOfContact"]}],
        "date_stamp": date(2018, 10, 18),
    },
    "identification": {
        "title": {"value": "Test Record"},
        "dates": {"creation": {"date": date(2018, 1, 1), "date_precision": "year"}},
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
configuration = MetadataRecordConfigV2(**minimal_record_config)
configuration.dump(file=Path('/path/to/file.json'))
```

### HTML entities

Do not include HTML entities in input to this generator, as they will be double escaped by [Lxml](https://lxml.de), the
underlying XML processing library used by this project. Instead, literal characters should be used (e.g. `>`), which
will be escaped as needed automatically. This applies to any unicode character, such as accents (e.g. `å`) and
symbols (e.g. `µ`).

E.g. If `&gt;`, the HTML entity for `>` (greater than), were used as input, it would be escaped again to `&amp;gt;`
which will not be valid output.

### ISO 19115 - linkages between transfer options and formats

To support generating a table of download options for a resource (such as [1]), this library uses a 'distribution
option' concept to group related formats and transfer option elements in [Record Configurations](#configuration-classes).

In ISO these elements are independent of each other, with no formal mechanism to associate formats and transfer options.
As this library seeks to be fully reversible between a configuration object and XML, this information would be lost
once records are encoded as XML.

To avoid this, this library uses the ID attribute available in both format and transfer option elements with values
can be used when decoding XML to reconstruct these associations. This functionality should be fully transparent to the
user, except for these auto-generated IDs being present in records.

See the [Automatic transfer option / format IDs](#iso-19115-automatic-transfer-option--format-ids) section for more 
details.

**Note:** Do not modify these IDs, as this will break this functionality.

[1]

| Format     | Size   | Download Link                |
| ---------- | ------ | ---------------------------- |
| CSV        | 68 kB  | [Link](https://example.com/) |
| GeoPackage | 1.2 MB | [Link](https://example.com/) |

### Disabling XML declaration

**WARNING:** This feature is deprecated.

**The example below is for the ISO 19115 standard but this applies to all standards.**

To disable the XML declaration (i.e. `<?xml version='1.0' encoding='utf-8'?>`), you can set the `xml_declaration`
parameter to false. This is sometimes needed when the generated XML documented needs to be embedded into a larger
document, such as a CSW transaction.

```python
# disable XML declaration
document = record.generate_xml_document(xml_declaration=False)

# output document
print(document)
```

### Migrating to new configuration versions

#### ISO 19115 Version 1 to version 2

**WARNING:** This feature is deprecated.

Utility methods are provided within the V1 and V2 [Record configuration](#configuration-classes) classes to convert to
and from the V2/V1 [Record Configuration Schema](#configuration-schemas).

**Note:** The version 1 and version 2 schemas are largely, but not fully, backwards compatible. Additional elements
added to the version 2 schema (i.e. for elements the version 1 schema didn't support) will be dropped to prevent
validation errors. For some elements (access/usage constraints), hard coded conversions are used for known use cases.

To convert a record configuration from version 1 to version 2 (lossless for known use cases):

```python
from datetime import date

from bas_metadata_library.standards.iso_19115_1 import (
    MetadataRecordConfigV1 as ISO19115_1_MetadataRecordConfigV1,
    MetadataRecord as ISO19115_1_MetadataRecord,
)

configuration_object = {
    "language": "eng",
    "character_set": "utf-8",
    "hierarchy_level": "dataset",
    "contacts": [{"organisation": {"name": "UK Polar Data Centre"}, "role": ["pointOfContact"]}],
    "date_stamp": date(2018, 10, 18),
    "resource": {
        "title": {"value": "Test Record"},
        "dates": [{"date": date(2018, 1, 1), "date_precision": "year", "date_type": "creation"}],
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
configurationV1 = ISO19115_1_MetadataRecordConfigV1(**configuration_object)
configurationV2 = configurationV1.convert_to_v2_configuration()

# encode converted configuration into an XML document
record = ISO19115_1_MetadataRecord(configurationV2)
document = record.generate_xml_document()

# output document
print(document)
```

To convert a record configuration from version 2 to version 1 (lossy):

```python
from datetime import date

from bas_metadata_library.standards.iso_19115_1 import (
    MetadataRecordConfigV2 as ISO19115_1_MetadataRecordConfigV2,
    MetadataRecordConfigV1 as ISO19115_1_MetadataRecordConfigV1
)

configuration_object = {
    "hierarchy_level": "dataset",
    "metadata": {
        "language": "eng",
        "character_set": "utf-8",
        "contacts": [{"organisation": {"name": "UK Polar Data Centre"}, "role": ["pointOfContact"]}],
        "date_stamp": date(2018, 10, 18),
    },
    "identification": {
        "title": {"value": "Test Record"},
        "dates": {"creation": {"date": date(2018, 1, 1), "date_precision": "year"}},
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
configurationV2 = ISO19115_1_MetadataRecordConfigV2(**configuration_object)
configurationV1 = ISO19115_1_MetadataRecordConfigV1()
configurationV1.convert_from_v2_configuration(configuration=configurationV2)

# print V1 configuration
print(configurationV1.config)
```

## Implementation

This library is implemented in Python and consists of a set of classes used to generate XML metadata records from a
configuration object, or to generate a configuration object from an XML record.

### Metadata Record classes

Each [supported Standard](#supported-standards) and [Supported Profile](#supported-profiles) is implemented as a module
under `bas_metadata_library.standards` (where profiles are implemented as modules under their respective standard).

For each, classes inherited from these parent classes are defined:

* `Namespaces`
* `MetadataRecord`
* `MetadataRecordConfig`

The `namespaces` class is a set of mappings between XML namespaces, their shorthand aliases and their definitions XSDs.

The `MetadataRecord` class represents a metadata record and defines the Root [Element](#element-classes). This class
provides methods to generate an XML document for example.

The `MetadataRecordConfig` class represents the [Configuration](#configuration-classes) used to define values within a
`MetadataRecord`, either for new records, or derived from existing records. This class provides methods to validate the
configuration used in a record for example.

### Element classes

Each supported element, in each [supported standard](#supported-standards), inherit and use the `MetadataRecordElement`
class to:

* encode configuration values into an XML fragment of at least one element
* decode an XML fragment into one or more configuration values

Specifically, at least two methods are implemented:

* `make_element()` which builds an XML element using values from a configuration object
* `make_config()` which uses typically XPath expressions to build a configuration object from XML

These methods may be simple (if encoding or decoding a simple free text value for example), or quite complex through
the use of sub-elements (which themselves may contain sub-elements as needed).

### Configuration classes

The configuration of each metadata record is held in a Python dictionary, within a `MetadataRecordConfig` class. This
class includes methods to validate its configuration against a relevant [Configuration Schema](#configuration-schemas).

Configuration classes are defined at the root of each standard or profile, alongside its root
[Metadata Element](#element-classes) and XML namespaces.

A configuration class will exist for each supported configuration schema with methods to convert from one version to
another, see the [Record configuration schema migration](#migrating-to-new-configuration-versions) section for more
information.

### Configuration schemas

Allowed configuration values for each [supported Standard](#supported-standards) and
[Supported Profile](#supported-profiles) are described by a [JSON Schema](https://json-schema.org). These configuration
schemas include which configuration properties are required, and in some cases, allowed values for these properties.

Configuration schemas are stored as JSON files in the `bas_metadata_library.standards_schemas` module and loaded as
resource files from within this package. Schemas are also made available externally through the BAS Metadata Standards
website, [metadata-standards.data.bas.ac.uk](https://metadata-standards.data.bas.ac.uk), to allow:

1. other applications to ensure their output will be compatible with this library but that can't, or don't want to,
   use this library
2. to allow schema inheritance/extension where used for standards that inherit from other standards (such as profiles)

Configuration schemas a versioned (e.g. `v1`, `v2`) to allow for backwards incompatible changes to be made.

#### Source and distribution schemas

Standards and profiles usually inherit from other standards and profiles. In order to prevent this creating huge
duplication within configuration schemas, inheritance is used to incorporate a base schema and extend it as needed. For
example, the ISO 19115-2 standard extends, and therefore incorporates the configuration schema for, ISO 19115-1.

JSON Schema references and identifier properties are used to implement this, using URIs within the BAS Metadata
Standards website. Unfortunately, this creates a problem when developing these schemas, as if Schema B relies on Schema
A, using its published identifier as a reference, the published instance of the schema will be used (i.e. the remote
schema will be downloaded when Schema B is validated). If Schema A is being developed, and is not ready to be
republished, there is a difference between the local and remote schemas used, creating unreliable tests for example.

To avoid this problem, a set of *source* schemas are used which use references to avoid duplication, from which a set
of *distribution* schemas are generated. These distribution schemas inline any references contained in their source
counterpart. These distribution schemas are therefore self-contained and can be updated locally without any
dependencies on remote sources. Distribution schemas are used by [Configuration Classes](#configuration-classes) and
published to the BAS Metadata Standards website, they are located in the `bas_metadata_library.schemas.dist` module.

When editing configuration schemas, you should edit the source schemas, located in the
`bas_metadata_library.schemas.src` module, then run the
[regenerate distribution schemas](#generating-configuration-schemas) using an internal command line utility.

JSON Schema's can be developed using [jsonschemavalidator.net](https://www.jsonschemavalidator.net).

### Adding a new standard

To add a new standard:

1. create a new module under `bas_metadata_library.standards`, e.g. `bas_metadata_library.standards.foo_v1/__init__.py`
2. in this module, overload the `Namespaces`, `MetadataRecordConfig` and `MetadataRecord` classes as needed
3. create a suitable metadata configuration JSON schema in `bas_metadata_library.schemas.src`
   e.g. `bas_metadata_library.schemas.src.foo_v1.json`
4. update the `generate_schemas` method in `manage.py` to generate distribution schemas
5. add a script line to the `publish-schemas-stage` and `publish-schemas-prod` jobs in `.gitlab-ci.yml`, to publish
   the distribution schema within the BAS Metadata Standards website
6. define a series of test configurations (e.g. minimal, typical and complete) for generating test records in
   `tests/resources/configs/` e.g. `tests/resources/configs/foo_v1_standard.py`
7. update the inbuilt Flask application in `app.py` with a route for generating test records for the new standard
8. use the inbuilt Flask application to generate the test records and save to `tests/resources/records/`
9. add relevant [tests](#testing) with methods to test each metadata element class and test records

### Adding a new element to an existing standard

[WIP]

1. [amend configuration schema](#configuration-schemas):
   * new or changed properties should be added to the configuration for the relevant standard (e.g. ISO 19115-1)
   * typically, this involves adding new elements to the `definitions` property and referencing these in the relevant
     parent element (e.g. to the `identification` property)
2. [generate distribution schemas](#generating-configuration-schemas)
3. amend test configs:
   * new or changed properties should be made to the relevant test record configurations in `tests/resources/configs/`
   * there are different levels of configuration, from minimal to complete, which should, where possible, build on
     each other (e.g. the complete record should include all the properties and values of the minimal record)
   * the `minimum` configuration should not be changed, as all mandatory elements are already implemented
   * the `base_simple` configuration should contain elements used most of the time, that use free-text values
   * the `base_complex` configuration should contain elements used most of the time, that use URL or other
     identifier values
   * the `complete` configuration should contain examples of all supported elements, providing this still produces a
     valid record, in order to ensure high test coverage
   * where possible, configurations should be internally consistent, but this can be ignored if needed
   * values used for identifiers and other external references should use the correct form/structure but do not need
     to exist or relate to the resource described by each configuration (i.e. DOIs should be valid URLs but could be
     a DOI for another resource for example)
4. add relevant [element class](#element-classes):
   * new or changed elements should be added to the configuration for the relevant package for each standard
   * for the ISO 19115 family of standards, element classes should be added to the `iso_19115_common` package
   * the exact module to use within this package will depend on the nature of the element being added, but in general,
     elements should be added to the module of their parent element (e.g. `data_identification.py` for elements
     under the `identification` record configuration property), elements used across a range of elements should be
     added to the `common_elements.py` module
   * remember to include references to new element class in the parent element class (in both the `make_element` and
     `make_config` methods)
5. until support for Version 1 configuration schemas is removed, add logic to the
   `bas_metadata_library.standards.iso_19115_common.utils.convert_from_v1_to_v2_configuration` and/or
   `bas_metadata_library.standards.iso_19115_common.utils.convert_from_v2_to_v1_configuration` methods as needed
   * for new elements, this usually consists of deleting configuration properties that don't exist in the V1 schema
     (as additional/unexpected keys are not allowed and will therefore fail validation)
   * for existing elements, logic may be needed to both upgrade and downgrade configurations, especially where
     refactoring has occurred between V1 and V2 configurations
   * where possible, such logic should be generic and agnostic to values used for configuration options, however
     there may be cases where this is unavoidable in order to produce a more complete translation between versions
   * if such logic would prove very unwieldy, and not confined to a limited set of known circumstances, it is ok to
     not implement such logic, on the basis that supporting multiple versions is temporary
6. [capture test records](#capturing-static-test-records)
    * initially this acts as a good way to check new or changed element classes encode configuration properties
      correctly
    * check the git status of these test records to check existing records have changed how you expect (and haven't
      changed things you didn't intend to for example)
7. add tests
    * new test cases should be added, or existing test cases updated, in the relevant module within
      `tests/bas_metadata_library/`
    * for the ISO 19115 family of standards, this should be `test_standard_iso_19115_1.py`, unless the element is only
      part of the ISO 19115-2 standard
    * providing there are enough test configurations to test all the ways a new element can be used (e.g. with a simple
      text string or anchor element for example), adding a test case for each element is typically enough to ensure
      sufficient test coverage
    * where this isn't the case, it's suggested to add one or more 'edge case' test cases to test remaining code paths
      explicitly
8. check [test coverage](#test-coverage)
    * for missing coverage, consider adding edge case test cases where applicable
    * wherever possible, the coverage exemptions should be minimised
    * there are a number of general types of code that can be exempted as part of an existing convention (but that
      will be reviewed in the future):
        * within `make_config` methods to check whether child elements are empty
        * within the `convert_from_v1_to_v2_configuration` and `convert_from_v2_to_v1_configuration` utility methods
    * where exceptions are added, they should be documented as an issue with information on how they will be
      addressed in the longer term
    * issue
      [#111](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/-/issues/111))
      will document existing exceptions and conventions, and look at how these can be removed in the future
9. update `README.md` examples if common element
    * this is probably best done before releasing a new version
10. update `CHANGELOG.md`
11. if needed, add name to `authors` property in `pyproject.toml`

### ISO 19115 - Automatic transfer option / format IDs

ID attributes are automatically added to `gmd:MD_Format` and `gmd:MD_DigitalTransferOptions` elements in order to
reconstruct related formats and transfer options (see the
[Linking transfer options and formats](#linking-transfer-options-and-formats) section for more information).

When a record is encoded, ID values are generated by hashing a JSON encoded string of the distribution object. This
ID is used as a shared base between the format and transfer option, with `-fmt` appended for the format and `-tfo`
for the transfer option.

When a record is decoded, ID values are extracted (stripping the `-fmt`/`-tfo` suffixes) to index and then match up
format and transfer options back into distribution options. Any format and transfer options without an ID value, or
without a corresponding match, are added as partial distribution options.

As a worked example for encoding a (simplified) distribution object such as:

```python
do = {
   'format': 'csv',
   'transfer_option': {
      'size': '40',
      'url': 'https://example.com/foo.csv'
   }
}
```

Becomes:

```
'{"format":"csv","transfer_option":{"size":40,"url":"https://example.com/foo.csv"}}'
```

When encoded as a JSON encoded string, which when hashed becomes:

```
16b7b5df78a664b15d69feda7ccc7caed501f341
```

The ID value added to the `gmd:MD_Format` element would be:

```xml
<gmd:MD_Format id="16b7b5df78a664b15d69feda7ccc7caed501f341-fmt">
```

And for the `gmd:MD_DigitalTransferOptions` element:

```xml
<gmd:MD_DigitalTransferOptions id="16b7b5df78a664b15d69feda7ccc7caed501f341-tfo">
```

## Setup

### Terraform

Terraform is used to provision resources required to operate this application in staging and production environments.

These resources allow [Configuration schemas](#configuration-schemas) for each standard to be accessed externally.

Access to the [BAS AWS account](https://gitlab.data.bas.ac.uk/WSF/bas-aws) is needed to provisioning these resources.

**Note:** This provisioning should have already been performed (and applies globally). If changes are made to this
provisioning it only needs to be applied once.

```shell
# start terraform inside a docker container
$ cd provisioning/terraform
$ docker compose run terraform
# setup terraform
$ terraform init
# apply changes
$ terraform validate
$ terraform fmt
$ terraform apply
# exit container
$ exit
$ docker compose down
```

#### Terraform remote state

State information for this project is stored remotely using a
[Backend](https://www.terraform.io/docs/backends/index.html).

Specifically the [AWS S3](https://www.terraform.io/docs/backends/types/s3.html) backend as part of the
[BAS Terraform Remote State](https://gitlab.data.bas.ac.uk/WSF/terraform-remote-state) project.

Remote state storage will be automatically initialised when running `terraform init`. Any changes to remote state will
be automatically saved to the remote backend, there is no need to push or pull changes.

##### Remote state authentication

Permission to read and/or write remote state information for this project is restricted to authorised users. Contact
the [BAS Web & Applications Team](mailto:servicedesk@bas.ac.uk) to request access.

See the [BAS Terraform Remote State](https://gitlab.data.bas.ac.uk/WSF/terraform-remote-state) project for how these
permissions to remote state are enforced.

## Development

This API is developed as a Python library. A bundled Flask application is used to simulate its usage, act as
framework for running tests etc., and provide utility methods for generating schemas etc.

### Development environment

Git, Docker and Docker Compose are required to set up a local development environment of this application.

If you have access to the [BAS GitLab instance](https://gitlab.data.bas.ac.uk), you can clone the project and pull
Docker images from the BAS GitLab instance and BAS Docker Registry.

```shell
$ git clone https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator.git
$ cd metadata-generator
$ docker login docker-registry.data.bas.ac.uk
$ docker compose pull
```

Otherwise, you will need to build the Docker image locally.

```shell
$ git clone https://github.com/antarctica/metadata-library.git
$ cd metadata-library
$ docker compose build
```

To run the application using the Flask development server (which reloads automatically if source files are changed):

```shell
$ docker compose up
```

To run other commands against the Flask application (such as [Tests](#testing)):

```shell
# in a separate terminal to `docker compose up`
$ docker compose run app flask [command]
# E.g.
$ docker compose run app flask test
# List all available commands
$ docker compose run app flask
```

### Code Style

PEP-8 style and formatting guidelines must be used for this project, with the exception of the 80 character line limit.

[Black](https://github.com/psf/black) is used to ensure compliance, configured in `pyproject.toml`.

Black can be [integrated](https://black.readthedocs.io/en/stable/editor_integration.html#pycharm-intellij-idea) with a
range of editors, such as PyCharm, to perform formatting automatically.

To apply formatting manually:

```shell
$ docker compose run app black bas_metadata_library/
```

To check compliance manually:

```shell
$ docker compose run app black --check bas_metadata_library/
```

Checks are ran automatically in [Continuous Integration](#continuous-integration).

### Dependencies

Python dependencies for this project are managed with [Poetry](https://python-poetry.org) in `pyproject.toml`.

Non-code files, such as static files, can also be included in the [Python package](#python-package) using the
`include` key in `pyproject.toml`.

#### Adding new dependencies

To add a new (development) dependency:

```shell
$ docker compose run app ash
$ poetry add [dependency] (--dev)
```

Then rebuild the development container, and if you can, push to GitLab:

```shell
$ docker compose build app
$ docker compose push app
```

#### Updating dependencies

```shell
$ docker compose run app ash
$ apk update
$ apk add build-base cargo
$ poetry update
```

Then rebuild the development container, and if you can, push to GitLab:

```shell
$ docker compose build app
$ docker compose push app
```

#### `jsonschema` package

The `jsonschema` dependency is locked to version 3.2.0 because version 4.0 > dropped Python 3.6 support. This
library cannot require newer Python versions to ensure it can be used in projects that run on BAS IT infrastructure.

#### `lxml` package

The `lxml` dependency takes a long time to install/update inside the container image because it needs to be installed
from source each time the container is built. This is because Alpine Linux, used by the official Python Docker base
images, is not supported by the Python [manylinux](https://github.com/pypa/manylinux) system, and therefore cannot use
pre-built, binary, wheels.

### Static security scanning

To ensure the security of this API, source code is checked against [Bandit](https://github.com/PyCQA/bandit) for issues
such as not sanitising user inputs or using weak cryptography.

**Warning:** Bandit is a static analysis tool and can't check for issues that are only be detectable when running the
application. As with all security tools, Bandit is an aid for spotting common mistakes, not a guarantee of secure code.

Through [Continuous Integration](#continuous-integration), each commit is tested.

To check locally:

```shell
$ docker compose run app bandit -r . -x './tests'
```

### Editor support

#### PyCharm

A run/debug configuration, *App*, is included in the project.

### Generating configuration schemas

To generate [distribution schemas from source schemas](#source-and-distribution-schemas), a custom Flask CLI command,
`generate-schemas` is available. The [`jsonref`](https://jsonref.readthedocs.io/en/latest/) library is used to resolve
any references in source schemas and write the output as distribution schemas, replacing any existing output.

```shell
# then in a separate terminal:
$ docker compose run app flask generate-schemas
```

To configure this command, (e.g. to add a new schema for a new standard/profile), adjust the `schemas` list in the
`generate_schemas` method in `manage.py`. This list should contain dictionaries with keys for the common name of the
schema (based on the common file name of the schema JSON file), and whether the source schema should be resolved or
simply copied. This should be true by default, and is only relevant to schemas that do not contain any references, as
this will cause an error if resolved.

## Testing

All code in the `bas_metadata_library` module must be covered by tests, defined in `tests/`. This project uses
[PyTest](https://docs.pytest.org/en/latest/) which should be ran in a random order using
[pytest-random-order](https://pypi.org/project/pytest-random-order/).

Tests are written to create metadata records based on a series of configurations defined in `tests/resources/configs/`.
These define 'minimal' to 'complete' test records, intended to test different ways a standard can be used, both for
individual elements and whole records. These tests are designed to ensure that records are generally well-formed and
that where config options are used the corresponding elements in the metadata record are generated.

As this library does not seek to support all possible elements and variations within each standard, these tests are
similarly not exhaustive, nor are they a substitute for formal metadata validation.

Test methods are used to test individual elements are formed correctly. Comparisons against static records are used to
test the structure of whole records.

To run tests manually from the command line:

```shell
$ docker compose run app pytest --random-order
```

To run tests manually using PyCharm, use the included *App (Tests)* run/debug configuration.

Tests are ran automatically in [Continuous Integration](#continuous-integration).

### Capturing static test records

To capture static test records, which verify complete records are assembled correctly, a custom Flask CLI command,
`capture-test-records` is available. This requires the Flask application to first be running. The Requests library is
used to make requests against the Flask app save responses to a relevant directory in `tests/resources/records`.

```shell
# start Flask application:
$ docker compose up
# then in a separate terminal:
$ docker compose run app flask capture-test-records
```

It is intended that this command will update pre-existing static records, with differences captured in version control
and reviewed manually to ensure they are correct.

### Test coverage

[pytest-cov](https://pypi.org/project/pytest-cov/) is used to measure test coverage.

To prevent noise, `.coveragerc` is used to omit empty `__init__.py` files from reports.

To measure coverage manually:

```shell
$ docker compose run app pytest --random-order --cov=bas_metadata_library --cov-fail-under=100 --cov-report=html .
```

[Continuous Integration](#continuous-integration) will check coverage automatically and fail if less than 100%.

### Continuous Integration

All commits will trigger a Continuous Integration process using GitLab's CI/CD platform, configured in `.gitlab-ci.yml`.

## Deployment

### Python package

This project is distributed as a Python package, hosted in [PyPi](https://pypi.org/project/bas-metadata-library).

Source and binary packages are built and published automatically using
[Poetry](https://python-poetry.org/docs/cli/#publish) in [Continuous Delivery](#continuous-deployment).

### Continuous Deployment

A Continuous Deployment process using GitLab's CI/CD platform is configured in `.gitlab-ci.yml`.

## Release procedure

For all releases:

1. create a release branch
2. close release in `CHANGELOG.md`
3. bump package version using `docker compose run app poetry version`
4. push changes, merge the release branch into `master` and tag with version

## Feedback

The maintainer of this project is the BAS Web & Applications Team, they can be contacted at:
[servicedesk@bas.ac.uk](mailto:servicedesk@bas.ac.uk).

## Issue tracking

This project uses issue tracking, see the
[Issue tracker](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/issues) for more
information.

**Note:** Read & write access to this issue tracker is restricted. Contact the project maintainer to request access.

## License

Copyright (c) 2019-2021 UK Research and Innovation (UKRI), British Antarctic Survey.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
