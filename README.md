# BAS Metadata Library

Python library for generating metadata records.

## Overview

The BAS Metadata Library is an underpinning library for other tools and applications to generate discovery level
metadata records (describing products, services and other resources). It is intended to avoid duplicating complex and
verbose encode/decoding logic across projects.

It supports a lossless, two-way, conversion between a [Configuration Object](#configuration-classes) (a python dict
representing the fields/structure of a record for a standard) into its formal representation (typically an XML document)
to support processing and manipulation of information between and within systems.

The library also supports validating record configurations (via JSON Schemas) and formal representations (typically via
XML XSDs).

> [!NOTE]
> This project is focused on needs within the British Antarctic Survey. It has been open-sourced in case parts are of
> interest to others. Some resources, indicated with a '🛡' or '🔒' symbol, can only be accessed by BAS staff or
> project members respectively. Contact the [Project Maintainer](#project-maintainer) to request access.

### Supported standards

<!-- pyml disable md013 -->
| Standard                                                        | Implementation                                                  | Status    | Library Namespace                               | Introduced In                                                                                        | Retired In                                                                                           |
|-----------------------------------------------------------------|-----------------------------------------------------------------|-----------|-------------------------------------------------|------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|
| [ISO 19115:2003](https://www.iso.org/standard/26020.html)       | [ISO 19139:2007](https://www.iso.org/standard/32557.html)       | Supported | `bas_metadata_library.standards.iso_19115_0_v1` | [#46 🛡️](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/issues/46)   | -                                                                                                    |
| [ISO 19115-2:2009](https://www.iso.org/standard/39229.html)     | [ISO 19139-2:2012](https://www.iso.org/standard/57104.html)     | Supported | `bas_metadata_library.standards.iso_19115_2_v1` | [#50 🛡️](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/issues/50)   | -                                                                                                    |
| [IEC 61174:2015](https://webstore.iec.ch/publication/23128)     | [IEC 61174:2015](https://webstore.iec.ch/publication/23128)     | Retired   | -                                               | [#139 🛡️](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/issues/139) | [#266 🛡️](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/issues/266) |
| [IEC PAS 61174:2021](https://webstore.iec.ch/publication/67774) | [IEC PAS 61174:2021](https://webstore.iec.ch/publication/67774) | Retired   | -                                               | [#139 🛡️](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/issues/144) | [#266 🛡️](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/issues/266) |                                                                                                     |
<!-- pyml enable md013 -->

> [!NOTE]
> From v0.11.0 of this library, the *ISO 19115:2003* standard revision is referred to as *ISO-19115-0* (`iso_19115_0`).
> Prior to this version, it was (incorrectly) referred to as *ISO-19115-1* (`iso_19115_1`).
>
> To avoid confusion, when the [ISO 19115-1:2014](https://www.iso.org/standard/53798.html) standard is implemented, it
> will be referred to as *ISO-19115-3* (`iso_19115_3`).

### Supported profiles

<!-- pyml disable md013 -->
| Standard  | Profile                                                                                               | Introduced In                                                                                    |
|-----------|-------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| ISO 19115 | [MAGIC Discovery Metadata V1](https://metadata-resources.data.bas.ac.uk/profiles/magic-discovery-v1/) | [#250](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/issues/250) |
| ISO 19115 | [MAGIC Discovery Metadata V2](https://metadata-resources.data.bas.ac.uk/profiles/magic-discovery/v2/) | [#250](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/issues/268) |
<!-- pyml enable md013 -->

### Supported configuration versions

<!-- pyml disable md013 -->
| IEC 61174:2015     | -       | [`v1`](https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iec-pas-61174-0-v1.json) | Retired | No longer supported                   |
| IEC PAS 61174:2021 | -       | [`v1`](https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iec-pas-61174-1-v1.json) | Retired | No longer supported                   |
| Standard           | Profile                     | Configuration Version                                                                                                     | Status       | Notes                                 |
|--------------------|-----------------------------|---------------------------------------------------------------------------------------------------------------------------|--------------|---------------------------------------|
| ISO 19115:2003     | -                           | [`v1`](https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-1-v1.json)     | Retired      | Replaced by `v2`, no longer supported |
| ISO 19115:2003     | -                           | [`v2`](https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-1-v2.json)     | Retired      | Replaced by `v3`, no longer supported |
| ISO 19115:2003     | -                           | [`v3`](https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-1-v3.json)     | Retired      | Replaced by `v4`, no longer supported |
| ISO 19115:2003     | -                           | [`v4`](https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-0-v4.json)     | Stable       | Currently supported version           |
| ISO 19115-2:2009   | -                           | [`v1`](https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v1.json)     | Retired      | Replaced by `v2`, no longer supported |
| ISO 19115-2:2009   | -                           | [`v2`](https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v2.json)     | Retired      | Replaced by `v3`, no longer supported |
| ISO 19115-2:2009   | -                           | [`v3`](https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v3.json)     | Retired      | Replaced by `v4`, no longer supported |
| ISO 19115-2:2009   | -                           | [`v4`](https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v4.json)     | Stable       | Currently supported version           |
| ISO 19115-2:2009   | MAGIC Discovery Metadata V2 | [`v1`](https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/magic-discovery-v2.json) | Experimental | Next supported version                |
<!-- pyml enable md013 -->

### Supported standards coverage

This library is limited to the standards, and subset of elements within these standards, needed for tools and use-cases
within the British Antarctic Survey (BAS) and the NERC Polar Data Centre (UK PDC).

> [!TIP]
> Additions enabling this library to support other use-cases are welcome as contributions, providing they do not add
> significant complexity or maintenance.

<!-- pyml disable md013 -->
| Standard           | Coverage | Coverage Summary                                                                                     |
|--------------------|----------|------------------------------------------------------------------------------------------------------|
| ISO 19115:2003     | Good     | All mandatory elements are supported with a good number of commonly used additional elements         |
| ISO 19115-2:2009   | Minimal  | No elements from this extension are supported, with the exception of the root element                |
<!-- pyml enable md013 -->

> [!NOTE]
> ISO 19115 extensions (i.e. `gmd:metadataExtensionInfo` elements) are not supported.

## Installation

This package can be installed using Pip from [PyPi](https://pypi.org/project/bas-metadata-library):

```text
$ pip install bas-metadata-library
```

This package depends on these OS level libraries for XML encoding and decoding:

- `libxml2`
- `libxslt`

This package depends on these OS level binaries for XML validation:

- `xmllint`

These libraries may already be installed, or require additional OS packages:

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

# define a minimalish record configuration
minimalish_config = {
    "$schema": "https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-1-v4.json",
    "hierarchy_level": "dataset",
    "metadata": {
        "contacts": [{"organisation": {"name": "UK Polar Data Centre"}, "role": ["pointOfContact"]}],
        "date_stamp": date(2018, 10, 18),
    },
    "identification": {
        "title": {"value": "Test Record"},
        "dates": {"creation": {"date": date(2018, 1, 1), "date_precision": "year"}},
        "abstract": "Test Record for ISO 19115 metadata standard (no profile) with required properties only.",
        "character_set": "utf8",
        "language": "eng",
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

# encode configuration into a formal document
config = MetadataRecordConfigV4(**minimal_config)
record = MetadataRecord(configuration=config)
document = record.generate_xml_document()

# output document
print(document.decode())
```

> [!TIP]
> See [HTML Entities](#html-entities) for guidance on using accents and symbols in configurations.
>
> See [Date Precision](#date-precision) for guidance on using partial (year or year-month) dates.

### Decode an ISO 19115 metadata record

```python
from bas_metadata_library.standards.iso_19115_2 import MetadataRecord

# load a formal document
with open(f"record.xml") as document_file:
    document = document_file.read()

# decode formal document into an informal Python config
record = MetadataRecord(record=document)
configuration = record.make_config()
config = configuration.config

# output config
print(config)
```

### Loading a record configuration from JSON

The `load()` and `loads()` methods on the relevant configuration class can load a record configuration encoded as a
JSON file or JSON string respectively:

```python
from pathlib import Path

from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV4

input_path = str('/path/to/file.json')

configuration = MetadataRecordConfigV4()
configuration.load(file=Path(input_path))
```

### Dumping a record configuration to JSON

The `dump()` and `dumps()` methods on the relevant configuration class can dump a record configuration to a JSON
encoded file or string respectively:

```python
from datetime import date
from pathlib import Path

from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV4

output_path = str('/path/to/file.json')

minimalish_config = {
    "$schema": "https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-1-v4.json",
    "hierarchy_level": "dataset",
    "metadata": {
        "contacts": [{"organisation": {"name": "UK Polar Data Centre"}, "role": ["pointOfContact"]}],
        "date_stamp": date(2018, 10, 18),
    },
    "identification": {
        "title": {"value": "Test Record"},
        "dates": {"creation": {"date": date(2018, 1, 1), "date_precision": "year"}},
        "abstract": "Test Record for ISO 19115 metadata standard (no profile) with required properties only.",
        "character_set": "utf8",
        "language": "eng",
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
configuration = MetadataRecordConfigV4(**minimalish_config)
configuration.dump(file=Path(output_path))
```

### Validating a record

The formal encoding of a record can be validated against one or more XML schemas relevant to each metadata or data
standard. Records are not validated automatically, and so must be validated explicitly:

```python
from datetime import date

from bas_metadata_library import RecordValidationError
from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV4, MetadataRecord

minimalish_config = {
    "$schema": "https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-1-v4.json",
    "hierarchy_level": "dataset",
    "metadata": {
        "contacts": [{"organisation": {"name": "UK Polar Data Centre"}, "role": ["pointOfContact"]}],
        "date_stamp": date(2018, 10, 18),
    },
    "identification": {
        "title": {"value": "Test Record"},
        "dates": {"creation": {"date": date(2018, 1, 1), "date_precision": "year"}},
        "abstract": "Test Record for ISO 19115 metadata standard (no profile) with required properties only.",
        "character_set": "utf8",
        "language": "eng",
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
configuration = MetadataRecordConfigV4(**minimalish_config)
record = MetadataRecord(configuration=configuration)

try:
    record.validate()
    print('Record valid')
except RecordValidationError as e:
    print('Record invalid')
    print(e)
```

Invalid records will raise a `RecordValidationError` exception. Printing this exception will return validation errors.

These errors should not happen, and if they do are considered internal bugs and [Reported](#project-maintainer).

See the [Record Schemas](#record-schemas) section for more information on how validation works.

### Validating a record configuration

[Record configurations](#configuration-classes) will be automatically validated using a JSON Schema for the metadata
standard used.

Where a record configuration states compliance with one or more [Supported Profiles](#supported-profiles), it will also
be automatically validated using a JSON Schema for each profile.

To explicitly validate a record configuration:

```python
from datetime import date

from jsonschema import ValidationError
from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV4

minimalish_config = {
    "$schema": "https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-1-v4.json",
    "hierarchy_level": "dataset",
    "metadata": {
        "contacts": [{"organisation": {"name": "UK Polar Data Centre"}, "role": ["pointOfContact"]}],
        "date_stamp": date(2018, 10, 18),
    },
    "identification": {
        "title": {"value": "Test Record"},
        "dates": {"creation": {"date": date(2018, 1, 1), "date_precision": "year"}},
        "abstract": "Test Record for ISO 19115 metadata standard (no profile) with required properties only.",
        "character_set": "utf8",
        "language": "eng",
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
    print('Record configuration valid')
except ValidationError as e:
    print('Record configuration invalid')
    print(e)
```

Invalid records will raise a
[`ValidationError`](https://python-jsonschema.readthedocs.io/en/stable/errors/#jsonschema.exceptions.ValidationError)
exception from the underlying JSON Schema library containing the specific validation error.

> [!NOTE]
> The first validation error encountered will stop further validation.

See the [Record Configuration Schemas](#configuration-schemas) section for more information.

### HTML entities

HTML entities (e.g. `&gt;`) will be double escaped by [Lxml](https://lxml.de) (the XML library used internally) and so
should be avoided. Literal characters (e.g. `>`) should be used instead, which will then be escaped automatically. This
also applies to any Unicode characters, such as accents (e.g. `å`) or symbols (e.g. `µ`).

E.g. If `&gt;`, the HTML entity for `>` (greater than), is used as input, it will be escaped again to the invalid
output `&amp;gt;`.

### Date Precision

Dates and date-times used in Python record configurations MUST be structured as dictionaries with a `date` property,
containing a date or date-time value.

Where this value represents a date with an unknown year or year and month, an additional `date_precision` property MUST
be set with a value of either:

- `year` (month and day are unknown)
- `month` (day is unknown)

Partial dates or date-times will be detected and a `date_precision` property set automatically when decoding records.

Python date and date time objects require values for all elements (even when unknown). Partial/unknown elements SHOULD
use '1' as a workaround value in these cases, which will be ignored when encoded.

When using JSON for [Record configurations](#configuration-classes), date or date times MUST be written as strings,
with partial values expressed naturally (e.g. `2014` or `2012-04`), without the need for wrapping object and
`date_precision` property.

Summary table:

<!-- pyml disable md013 -->
| Date Precision | Python Encoding                                                                | JSON Encoding           | XML Encoding            |
|----------------|--------------------------------------------------------------------------------|-------------------------|-------------------------|
| Year           | `{'date': date(year=2012, month=1, day=1), 'date_precision': 'year'}`          | `"2012"`                | `"2012"`                |
| Month          | `{'date': date(year=2012, month=4, day=1), 'date_precision': 'month'}`         | `"2012-04"`             | `"2012-04"`             |
| Day            | `{'date': date(year=2012, month=4, day=14)}`                                   | `"2012-04-14"`          | `"2012-04-14"`          |
| Hour           | `{'date': datetime(year=2012, month=4, day=14, hour=6)}`                       | `"2012-04-14T06"`       | `"2012-04-14T06"`       |
| Minute         | `{'date': datetime(year=2012, month=4, day=14, hour=6, minute=30)}`            | `"2012-04-14T06:30"`    | `"2012-04-14T06:30"`    |
| Second         | `{'date': datetime(year=2012, month=4, day=14, hour=6, minute=30, second=42)}` | `"2012-04-14T06:30:42"` | `"2012-04-14T06:30:42"` |
<!-- pyml enable md013 -->

> [!NOTE]
> For date times, the UTC timezone is assumed unless set.

### ISO 19115 - linkages between transfer options and formats

In ISO 19115, there is no formal mechanism to associate file distribution formats and transfer options, needed to
produce download tables such as [1].

As this library seeks to be fully reversible between a configuration dict and formal XML encoding, associations between
these elements would be lost when records are encoded as XML. In [Record Configurations](#configuration-classes), these
associations are encoded using a 'distribution option' concept.

Within formal XML records, associations are encoded using `xsd:ID` attributes in `gmd:MD_Format` and
`gmd:DigitalTransferOptions` elements, with values allowing associations to be reconstructed when decoding XML records.

> [!CAUTION]
> Do not modify automatically assigned IDs outside of this library.

See the [Automatic transfer option / format IDs](#iso-19115-automatic-transfer-option-format-ids) section for
implementation details.

[1]

| Format     | Size   | Download Link                |
|------------|--------|------------------------------|
| CSV        | 68 kB  | [Link](https://example.com/) |
| GeoPackage | 1.2 MB | [Link](https://example.com/) |

## Implementation

This library is implemented in Python and consists of a set of classes to generate XML metadata records from a
configuration object (Python dict), or to generate such an object from an XML record.

Each [Supported Standard](#supported-standards) is implemented as a module under `bas_metadata_library.standards`. Each
[Supported Profile](#supported-profiles) is implemented as modules under their respective standard.

### Base classes

For each standard and profile, instances of these base classes are defined:

- `Namespaces`
- `MetadataRecord`
- `MetadataRecordConfig`

The `Namespaces` class is a mapping between XML namespaces, their shorthand aliases and their XML definition XSDs.

The `MetadataRecord` class represents a metadata record and defines the Root [Element](#record-element-classes). These
classes provide methods to generate XML documents or parse a XML document into a `MetadataRecordConfig` class.

The `MetadataRecordConfig` class represents the [Configuration](#configuration-classes) defining the structure and
values for a `MetadataRecord` (either for new records, or derived from existing records). This class provides methods
to validate the configuration and dumping/loading from/to JSON.

### Record element classes

Each supported element, in each [supported standard](#supported-standards), inherit and use the `MetadataRecordElement`
class to:

- encode configuration values into an XML fragment of at least one element
- decode an XML fragment into one or more configuration values

Specifically, at least two methods are implemented:

- `make_element()` which builds an XML element using values from a configuration object
- `make_config()` which uses typically XPath expressions to build a configuration object from XML

These methods may be simple (if encoding or decoding a simple free text value for example), or quite complex, using
sub-elements (which themselves may contain sub-elements as needed).

### Record schemas

Allowed elements, attributes and values for each [supported Standard](#supported-standards), and if applicable,
[Supported Profile](#supported-profiles) are defined using one or more [XML Schemas](https://www.w3.org/XML/Schema).
These schemas define any required entities, and any entities with enumerated values. Schemas are usually published by
standards organisations to facilitate record validation.

For performance, and to ensure required schemas are always available, these schema files are stored within this
package. Schemas are stored as XML Schema Definition (XSD) files in the `bas_metadata_library.schemas.xsd` module.

> [!NOTE]
> To support local validation, imported or included schema locations in local versions of XML schemas, have been
> modified. These changes do not usually change the substance of any schema.
>
> Some material changes *have* had to be made in local schemas in order to workaround specific issues, explained below.

#### Altered Metadata Schema - Geographic Metadata (GMD)

The ISO *Geographic Metadata (GMD)* schema (used directly for the ISO 19115-0 standard, and indirectly in the ISO
19115-2 standard) has been modified to:

1. include the ISO *Geographic Metadata XML (GMX)* schema [1]

[1] In order to allow Anchor elements to substitute primitive/simple values (such as character strings and integers),
as defined in the ISO 19139:2007 and ISO 19139:2012 standards.

### Configuration classes

The configuration of each metadata record is held in a Python dictionary, within a `MetadataRecordConfig` class. This
class includes methods to validate its configuration against a relevant [Configuration Schema](#configuration-schemas).

Configuration classes are defined at the root of each standard, alongside its root
[Metadata Element](#record-element-classes) and XML namespaces. Configuration classes exists for each supported
configuration schema, with methods to convert from one version to another.

### Configuration schemas

Allowed properties and values for record configurations for each [supported Standard](#supported-standards) and
[Supported Profile](#supported-profiles) are defined using a [JSON Schema](https://json-schema.org). These schemas
define any required properties, and any properties with enumerated values.

Configuration schemas are stored as JSON files in the `bas_metadata_library.schemas` module. Schemas are also made
available externally through `https://metadata-resources.data.bas.ac.uk` to allow:

1. other applications to ensure their output will be compatible with this library
2. schema inheritance/extension - for standards that inherit from other standards (such as extensions or profiles)

> [!WARNING]
> These schemas used to be available at `https://metadata-standards.data.bas.ac.uk`, these URLs no longer work.

Configuration schemas are versioned (e.g. `v1`, `v2`) to allow backwards incompatible changes to be made.
Upgrade/Downgrade methods between versions will be provided for a limited time to assist migrating record
configurations between versions.

#### Source and distribution schemas

Standards and profiles usually inherit from other standards and profiles. In order to prevent this creating huge
duplication, inheritance is used to extend a base schema as needed. For example, the ISO 19115-2 standard extends
(and therefore incorporates) the configuration schema for ISO 19115-0.

This is implemented with JSON Schema `$id` and `$schema` properties using URIs within the BAS Metadata Standards website.

Unfortunately, this creates a problem when developing these schemas as, if Schema B relies on Schema A, using its
published identifier as a reference, the published instance of the schema will be used (i.e. the remote schema will be
downloaded when Schema B is validated). If Schema A is being developed, and is not ready to be republished, there is a
difference between the local and remote schemas used, creating unreliable tests.

To avoid this problem, a set of *source* schemas are used, from which a set of *distribution* schemas are generated.
Source schemas (defined in the `bas_metadata_library.schemas.src` module) use internal references to avoid duplication
of content. Whilst distribution schemas inline these references to give self-contained and independent implementations.

> [!NOTE] To update configuration schemas, only source schema should be updated, followed by
[Regenerating](/DEVELOPING.md#generating-configuration-schemas) distribution schemas.

Distribution schemas are used by [Configuration Classes](#configuration-classes), stored in the
`bas_metadata_library.schemas.dist` module and published to the BAS Metadata Standards resources website.

> [!TIP]
> JSON Schema's can be developed using https://www.jsonschemavalidator.net.
>
> For ISO 19115-0/2 schemas only (which are currently essentially identical), a shortcut for resolving references is
> used whereby common members of both schemas are directly copied from the ISO 19115-0 schema into ISO 19115-2.

### ISO 19115 - Automatic transfer option / format IDs

ID attributes are automatically added to `gmd:MD_Format` and `gmd:MD_DigitalTransferOptions` elements in order to
reconstruct related formats and transfer options (see the
[Linking transfer options and formats](#iso-19115-linkages-between-transfer-options-and-formats) section for more
information).

When a record is encoded, ID values are generated by hashing a JSON encoded string of the distribution object. This
ID is used as a shared base between the format and transfer option, with `-fmt` appended for the format and `-tfo`
for the transfer option.

When a record is decoded, ID values are extracted, with suffixes stripped, to index and then match up format and
transfer options back into distribution options. Any format and transfer options without an ID value, or without a
corresponding match, are added as partial distribution options.

As a worked example, encoding a (simplified) distribution object:

```python
do = {
   'format': 'csv',
   'transfer_option': {
      'size': '40',
      'url': 'https://example.com/foo.csv'
   }
}
```

Becomes a JSON encoded string:

```text
'{"format":"csv","transfer_option":{"size":40,"url":"https://example.com/foo.csv"}}'
```

And then a hashed value:

```text
16b7b5df78a664b15d69feda7ccc7caed501f341
```

And then an `id` attribute in a `gmd:MD_Format` element:

```xml
<gmd:MD_Format id="bml-16b7b5df78a664b15d69feda7ccc7caed501f341-fmt" />
```

And a corresponding `id` attribute in a `gmd:MD_DigitalTransferOptions` element:

```xml
<gmd:MD_DigitalTransferOptions id="bml-16b7b5df78a664b15d69feda7ccc7caed501f341-tfo" />
```

> [!TIP]
> The `bml-` prefix ensures all IDs begin with a letter (as required by XML), and allow IDs generated by this library
> to be detected. The `-fmt`/`-tfo` prefixes are used to allow the same ID value to identify each element uniquely.

## Setup

See [Setup](DEVELOPING.md#setup) documentation.

## Development

See [Development](DEVELOPING.md) documentation.

## Releases

- [latest release 🛡️](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/releases/permalink/latest)
- [all releases 🛡️](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/releases)
- [PyPi](https://pypi.org/project/bas-metadata-library/)

See the [Release Workflow](DEVELOPING.md#release-workflow) for creating a new release.

## Project maintainer

Mapping and Geographic Information Centre ([MAGIC](https://www.bas.ac.uk/teams/magic)), British Antarctic Survey
([BAS](https://www.bas.ac.uk)).

Project lead: [@felnne](https://www.bas.ac.uk/profile/felnne).

## Data protection

A Data Protection Impact Assessment (DPIA) does not apply to this project.

## License

Copyright (c) 2019-2025 UK Research and Innovation (UKRI), British Antarctic Survey (BAS).

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
