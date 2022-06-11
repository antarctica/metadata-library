# BAS Metadata Library

Python library for generating metadata and data records.

## Overview

### Purpose

This library is designed to assist in generating metadata and data records, primarily for the discovery of datasets,
services, features and related resources. This project is intended to be used as a dependency, to avoid the need to
duplicate the implementation of complex and verbose metadata and data standards.

At a high level, this library allows a configuration object, representing the fields/structure of a standard, to be
encoded into its formal representation set out by that standard (typically using XML). It also allows such a formal
representation to be decoded back into a configuration object, which can be more easily used or manipulated.

### Supported standards

| Standard                                                        | Implementation                                                  | Library Namespace                                   | Introduced In                                                                                      |
| --------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| [ISO 19115:2003](https://www.iso.org/standard/26020.html)       | [ISO 19139:2007](https://www.iso.org/standard/32557.html)       | `bas_metadata_library.standards.iso_19115_1_v1`     | [#46](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/issues/46)   |
| [ISO 19115-2:2009](https://www.iso.org/standard/39229.html)     | [ISO 19139-2:2012](https://www.iso.org/standard/57104.html)     | `bas_metadata_library.standards.iso_19115_2_v1`     | [#50](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/issues/50)   |
| [IEC 61174:2015](https://webstore.iec.ch/publication/23128)     | [IEC 61174:2015](https://webstore.iec.ch/publication/23128)     | `bas_metadata_library.standards.iec_pas_61174_0_v1` | [#139](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/issues/139) |
| [IEC PAS 61174:2021](https://webstore.iec.ch/publication/67774) | [IEC PAS 61174:2021](https://webstore.iec.ch/publication/67774) | `bas_metadata_library.standards.iec_pas_61174_1_v1` | [#139](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/issues/144) |

**Note:** In this library, the *ISO 19115:2003* standard is referred to as *ISO-19115-1* (`iso_19115_1`) for
consistency with *ISO 19115-2:2009* (referred to as *ISO-19115-2*, `iso_19115_2`). In the future, the
[ISO 19115-1:2014](https://www.iso.org/standard/53798.html) standard will be referred to as *ISO-19115-3*.

### Supported profiles

| Standard | Profile  | Implementation  | Library Namespace | Introduced In |
| -------- | -------- | --------------- | ----------------- | ------------- |
| -        | -        | -               | -                 | -             |

**Note:** Support for profiles has been removed to allow underlying standards to be implemented more easily, and to
wait until a stable profile for UK PDC Discovery metadata has been developed and approved.

### Supported configuration versions

| Standard           | Profile | Configuration Version                                                                                                     | Status  | Notes            |
| ------------------ | ------- |---------------------------------------------------------------------------------------------------------------------------|---------|------------------|
| ISO 19115:2003     | -       | [`v1`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-1-v1.json)     | Retired | Replaced by `v2` |
| ISO 19115:2003     | -       | [`v2`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-1-v2.json)     | Live    | Stable version   |
| ISO 19115:2003     | -       | [`v3`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v3/iso-19115-1-v2.json)     | Alpha   | Experimental     |
| ISO 19115-2:2009   | -       | [`v1`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v1.json)     | Retired | Replaced by `v2` |
| ISO 19115-2:2009   | -       | [`v2`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v2.json)     | Live    | Stable version   |
| ISO 19115-2:2009   | -       | [`v3`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v3.json)     | Alpha   | Experimental     |
| IEC 61174:2015     | -       | [`v1`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iec-pas-61174-0-v1.json) | Alpha   | Experimental     |
| IEC PAS 61174:2021 | -       | [`v1`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iec-pas-61174-1-v1.json) | Alpha   | Experimental     |

### Supported standards coverage

This library is built around the needs of the British Antarctic Survey and the NERC (UK) Polar Data Centre. This means
only standards, and elements of these standards, used by BAS or the UK PDC are supported. However, additions that would
enable this library to be useful to other organisations and use-case are welcome as contributions providing they do not
add significant complexity or maintenance.

| Standard           | Coverage | Coverage Summary                                                                                     |
| ------------------ | -------- |------------------------------------------------------------------------------------------------------|
| ISO 19115:2003     | Good     | All mandatory elements are supported with a good number of commonly used additional elements         |
| ISO 19115-2:2009   | Minimal  | No elements from this extension are supported, with the exception of the root element                |
| IEC 61174:2015     | Minimal  | All mandatory elements are supported, plus a limited number of optional route information attributes |
| IEC PAS 61174:2021 | Minimal  | All mandatory elements are supported, plus a limited number of optional route information attributes |

**Note:** ISO 19115 extensions (i.e. `gmd:metadataExtensionInfo` elements) are not supported.

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

This package depends on native libraries for XML encoding and decoding:

* `libxml2`
* `libxslt`

This package depends on native binaries for XML validation:

* `xmllint`

Most Operating Systems include these libraries and packages by default. However, others, particularly minimal OSes
require these packages to be installed separately. Required packages for supported Operating Systems are:

| Operating System      | Required Packages              | Notes                |
|-----------------------|--------------------------------|----------------------|
| Alpine Linux (Docker) | `libxslt-dev`, `libxml2-utils` | -                    |
| CentOS 7              | -                              | Installed by default |
| CentOS 7 (Docker)     | -                              | Installed by default |

## Usage

### Encode an ISO 19115 metadata record

To generate an ISO 19115 metadata record from a Python record configuration and return it as an XML document:

```python
from datetime import date

from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV3, MetadataRecord

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
configuration = MetadataRecordConfigV3(**minimal_record_config)
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

### Upgrade a version 2 ISO 19115 metadata record configuration to version 3

The version 3 record configuration object includes an upgrade method. This method accepts a version 2 record and returns
a version 3 object. This method will change the record configuration structure to account for changes introduced in the 
version configuration schema.

```python
from datetime import date

from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV2, MetadataRecordConfigV3

minimal_record_config_v2 = {
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
configuration_v2 = MetadataRecordConfigV2(**minimal_record_config_v2)
configuration_v3 = MetadataRecordConfigV3()
configuration_v3.upgrade_from_v2_config(v2_config=configuration_v2)
```

### Downgrade a version 3 ISO 19115 metadata record configuration to version 2

The version 3 record configuration object includes a downgrade method. This method accepts returns a version 2 
equivalent of the record configuration.

**Note**: This will result in data loss, in that the V3 configuration allows information that the V2 configuration 
does not. This additional information will be lost when downgrading to V2, even if the resulting V2 configuration is 
upgraded to V3 again. 

Information that will be lost when downgrading:

* any resource constraints with a `permissions` property - the entire constraint will be lost

```python
from datetime import date

from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV3

minimal_record_config_v3 = {
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
configuration_v3 = MetadataRecordConfigV3(**minimal_record_config_v3)
configuration_v2 = configuration_v3.downgrade_to_v2_config()
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

from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV3

input_path = str('/path/to/file.json')

configuration = MetadataRecordConfigV3()
configuration.load(file=Path(input_path))
```

### Dumping a record configuration to JSON

**The example below is for the ISO 19115 standard but this applies to all standards.**

The `dump()` and `dumps()` methods on the configuration class can be used to dump a record configuration to a JSON
encoded file or string respectively:

```python
from datetime import date
from pathlib import Path

from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV3

output_path = str('/path/to/file.json')

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
configuration = MetadataRecordConfigV3(**minimal_record_config)
configuration.dump(file=Path(output_path))
```

### Validating a record

**The example below is for the ISO 19115 standard but this applies to all standards.**

The formal encoding of a record can be validated against one or more XML schemas relevant to each metadata or data
standard. Records are not validated automatically, and so must be validated explicitly:

```python
from datetime import date

from bas_metadata_library import RecordValidationError
from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV3, MetadataRecord

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
configuration = MetadataRecordConfigV3(**minimal_record_config)
record = MetadataRecord(configuration=configuration)

try:
    record.validate()
except RecordValidationError as e:
    print('Record invalid')
    print(e)
```

Where the contents of the record is invalid, a `RecordValidationError` exception will be raised. Printing this
exception will return validation errors.

These errors should not happen, and if they do are considered internal bugs. Please report any in the
[Project Issue Tracker](#issue-tracking) if you are internal to BAS, or as [Feedback](#feedback) if you are not.

See the [Record Schemas](#record-schemas) section for more information on how validation works.

### Validating a record configuration

**The example below is for the ISO 19115 standard but this applies to all standards.**

Record configurations will be validated automatically using a JSON Schema relevant to each metadata or data standard.

To explicitly validate a record configuration:

```python
from datetime import date

from jsonschema import ValidationError
from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV3

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
configuration = MetadataRecordConfigV3(**minimal_record_config)

try:
    configuration.validate()
except ValidationError as e:
    print('Record configuration invalid')
    print(e)
```

Where the contents of the record is invalid, a
[`ValidationError`](https://python-jsonschema.readthedocs.io/en/stable/errors/#jsonschema.exceptions.ValidationError)
exception will be raised by the underlying JSON Schema library. Printing this exception will return validation errors.

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
| ---------- | ------ | ---------------------------- |
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

Allowed elements, attributes and values for each [supported Standard](#supported-standards) and
[Supported Profile](#supported-profiles) are defined using one or more [XML Schemas](https://www.w3.org/XML/Schema).
These schemas define any required entities, and any entities with enumerated values. Schemas are usually published by
standards organisations to facilitate record validation.

For performance reasons, and to ensure required schemas are not unavailable (due to remote locations being reorganised,
or during server maintenance etc.), these schema files are stored within this package. Schemas are stored as XML Schema
Definition (XSD) files in the `bas_metadata_library.schemas.xsd` module, and loaded as resource files for use in record
validation.

**Note:** To support local validation, imported or included schema locations in local versions of XML schemas, have
been modified. These changes do not materially change the contents of any schema.

**Note:** In some cases, material changes *have* been made to local versions of schemas, in order to workaround
specific issues. These changes will be documented and explained, to allow users to understand the effect they will
have, and why they have been made.

#### Altered Metadata Schema - Geographic Metadata (GMD)

The ISO *Geographic Metadata (GMD)* schema (used directly for the ISO 19115-0 standard, and indirectly in the ISO
19115-2 standard) has been modified to:

1. include the ISO *Geographic Metadata XML (GMX)* schema:
    * in order to allow Anchor elements to substitute primitive/simple values (such as character strings and integers),
    * as defined in the ISO 19139:2007 and ISO 19139:2012 standards

### Configuration classes

The configuration of each metadata record is held in a Python dictionary, within a `MetadataRecordConfig` class. This
class includes methods to validate its configuration against a relevant [Configuration Schema](#configuration-schemas).

Configuration classes are defined at the root of each standard or profile, alongside its root
[Metadata Element](#record-element-classes) and XML namespaces.

A configuration class will exist for each supported configuration schema with methods to convert from one version to
another.

### Configuration schemas

Allowed properties and values for record configurations for each [supported Standard](#supported-standards) and
[Supported Profile](#supported-profiles) are defined using a [JSON Schema](https://json-schema.org). These schemas
define any required properties, and any properties with enumerated values.

Configuration schemas are stored as JSON files in the `bas_metadata_library.schemas` module, and loaded as
resource files from within this package to validate record configurations. Schemas are also made available externally
through the BAS Metadata Standards website,
[metadata-standards.data.bas.ac.uk](https://metadata-standards.data.bas.ac.uk), to allow:

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
`bas_metadata_library.schemas.src` module, then [generate distribution schemas](#generating-configuration-schemas).

JSON Schema's can be developed using [jsonschemavalidator.net](https://www.jsonschemavalidator.net).

### Adding a new standard

To add a new standard:

1. create a new module under `bas_metadata_library.standards`, e.g. `bas_metadata_library.standards.foo_v1/__init__.py`
2. in this module, overload the `Namespaces`, `MetadataRecordConfig` and `MetadataRecord` classes as needed
    * version the `MetadataRecordConfig` class, e.g. `MetadataRecordConfigV1` 
3. create a suitable metadata configuration JSON schema in `bas_metadata_library.schemas.src`, 
   e.g. `bas_metadata_library.schemas.src.foo_v1.json`
4. update the `generate_schemas` method in `app.py` to generate distribution schemas
5. add a script line to the `publish-schemas-stage` and `publish-schemas-prod` jobs in `.gitlab-ci.yml`, to publish
   the distribution schema within the BAS Metadata Standards website
6. define a series of test configurations (e.g. minimal, typical and complete) for generating test records in
   `tests/resources/configs/` e.g. `tests/resources/configs/foo_v1_standard.py`
7. add a route in `app.py` for generating test records for the new standard
8. update the `capture_test_records` method in `app.py` to generate and save test records
9. add relevant [tests](#testing) with methods to test each metadata element class and test records

### Adding a new element to an existing standard

**Note:** These instructions are specific to the ISO 19115 metadata standards family.

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
4. add relevant [element class](#record-element-classes):
   * new or changed elements should be added to the configuration for the relevant package for each standard
   * for the ISO 19115 family of standards, element classes should be added to the `iso_19115_common` package
   * the exact module to use within this package will depend on the nature of the element being added, but in general,
     elements should be added to the module of their parent element (e.g. `data_identification.py` for elements
     under the `identification` record configuration property), elements used across a range of elements should be
     added to the `common_elements.py` module
   * remember to include references to new element class in the parent element class (in both the `make_element` and
     `make_config` methods)
5. [capture test records](#capturing-test-records)
    * initially this acts as a good way to check new or changed element classes encode configuration properties
      correctly
    * check the git status of these test records to check existing records have changed how you expect (and haven't
      changed things you didn't intend to for example)
6. [capture test JSON configurations](#capturing-test-configurations-as-json)
    * check the git status of these test configs to check they are encoded correctly from Python (i.e. dates)
7. add tests:
    * new test cases should be added, or existing test cases updated, in the relevant module within
      `tests/bas_metadata_library/`
    * for the ISO 19115 family of standards, this should be `test_standard_iso_19115_1.py`, unless the element is only
      part of the ISO 19115-2 standard
    * providing there are enough test configurations to test all the ways a new element can be used (e.g. with a simple
      text string or anchor element for example), adding a test case for each element is typically enough to ensure
      sufficient test coverage
    * where this isn't the case, it's suggested to add one or more 'edge case' test cases to test remaining code paths
      explicitly
8. check [test coverage](#test-coverage):
    * for missing coverage, consider adding edge case test cases where applicable
    * coverage exemptions should be avoided wherever feasible and all exemptions must be discussed before they are added
    * where exceptions are added, they should be documented as an issue with information on how they will be addressed
      in the longer term
9. update `README.md` examples if common element:
    * this is probably best done before releasing a new version
10. update `CHANGELOG.md`
11. if needed, add name to `authors` property in `pyproject.toml`

### Adding a new config version for an existing standard [WIP]

**Note:** This is typically only needed if breaking changes need to be made to the schema for a configuration, as the 
work involved is quite involved.

**Note:** This section is a work in progress whilst developing the ISO 19115 v3 configuration in
[#182](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/182).

**Note:** In these instructions, `v1` refers to the current/previous configuration version. `v2` refers to the new 
configuration version.

First create a new configuration version that is identical to the current/previous version, but that sets up the 
schema, objects, methods, tests and documentation needed for the new configuration, and to convert between the old 
and new configurations.

1. create an issue summarising, and referencing specific issues for, changes to be made in the new schema version
2. copy the current/previous metadata configuration JSON schema from `bas_metadata_library.schemas.src`
   e.g. `bas_metadata_library.schemas.src.foo_v1.json` to `bas_metadata_library.schemas.src.foo_v2.json`
   1. change the version in:
       * the `$id` property
       * the `title` property
       * the `description` property
3. duplicate the configuration classes for the standard in `bas_metadata_library.standards`
    * i.e. in `bas_metadata_library.standards.foo_v1/__init__.py`, copy:
        * `MetadataRecordConfigV1` to `MetadataRecordConfigV2`
4. in the new configuration class, add `upgrade_to_v1_config()` and `downgrade_to_v2_config()` methods
    * the `upgrade_from_v2_config()` method should accept a current/previous configuration class
    * the `downgrade_to_v1_config()` method should return a current/previous configuration class
5. change the signature of the `MetadataRecord` class to use the new configuration class
6. change the `make_config()` method of the `MetadataRecord` class to return the new configuration class
7. update the `generate_schemas()` method in `app.py` to generate distribution schemas for the new schema version
8. [Generate configuration schemas](#generating-configuration-schemas)
9. add a script line to the `publish-schemas-stage` and `publish-schemas-prod` jobs in `.gitlab-ci.yml`, to publish
   the distribution schema for the new schema version within the BAS Metadata Standards website
10. define a series of test configurations (e.g. minimal, typical and complete) for generating test records in
    `tests/resources/configs/` e.g. `tests/resources/configs/foo_v1_standard.py`
     * note that the version in these file names is for the version of the standard, not the configuration
     * new config objects will be made within this file that relate to the new configuration version
     * initially these new config objects can inherit from test configurations for the current/previous version
11. update the `generate_json_test_configs()` method in `app.py` to generate JSON versions of each test configuration
12. [Capture test JSON record configurations](#capturing-test-configurations-as-json)
13. update the route for the standard in `app.py` (e.g. `standard_foo_v1`) to:
     1. upgrade configs for the old/current version of the standard (as the old/current MetadataRecordConfig class will 
        now be incompatible with the updated MetadataRecord class)  
     2. include configs for the new config version of the standard
14. update the `capture_test_records()` method in `app.py` to capture test records for the new test configurations
15. [Capture test XML records](#capturing-test-records)
16. add test cases for the new `MetadataRecordConfig` class in the relevant module in `tests.bas_metadata_library`:
    * `test_invalid_configuration_v2`
    * `test_configuration_v2_from_json_file`
    * `test_configuration_v2_from_json_string`
    * `test_configuration_v2_to_json_file`
    * `test_configuration_v2_to_json_string`
    * `test_configuration_v2_json_round_trip`
    * `test_parse_existing_record_v2`
    * `test_lossless_conversion_v2`
17. change all test cases to target record configurations for the new version
18. update the `test_record_schema_validation_valid` and `test_record_schema_validation_valid` test cases, which test 
    the XML/XSD schema for the standard, not the configuration JSON schema
19. update the existing `test_lossless_conversion_v1` test case to upgrade v1 configurations to v2, as the 
    `MetadataRecord` class will no longer be compatible with the `MetadataRecordConfigV1` class
20. update the [Supported configuration versions](#supported-configuration-versions) section of the README 
     * add the new schema version, with a status of 'alpha'
21. update the encode/decode subsections in the [Usage](#usage) section of the README to use the new RecordConfig class
22. if the lead standard (ISO 19115) is being updated also update these [Usage](#usage) subsections:
    * [Loading a record configuration from JSON](#loading-a-record-configuration-from-json)
    * [Dumping a record configuration to JSON](#dumping-a-record-configuration-to-json)
    * [Validating a record](#validating-a-record)
    * [Validating a record configuration](#validating-a-record-configuration)
23. add a subsection to the [Usage](#usage) section of the README explaining how to upgrade and downgrade a 
    configuration between the old and new versions
24. Update the change log to reference the creation of the new schema version, referencing the summary issue

Second, iteratively introduce changes to the new configuration, adding logic to convert between the old and new 
configurations as needed. This logic will likely be messy and may target specific known use-cases. This is acceptable on 
the basis these methods will be relatively short lived.

1. as changes are made, add notes and caveats to the upgrade/downgrade methods in code, and summarise any 
   significant points in the [Usage](#usage) instructions as needed (e.g. that the process is lossy)

### ISO 19115 - Automatic transfer option / format IDs

ID attributes are automatically added to `gmd:MD_Format` and `gmd:MD_DigitalTransferOptions` elements in order to
reconstruct related formats and transfer options (see the
[Linking transfer options and formats](#ISO-19115-linkages-between-transfer-options-and-formats) section for more 
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
<gmd:MD_Format id="bml-16b7b5df78a664b15d69feda7ccc7caed501f341-fmt">
```

And for the `gmd:MD_DigitalTransferOptions` element:

```xml
<gmd:MD_DigitalTransferOptions id="bml-16b7b5df78a664b15d69feda7ccc7caed501f341-tfo">
```

The `bml-` prefix is added to ensure all IDs begin with a letter (as required by XML), and to allow IDs generated by
this library to be detected. The `-fmt`/`-tfo` prefixes are used to allow the same ID value to uniquely identify two
elements uniquely.

## Setup

### Terraform

Terraform is used to provision resources required to operate this application in staging and production environments.

These resources allow [Configuration schemas](#configuration-schemas) for each standard to be accessed externally.

Access to the [BAS AWS account](https://gitlab.data.bas.ac.uk/WSF/bas-aws) is needed to provision these resources.

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

Git and [Poetry](https://python-poetry.org) are required to set up a local development environment of this application.

**Note:** If you use [Pyenv](https://github.com/pyenv/pyenv), this project sets a local Python version for consistency.

If you have access to the [BAS GitLab instance](https://gitlab.data.bas.ac.uk):

```shell
# clone from the BAS GitLab instance if possible
$ git clone https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library.git

# alternatively, clone from the GitHub mirror
$ git clone https://github.com/antarctica/metadata-library.git

# setup virtual environment
$ cd metadata-library
$ poetry install
```

### Code Style

PEP-8 style and formatting guidelines must be used for this project, except the 80 character line limit.
[Black](https://github.com/psf/black) is used for formatting, configured in `pyproject.toml` and enforced as part of
[Python code linting](#code-linting-python).

Black can be integrated with a range of editors, such as 
[PyCharm](https://black.readthedocs.io/en/stable/integrations/editors.html#pycharm-intellij-idea), to apply formatting 
automatically when saving files.

To apply formatting manually:

```shell
$ poetry run black src/ tests/
```

### Code Linting (Python)

[Flake8](https://flake8.pycqa.org) and various extensions are used to lint Python files in the `bas_metadata_library` 
module. Specific checks, and any configuration options, are documented in the `./.flake8` config file.

To check files manually:

```shell
$ poetry run flake8 src/
```

Checks are run automatically in [Continuous Integration](#continuous-integration).

### Code Linting (JSON)

JSON files (specifically JSON Schemas used for [Record Configurations](#configuration-schemas)) must be valid JSON 
documents. Minimal linting is used to enforce this as part of [Continuous Integration](#continuous-integration).

To check files manually:

```shell
$ for file in $(find ./src/bas_metadata_library/schemas/src -name "*.json"); do echo ${file}; poetry run python -m json.tool < ${file} 1>/dev/null; done
```

### Dependencies

Python dependencies for this project are managed with [Poetry](https://python-poetry.org) in `pyproject.toml`.

Non-code files, such as static files, can also be included in the [Python package](#python-package) using the
`include` key in `pyproject.toml`.

#### Adding new dependencies

To add a new (development) dependency:

```shell
$ poetry add [dependency] (--dev)
```

Then update the Docker image used for CI/CD builds and push to the BAS Docker Registry (which is provided by GitLab):

```shell
$ docker build -f gitlab-ci.Dockerfile -t docker-registry.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library:latest .
$ docker push docker-registry.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library:latest
```

#### Updating dependencies

```shell
$ poetry update
```

See the instructions above to update the Docker image used in CI/CD.

#### Dependency vulnerability checks

The [Safety](https://pypi.org/project/safety/) package is used to check dependencies against known vulnerabilities.

**IMPORTANT!** As with all security tools, Safety is an aid for spotting common mistakes, not a guarantee of secure 
code. In particular this is using the free vulnerability database, which is updated less frequently than paid options.

This is a good tool for spotting low-hanging fruit in terms of vulnerabilities. It isn't a substitute for proper 
vetting of dependencies, or a proper audit of potential issues by security professionals. If in any doubt you MUST seek
proper advice.

Checks are run automatically in [Continuous Integration](#continuous-integration).

To check locally:

```shell
$ poetry export --without-hashes -f requirements.txt | poetry run safety check --full-report --stdin
```

#### `jsonschema` package

The `jsonschema` dependency is locked to version 3.2.0 because version 4.0 > dropped Python 3.6 support. This
library cannot require newer Python versions to ensure it can be used in projects that run on BAS IT infrastructure.

#### `lxml` package

The `lxml` dependency takes a long time to install/update inside Alpine container images because it needs to be built 
from source. This is because Alpine Linux, used by the official Python Docker base images, is not supported by the 
Python [manylinux](https://github.com/pypa/manylinux) system, and therefore cannot use pre-built, binary, wheels.

### Static security scanning

To ensure the security of this API, source code is checked against [Bandit](https://github.com/PyCQA/bandit)
and enforced as part of [Python code linting](#code-linting-python).

**Warning:** Bandit is a static analysis tool and can't check for issues that are only be detectable when running the
application. As with all security tools, Bandit is an aid for spotting common mistakes, not a guarantee of secure code.

Checks are run automatically in [Continuous Integration](#continuous-integration).

#### `lxml` package (bandit)

Bandit identifies the use of `lxml` classes and methods as a security issue, specifically:

> Element to parse untrusted XML data is known to be vulnerable to XML attacks

The recommendation is to use a *safe* implementation of an XML processor (`defusedxml`) that can avoid entity bombs and 
other XML processing attacks. However, `defusedxml` does not offer all of the methods we need and there does not appear
to be such another processor that does provide them.

The main vulnerability this security issue relates to is processing user input that can't be trusted. This isn't really
applicable to this library directly, but rather to where it's used in implementing projects. I.e. if this library is 
used in a service that accepts user input, an assessment must be made whether the input needs to be sanitised.

Within this library itself, the only input that is processed is test records, all of which are assumed to be safe to 
process.

### Generating configuration schemas

To generate [distribution schemas from source schemas](#source-and-distribution-schemas), a custom Flask CLI command,
`generate-schemas` is available. The [`jsonref`](https://jsonref.readthedocs.io/en/latest/) library is used to resolve
any references in source schemas and write the output as distribution schemas, replacing any existing output.

```shell
$ poetry run flask generate-schemas
```

To configure this command, (e.g. to add a new schema for a new standard/profile), adjust the `schemas` list in the
`generate_schemas` method in `app.py`. This list should contain dictionaries with keys for the common name of the
schema (based on the common file name of the schema JSON file), and whether the source schema should be resolved or
simply copied. This should be true by default, and is only relevant to schemas that do not contain any references, as
this will cause an error if resolved.

## Testing

All code in the `bas_metadata_library` module must be covered by tests, defined in `tests/`. This project uses
[PyTest](https://docs.pytest.org/en/latest/) which should be run in a random order using
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
$ poetry run pytest --random-order
```

To run tests manually using PyCharm, use the included *App (Tests)* run/debug configuration.

Tests are run automatically in [Continuous Integration](#continuous-integration).

### Capturing test records

To capture test records, which verify complete records are assembled correctly, a custom Flask CLI command,
`capture-test-records` is available. This command will update pre-existing records in `tests/resources/records`, with 
differences captured in version control to aid in manual review to ensure changes are expected/correct.

```shell
$ poetry run flask capture-test-records
```

### Capturing test configurations as JSON

To capture test configurations as JSON, which verify the dump/load methods of configuration classes work encode and 
decode information correctly, a custom Flask CLI command, `capture-json-test-configs` is available. This will dump all 
test configurations for each standard to set of JSON files in `tests/resources/configs/`. 

```shell
$ poetry run flask capture-json-test-configs
```

These files MUST then be manually verified to ensure they have encoded each configuration correctly. Once they have, 
they can be used in tests to automatically verify this remains the case.

It is intended that this command will update pre-existing configurations, with differences captured in version control
to aid in manual review to ensure they are correct.

### Test coverage

[pytest-cov](https://pypi.org/project/pytest-cov/) is used to measure test coverage.

To measure coverage manually:

```shell
$ poetry run pytest --random-order --cov=bas_metadata_library --cov-fail-under=100 --cov-report=html .
```

[Continuous Integration](#continuous-integration) will check coverage automatically and fail if less than 100%.

### Continuous Integration

All commits will trigger a Continuous Integration process using GitLab's CI/CD platform, configured in `.gitlab-ci.yml`.

## Deployment

### Python package

This project is distributed as a Python package, hosted in [PyPi](https://pypi.org/project/bas-metadata-library).

Source and binary packages are built and published automatically using
[Poetry](https://python-poetry.org) in [Continuous Deployment](#continuous-deployment).

**Note:** Except for tagged releases, Python packages built in CD will use `0.0.0` as a version to indicate they are 
not formal releases.

### Continuous Deployment

A Continuous Deployment process using GitLab's CI/CD platform is configured in `.gitlab-ci.yml`.

## Release procedure

For all releases, create a release issue by creating a new [issue](#issue-tracking), with the 'release' issue template,
and follow its instructions.

## Feedback

The maintainer of this project is the BAS Web & Applications Team, they can be contacted at:
[servicedesk@bas.ac.uk](mailto:servicedesk@bas.ac.uk).

## Issue tracking

This project uses issue tracking, see the
[Issue tracker](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/issues) for more
information.

**Note:** Read & write access to this issue tracker is restricted. Contact the project maintainer to request access.

## License

Copyright (c) 2019-2022 UK Research and Innovation (UKRI), British Antarctic Survey.

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
