# BAS Metadata Library

Python library for generating metadata records.

## Overview

The BAS Metadata Library is an underpinning library for other tools and applications to generate discovery level
metadata records (describing products, services and other resources). It is intended to avoid duplicating complex and
verbose encode/decoding logic across projects.

It supports a lossless, two-way, conversion between a
[Configuration Object](/docs/implementation.md#configuration-classes) (a python dict representing the fields/structure
of a record for a standard) into its formal representation (typically an XML document) to support processing and
manipulation of information between and within systems.

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
| ISO 19115 | [MAGIC Discovery Metadata V1](https://metadata-resources.data.bas.ac.uk/profiles/magic-discovery/v1/) | [#250](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/issues/250) |
| ISO 19115 | [MAGIC Discovery Metadata V2](https://metadata-resources.data.bas.ac.uk/profiles/magic-discovery/v2/) | [#250](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/issues/268) |
<!-- pyml enable md013 -->

### Supported configuration versions

<!-- pyml disable md013 -->
| Standard           | Profile                     | Configuration Version                                                                                                     | Status       | Notes                                 |
|--------------------|-----------------------------|---------------------------------------------------------------------------------------------------------------------------|--------------|---------------------------------------|
| IEC 61174:2015     | -                           | [`v1`](https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iec-pas-61174-0-v1.json) | Retired      | No longer supported                   |
| IEC PAS 61174:2021 | -                           | [`v1`](https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iec-pas-61174-1-v1.json) | Retired      | No longer supported                   |
| ISO 19115:2003     | -                           | [`v1`](https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-1-v1.json)     | Retired      | Replaced by `v2`, no longer supported |
| ISO 19115:2003     | -                           | [`v2`](https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-1-v2.json)     | Retired      | Replaced by `v3`, no longer supported |
| ISO 19115:2003     | -                           | [`v3`](https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-1-v3.json)     | Retired      | Replaced by `v4`, no longer supported |
| ISO 19115:2003     | -                           | [`v4`](https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-0-v4.json)     | Stable       | Currently supported version           |
| ISO 19115-2:2009   | -                           | [`v1`](https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v1.json)     | Retired      | Replaced by `v2`, no longer supported |
| ISO 19115-2:2009   | -                           | [`v2`](https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v2.json)     | Retired      | Replaced by `v3`, no longer supported |
| ISO 19115-2:2009   | -                           | [`v3`](https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v3.json)     | Retired      | Replaced by `v4`, no longer supported |
| ISO 19115-2:2009   | -                           | [`v4`](https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v4.json)     | Stable       | Currently supported version           |
| ISO 19115-2:2009   | MAGIC Discovery Metadata V1 | [`v1`](https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/magic-discovery-v1.json) | Stable       | Currently supported version           |
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

> [!TIP]
> To install on Windows, it's recommended to use [UV](https://docs.astral.sh/uv/) to use a Python version covered by
> pre-built `lxml` wheels, avoiding the complexity of building packages from source.

### Installation dependencies

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
    "hierarchy_level": "product",
    "metadata": {
        "contacts": [{"organisation": {"name": "Mapping and Geographic Information Centre, British Antarctic Survey"}, "role": ["pointOfContact"]}],
        "date_stamp": date(2018, 10, 18),
    },
    "identification": {
        "title": {"value": "Test Record"},
        "dates": {"creation": {"date": date(2018, 1, 1), "date_precision": "year"}},
        "abstract": "Test Record for ISO 19115 metadata standard (no profile) with minimal (but not minimal) fields.",
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
> See [HTML Entities](/docs/usage.md#html-entities) for guidance on using accents and symbols in configurations.
>
> See [Date Precision](/docs/usage.md#date-precision) for guidance on using partial (year or year-month) dates.

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

### Further examples

See [Usage](/docs/usage.md) documentation for further usage examples.

## Implementation

See [Implementation](/docs/implementation.md) documentation.

## Setup

See [Setup](/docs/dev.md#setup) documentation.

## Development

See [Development](/docs/dev.md) documentation.

## Releases

- [latest release 🛡️](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/releases/permalink/latest)
- [all releases 🛡️](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/releases)
- [PyPi](https://pypi.org/project/bas-metadata-library/)

See the [Release Workflow](/docs/dev.md#release-workflow) for creating a new release.

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
