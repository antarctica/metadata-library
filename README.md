# BAS Metadata Library

Python library for generating metadata and data records.

## Overview

**Note:** This project is focused on needs within the British Antarctic Survey. It has been open-sourced in case it is
of interest to others. Some resources, indicated with a '🛡' or '🔒' symbol, can only be accessed by BAS staff or
project members respectively. Contact the [Project Maintainer](#project-maintainer) to request access.

### Purpose

This library is designed to assist in generating metadata and data records, primarily for the discovery of datasets,
services, features and related resources. This project is intended to be used as an underpinning library within tools,
to avoid the need to duplicate the implementation of complex and verbose metadata and data standards.

At a high level, this library allows a configuration object, representing the fields/structure of a standard, to be
encoded into its formal representation set out by that standard (typically using XML). It also allows such a formal
representation to be decoded back into a configuration object, which can be more easily used or manipulated.

### Supported standards

| Standard                                                        | Implementation                                                  | Library Namespace                                   | Introduced In                                                                                        |
|-----------------------------------------------------------------|-----------------------------------------------------------------|-----------------------------------------------------|------------------------------------------------------------------------------------------------------|
| [ISO 19115:2003](https://www.iso.org/standard/26020.html)       | [ISO 19139:2007](https://www.iso.org/standard/32557.html)       | `bas_metadata_library.standards.iso_19115_0_v1`     | [#46 🛡️](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/issues/46)   |
| [ISO 19115-2:2009](https://www.iso.org/standard/39229.html)     | [ISO 19139-2:2012](https://www.iso.org/standard/57104.html)     | `bas_metadata_library.standards.iso_19115_2_v1`     | [#50 🛡️](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/issues/50)   |
| [IEC 61174:2015](https://webstore.iec.ch/publication/23128)     | [IEC 61174:2015](https://webstore.iec.ch/publication/23128)     | `bas_metadata_library.standards.iec_pas_61174_0_v1` | [#139 🛡️](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/issues/139) |
| [IEC PAS 61174:2021](https://webstore.iec.ch/publication/67774) | [IEC PAS 61174:2021](https://webstore.iec.ch/publication/67774) | `bas_metadata_library.standards.iec_pas_61174_1_v1` | [#139 🛡️](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/issues/144) |

**Note:** In this library, starting from version v0.11.0, the *ISO 19115:2003* standard is referred to as *ISO-19115-0*
(`iso_19115_0`). Prior to this version it was (incorrectly) referred to as *ISO-19115-1* (`iso_19115_1`). To avoid
confusion, when the [ISO 19115-1:2014](https://www.iso.org/standard/53798.html) standard is implemented, it will be
referred to as *ISO-19115-3* (`iso_19115_3`).

### Supported profiles

| Standard  | Profile                                                                                               | Introduced In                                                                                    |
|-----------|-------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| ISO 19115 | [MAGIC Discovery Metadata V1](https://metadata-standards.data.bas.ac.uk/profiles/magic-discovery-v1/) | [#250](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/issues/250) |

### Supported configuration versions

| Standard           | Profile | Configuration Version                                                                                                     | Status  | Notes                                 |
|--------------------|---------|---------------------------------------------------------------------------------------------------------------------------|---------|---------------------------------------|
| ISO 19115:2003     | -       | [`v1`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-1-v1.json)     | Retired | Replaced by `v2`, no longer supported |
| ISO 19115:2003     | -       | [`v2`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-1-v2.json)     | Retired | Replaced by `v3`, no longer supported |
| ISO 19115:2003     | -       | [`v3`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v3/iso-19115-1-v3.json)     | Retired | Replaced by `v4`, no longer supported |
| ISO 19115:2003     | -       | [`v4`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v3/iso-19115-0-v4.json)     | Stable  | Currently supported version           |
| ISO 19115-2:2009   | -       | [`v1`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v1.json)     | Retired | Replaced by `v2`, no longer supported |
| ISO 19115-2:2009   | -       | [`v2`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v2.json)     | Retired | Replaced by `v3`, no longer supported |
| ISO 19115-2:2009   | -       | [`v3`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v3.json)     | Retired | Replaced by `v4`, no longer supported |
| ISO 19115-2:2009   | -       | [`v4`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v4.json)     | Stable  | Currently supported version           |
| IEC 61174:2015     | -       | [`v1`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iec-pas-61174-0-v1.json) | Stable  | Currently supported version           |
| IEC PAS 61174:2021 | -       | [`v1`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iec-pas-61174-1-v1.json) | Stable  | Currently supported version           |

### Supported standards coverage

This library is built around the needs of the British Antarctic Survey and the NERC (UK) Polar Data Centre. This means
only standards, and elements of these standards, used by BAS or the UK PDC are supported. However, additions that would
enable this library to be useful to other organisations and use-case are welcome as contributions providing they do not
add significant complexity or maintenance.

| Standard           | Coverage | Coverage Summary                                                                                     |
|--------------------|----------|------------------------------------------------------------------------------------------------------|
| ISO 19115:2003     | Good     | All mandatory elements are supported with a good number of commonly used additional elements         |
| ISO 19115-2:2009   | Minimal  | No elements from this extension are supported, with the exception of the root element                |
| IEC 61174:2015     | Minimal  | All mandatory elements are supported, plus a limited number of optional route information attributes |
| IEC PAS 61174:2021 | Minimal  | All mandatory elements are supported, plus a limited number of optional route information attributes |

**Note:** ISO 19115 extensions (i.e. `gmd:metadataExtensionInfo` elements) are not supported.

#### Coverage for IEC 61174

As required by the IEC 61174 standard, this library supports the following properties within this standard:

| Element                                        | Reference | Obligation |
|------------------------------------------------|-----------|------------|
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

This package depends on native libraries for XML encoding and decoding:

* `libxml2`
* `libxslt`

This package depends on native binaries for XML validation:

* `xmllint`

Most Operating Systems include these libraries and packages by default. However, others, particularly minimal OSes,
require these packages to be installed separately. Notably:

| Operating System | Required Packages              |
|------------------|--------------------------------|
| Linux (Alpine)   | `libxslt-dev`, `libxml2-utils` |
| Linux (Debian)   | `libxml2-utils`                |

## Usage

### Encode an ISO 19115 metadata record

To generate an ISO 19115 metadata record from a Python record configuration and return it as an XML document:

```python
from datetime import date

from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV4, MetadataRecord

minimal_record_config = {
    "$schema": "https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-1-v4.json",
    "hierarchy_level": "dataset",
    "metadata": {
        "language": "eng",
        "character_set": "utf8",
        "contacts": [{"organisation": {"name": "UK Polar Data Centre"}, "role": ["pointOfContact"]}],
        "date_stamp": date(2018, 10, 18),
    },
    "identification": {
        "title": {"value": "Test Record"},
        "dates": {"creation": {"date": date(2018, 1, 1), "date_precision": "year"}},
        "abstract": "Test Record for ISO 19115 metadata standard (no profile) with required properties only.",
        "character_set": "utf8",
        "language": "eng",
        "topics": ["environment", "climatologyMeteorologyAtmosphere"],
        "extents": [
            {
                "identifier": "bounding",
                "geographic": {
                    "bounding_box": {
                        "west_longitude": -45.61521,
                        "east_longitude": -27.04976,
                        "south_latitude": -68.1511,
                        "north_latitude": -54.30761,
                    }
                },
            },
        ],
    },
}
configuration = MetadataRecordConfigV4(**minimal_record_config)
record = MetadataRecord(configuration=configuration)
document = record.generate_xml_document()

# output document
print(document.decode())
```

See the [HTML Entities](#html-entities) section for guidance on using accents and symbols in descriptions.

You will need to use a `date_precision` property for partial dates. See the [Date Precision](#date-precision) section
for more information.

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

output_path = str('/path/to/file.rtzp')

minimal_record_config = {"route_name": "minimal-test-route",
    "waypoints": [
        {"id": 1001, "revision": 0, "position": {"lat": 5, "lon": 50}},
        {"id": 1002, "revision": 0, "position": {"lat": 5, "lon": 50}},
        {"id": 1003, "revision": 0, "position": {"lat": 5, "lon": 50}},
    ],
}
configuration = MetadataRecordConfigV1(**minimal_record_config)
record = MetadataRecord(configuration=configuration)
record.generate_rtzp_archive(file=Path(output_path))
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

input_path = str('/path/to/file.rtzp')

record = MetadataRecord()
record.load_from_rtzp_archive(file=Path(input_path))
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

from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV4

input_path = str('/path/to/file.json')

configuration = MetadataRecordConfigV4()
configuration.load(file=Path(input_path))
```

### Dumping a record configuration to JSON

**The example below is for the ISO 19115 standard but this applies to all standards.**

The `dump()` and `dumps()` methods on the configuration class can be used to dump a record configuration to a JSON
encoded file or string respectively:

```python
from datetime import date
from pathlib import Path

from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV4

output_path = str('/path/to/file.json')

minimal_record_config = {
    "$schema": "https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v4.json",
    "hierarchy_level": "dataset",
    "metadata": {
        "language": "eng",
        "character_set": "utf8",
        "contacts": [{"organisation": {"name": "UK Polar Data Centre"}, "role": ["pointOfContact"]}],
        "date_stamp": date(2018, 10, 18),
    },
    "identification": {
        "title": {"value": "Test Record"},
        "dates": {"creation": {"date": date(2018, 1, 1), "date_precision": "year"}},
        "abstract": "Test Record for ISO 19115 metadata standard (no profile) with required properties only.",
        "character_set": "utf8",
        "language": "eng",
        "topics": ["environment", "climatologyMeteorologyAtmosphere"],
        "extents": [
            {
                "identifier": "bounding",
                "geographic": {
                    "bounding_box": {
                        "west_longitude": -45.61521,
                        "east_longitude": -27.04976,
                        "south_latitude": -68.1511,
                        "north_latitude": -54.30761,
                    }
                },
            },
        ],
    },
}
configuration = MetadataRecordConfigV4(**minimal_record_config)
configuration.dump(file=Path(output_path))
```

### Validating a record

**The example below is for the ISO 19115 standard but this applies to all standards.**

The formal encoding of a record can be validated against one or more XML schemas relevant to each metadata or data
standard. Records are not validated automatically, and so must be validated explicitly:

```python
from datetime import date

from bas_metadata_library import RecordValidationError
from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV4, MetadataRecord

minimal_record_config = {
    "$schema": "https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v4.json",
    "hierarchy_level": "dataset",
    "metadata": {
        "language": "eng",
        "character_set": "utf8",
        "contacts": [{"organisation": {"name": "UK Polar Data Centre"}, "role": ["pointOfContact"]}],
        "date_stamp": date(2018, 10, 18),
    },
    "identification": {
        "title": {"value": "Test Record"},
        "dates": {"creation": {"date": date(2018, 1, 1), "date_precision": "year"}},
        "abstract": "Test Record for ISO 19115 metadata standard (no profile) with required properties only.",
        "character_set": "utf8",
        "language": "eng",
        "topics": ["environment", "climatologyMeteorologyAtmosphere"],
        "extents": [
            {
                "identifier": "bounding",
                "geographic": {
                    "bounding_box": {
                        "west_longitude": -45.61521,
                        "east_longitude": -27.04976,
                        "south_latitude": -68.1511,
                        "north_latitude": -54.30761,
                    }
                },
            },
        ],
    },
}
configuration = MetadataRecordConfigV4(**minimal_record_config)
record = MetadataRecord(configuration=configuration)

try:
    record.validate()
except RecordValidationError as e:
    print('Record invalid')
    print(e)
```

Where the contents of the record is invalid, a `RecordValidationError` exception will be raised. Printing this
exception will return validation errors.

These errors should not happen, and if they do are considered internal bugs and [Reported](#project-maintainer).

See the [Record Schemas](#record-schemas) section for more information on how validation works.

### Validating a record configuration

**The example below is for the ISO 19115 standard but this applies to all standards.**

Record configurations will be automatically validated using a JSON Schema for the metadata or data standard used.

Where a record configuration states compliance with one or more [Supported Profiles](#supported-profiles) applicable to
the metadata or data standard, it will also be automatically validated using a JSON Schema for each profile.

To explicitly validate a record configuration:

```python
from datetime import date

from jsonschema import ValidationError
from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV4

minimal_record_config = {
    "$schema": "https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v4.json",
    "hierarchy_level": "dataset",
    "metadata": {
        "language": "eng",
        "character_set": "utf8",
        "contacts": [{"organisation": {"name": "UK Polar Data Centre"}, "role": ["pointOfContact"]}],
        "date_stamp": date(2018, 10, 18),
    },
    "identification": {
        "title": {"value": "Test Record"},
        "dates": {"creation": {"date": date(2018, 1, 1), "date_precision": "year"}},
        "abstract": "Test Record for ISO 19115 metadata standard (no profile) with required properties only.",
        "character_set": "utf8",
        "language": "eng",
        "topics": ["environment", "climatologyMeteorologyAtmosphere"],
        "extents": [
            {
                "identifier": "bounding",
                "geographic": {
                    "bounding_box": {
                        "west_longitude": -45.61521,
                        "east_longitude": -27.04976,
                        "south_latitude": -68.1511,
                        "north_latitude": -54.30761,
                    }
                },
            },
        ],
    },
}
configuration = MetadataRecordConfigV4(**minimal_record_config)

try:
    configuration.validate()
except ValidationError as e:
    print('Record configuration invalid')
    print(e)
```

Where the contents of the record is invalid, a
[`ValidationError`](https://python-jsonschema.readthedocs.io/en/stable/errors/#jsonschema.exceptions.ValidationError)
exception will be raised by the underlying JSON Schema library. Printing this exception will return validation errors.

**Note:** The first validation error encountered will stop further validation.

See the [Record Configuration Schemas](#configuration-schemas) section for more information.

### HTML entities

Do not include HTML entities in input to this library, as they will be double escaped by [Lxml](https://lxml.de), the
underlying XML processing library used by this project. Instead, literal characters should be used (e.g. `>`), which
will be escaped as needed automatically. This applies to any unicode character, such as accents (e.g. `å`) and
symbols (e.g. `µ`).

E.g. If `&gt;`, the HTML entity for `>` (greater than), were used as input, it would be escaped again to `&amp;gt;`
which will not be valid output.

### Date Precision

When using Python for record configurations, date or date times must be structured as dictionaries with a `date`
value (which can be a Python date or date time object), and optional `date_precision` property for indicating elements
in the date or date time object should be ignored when encoding records. This property can be set to either:

* `year` (month and day are unknown)
* `month` (day is unknown)

When decoding a record, partial dates or date times will be detected and a `date_precision` property added
automatically. Unknown elements of a date or date time should, or will, use '1' as a conventional value, which can
effectively be ignored. This is necessary as Python does not allow unknown date elements to be omitted.

When using JSON for record configurations, date or date times must be written as strings. Partial dates or date
times can be expressed naturally (e.g. `2012-04`), without the need for a `date_precision` property. This library will
automatically convert strings to or from dictionaries, with a `date_precision` property if needed, when loading from,
or saving to, JSON.

Summary table:

| Date Precision | Python Encoding                                                                | JSON Encoding           | XML Encoding            |
|----------------|--------------------------------------------------------------------------------|-------------------------|-------------------------|
| Year           | `{'date': date(year=2012, month=1, day=1), 'date_precision': 'year'}`          | `"2012"`                | `"2012"`                |
| Month          | `{'date': date(year=2012, month=4, day=1), 'date_precision': 'month'}`         | `"2012-04"`             | `"2012-04"`             |
| Day            | `{'date': date(year=2012, month=4, day=14)}`                                   | `"2012-04-14"`          | `"2012-04-14"`          |
| Hour           | `{'date': datetime(year=2012, month=4, day=14, hour=6)}`                       | `"2012-04-14T06"`       | `"2012-04-14T06"`       |
| Minute         | `{'date': datetime(year=2012, month=4, day=14, hour=6, minute=30)}`            | `"2012-04-14T06:30"`    | `"2012-04-14T06:30"`    |
| Second         | `{'date': datetime(year=2012, month=4, day=14, hour=6, minute=30, second=42)}` | `"2012-04-14T06:30:42"` | `"2012-04-14T06:30:42"` |

**Note:** For date times, the UTC timezone is assumed unless set.

### ISO 19115 - linkages between transfer options and formats

In ISO 19115, there is no formal mechanism to associate file distribution formats and transfer options. As this library
seeks to be fully reversible between a configuration object and formal XML encoding, associations between these elements
would be lost when records are encoded as XML. These associations are used to produce download tables such as [1].

In [Record Configurations](#configuration-classes), these associations are encoded using a 'distribution option'
concept. In formal XML records, these associations are encoded using `xsd:ID` attributes in `gmd:MD_Format` and
`gmd:DigitalTransferOptions` elements, with values that allow these associations to be reconstructed when decoding XML.

**Note:** Do not modify automatically assigned IDs, as this will break this functionality.

See the [Automatic transfer option / format IDs](#iso-19115-automatic-transfer-option-format-ids) section for more
information.

[1]

| Format     | Size   | Download Link                |
|------------|--------|------------------------------|
| CSV        | 68 kB  | [Link](https://example.com/) |
| GeoPackage | 1.2 MB | [Link](https://example.com/) |

## Implementation

This library is implemented in Python and consists of a set of classes used to generate XML metadata and data records
from a configuration object, or to generate a configuration object from an XML record.

Each [supported Standard](#supported-standards) is implemented as a module under `bas_metadata_library.standards`. Each
[Supported Profile](#supported-profiles) is implemented as modules under their respective standard.

### Base classes

For each standard and profile, instances of these base classes are defined:

* `Namespaces`
* `MetadataRecord`
* `MetadataRecordConfig`

The `namespaces` class is a set of mappings between XML namespaces, their shorthand aliases and their definitions XSDs.

The `MetadataRecord` class represents a metadata record and defines the Root [Element](#record-element-classes). This
class provides methods to generate an XML document for example.

The `MetadataRecordConfig` class represents the [Configuration](#configuration-classes) used to define values within a
`MetadataRecord`, either for new records, or derived from existing records. This class provides methods to validate the
configuration used in a record for example.

### Record element classes

Each supported element, in each [supported standard](#supported-standards), inherit and use the `MetadataRecordElement`
class to:

* encode configuration values into an XML fragment of at least one element
* decode an XML fragment into one or more configuration values

Specifically, at least two methods are implemented:

* `make_element()` which builds an XML element using values from a configuration object
* `make_config()` which uses typically XPath expressions to build a configuration object from XML

These methods may be simple (if encoding or decoding a simple free text value for example), or quite complex, using
sub-elements (which themselves may contain sub-elements as needed).

### Record schemas

Allowed elements, attributes and values for each [supported Standard](#supported-standards), and if applicable,
[Supported Profile](#supported-profiles) are defined using one or more [XML Schemas](https://www.w3.org/XML/Schema).
These schemas define any required entities, and any entities with enumerated values. Schemas are usually published by
standards organisations to facilitate record validation.

For performance reasons, and to ensure required schemas are not unavailable (due to remote locations being reorganised,
or during server maintenance etc.), these schema files are stored within this package. Schemas are stored as XML Schema
Definition (XSD) files in the `bas_metadata_library.schemas.xsd` module, and loaded as resource files for use in record
validation.

**Note:** To support local validation, imported or included schema locations in local versions of XML schemas, have
been modified. These changes do not usually change the substance of any schema.

**Note:** In some cases, material changes *have* been made to local versions of schemas, in order to workaround
specific issues. These changes are documented and explained below.

#### Altered Metadata Schema - Geographic Metadata (GMD)

The ISO *Geographic Metadata (GMD)* schema (used directly for the ISO 19115-0 standard, and indirectly in the ISO
19115-2 standard) has been modified to:

1. include the ISO *Geographic Metadata XML (GMX)* schema:
    * in order to allow Anchor elements to substitute primitive/simple values (such as character strings and integers),
    * as defined in the ISO 19139:2007 and ISO 19139:2012 standards

### Configuration classes

The configuration of each metadata record is held in a Python dictionary, within a `MetadataRecordConfig` class. This
class includes methods to validate its configuration against a relevant [Configuration Schema](#configuration-schemas).

Configuration classes are defined at the root of each standard, alongside its root
[Metadata Element](#record-element-classes) and XML namespaces.

A configuration class will exist for each supported configuration schema with methods to convert from one version to
another.

### Configuration schemas

Allowed properties and values for record configurations for each [supported Standard](#supported-standards) and
[Supported Profile](#supported-profiles) are defined using a [JSON Schema](https://json-schema.org). These schemas
define any required properties, and any properties with enumerated values.

Configuration schemas are stored as JSON files in the `bas_metadata_library.schemas` module, and loaded as resource
files from within this package to validate record configurations. Schemas are also made available externally through
the BAS Metadata Standards website, [metadata-standards.data.bas.ac.uk](https://metadata-standards.data.bas.ac.uk), to
allow:

1. other applications to ensure their output will be compatible with this library - where they can't, or don't want to,
   use this library directly
2. schema inheritance/extension - for standards that inherit from other standards (such as extensions or profiles)

Configuration schemas are versioned (e.g. `v1`, `v2`) to allow for backwards incompatible changes to be made.
Upgrade/Downgrade methods will be provided for a limited time to assist migrating record configurations between schema
versions.

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
`bas_metadata_library.schemas.src` module, then
[generate distribution schemas](/DEVELOPING.md#generating-configuration-schemas).

JSON Schema's can be developed using [jsonschemavalidator.net](https://www.jsonschemavalidator.net).

For ISO 19115 schemas only, which are currently essentially identical, a shortcut is taken for resolving references
whereby the common members of the two schemas are directly copied from the ISO 19115-0 schema to ISO 19115-2.

### ISO 19115 - Automatic transfer option / format IDs

ID attributes are automatically added to `gmd:MD_Format` and `gmd:MD_DigitalTransferOptions` elements in order to
reconstruct related formats and transfer options (see the
[Linking transfer options and formats](#iso-19115-linkages-between-transfer-options-and-formats) section for more
information).

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
<gmd:MD_Format id="bml-16b7b5df78a664b15d69feda7ccc7caed501f341-fmt" />
```

And for the `gmd:MD_DigitalTransferOptions` element:

```xml
<gmd:MD_DigitalTransferOptions id="bml-16b7b5df78a664b15d69feda7ccc7caed501f341-tfo" />
```

The `bml-` prefix is added to ensure all IDs begin with a letter (as required by XML), and to allow IDs generated by
this library to be detected. The `-fmt`/`-tfo` prefixes are used to allow the same ID value to uniquely identify two
elements uniquely.

## Setup

See [setup](DEVELOPING.md#setup) documentation.

## Developing

See [Developing](DEVELOPING.md) documentation.

## Releases

- [latest release 🛡️](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/releases/permalink/latest)
- [all releases 🛡️](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/releases)
- [PyPi](https://pypi.org/project/bas-metadata-library/)

## Project maintainer

British Antarctic Survey ([BAS](https://www.bas.ac.uk)) Mapping and Geographic Information Centre
([MAGIC](https://www.bas.ac.uk/teams/magic)). Contact [magic@bas.ac.uk](mailto:magic@bas.ac.uk).

The project lead is [@felnne](https://www.bas.ac.uk/profile/felnne).

## License

Copyright (c) 2019-2024 UK Research and Innovation (UKRI), British Antarctic Survey (BAS).

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
