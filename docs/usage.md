# BAS Metadata Library - Usage

## Loading a record configuration from JSON

The `load()` and `loads()` methods on the relevant configuration class can load a record configuration encoded as a
JSON file or JSON string respectively:

```python
from pathlib import Path

from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV4

input_path = str('/path/to/file.json')

configuration = MetadataRecordConfigV4()
configuration.load(file=Path(input_path))
```

## Dumping a record configuration to JSON

The `dump()` and `dumps()` methods on the relevant configuration class can dump a record configuration to a JSON
encoded file or string respectively:

```python
from datetime import date
from pathlib import Path

from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV4

output_path = str('/path/to/file.json')

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
configuration = MetadataRecordConfigV4(**minimalish_config)
configuration.dump(file=Path(output_path))
```

## Encode MAGIC administration metadata within an ISO 19115 record

To generate an ISO 19115 metadata record containing MAGIC administration metadata:

```python
from datetime import date, datetime, timezone
from uuid import uuid4

from jwskate import Jwk

from bas_metadata_library.standards.iso_19115_2 import MetadataRecord, MetadataRecordConfigV4
from bas_metadata_library.standards.magic_administration.v1 import AdministrationMetadata, Permission
from bas_metadata_library.standards.magic_administration.v1.utils import AdministrationKeys, set_admin

# setup keys for signing and encrypting administration metadata
admin_keys = AdministrationKeys(
    signing_private=Jwk({
        "kty": "EC",
        "kid": "bas_metadata_testing_signing_key",
        "alg": "ES256",
        "crv": "P-256",
        "x": "FzxBM1ZPO5W2bYlhT9AjZUKz5_oH5vIh4_k4aEZ64rM",
        "y": "vmK5PWOoIA9eO0ntLh37AMpVODyj0NWf842FwoN-GRs",
        "d": "FdxFSRF2zAAfn7_GaDk81T8PdBGlzZpRtxd10-kc4PE",
    }),
    encryption_private=Jwk({
    "kty": "EC",
    "kid": "bas_metadata_testing_encryption_key",
    "alg": "ECDH-ES+A128KW",
    "crv": "P-256",
    "x": "kYiwq6MW8lGN6PB2csVMuMRcISVk5eNUpGkjM-mm8QY",
    "y": "raOTT2xAQhHFKhPHy338L8Ql0hvgsDtHwtEc8pCOf2Q",
    "d": "2lBuUtJK2TcV_b4B-bDCPnRVAqMnYvnLZ41IUguprs8",
}),
)

# generate random identifier for the resource
resource_identifier = str(uuid4())

# define administration metadata with:
# - associated GitLab issue
# - permissions to allow anyone to access to the metadata (an implicit expiry at Python max datetime will be set)
# - permissions to allow a specific group in a directory/IdP to access the resource until an explicit date
admin_meta = AdministrationMetadata(
    id=resource_identifier,
    gitlab_issues=['https://gitlab.com/group/project/-/issues/123'],
    metadata_permissions=[Permission(directory="*", group="*", comment="Unrestricted access.")],
    resource_permissions=[Permission(directory="123", group="abc", expiry=datetime(2018, 10, 18, tzinfo=timezone.utc), comment="Restricted access.")],
)

# define a minimalish record configuration (file_identifier is required)
minimalish_config = {
    "$schema": "https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-1-v4.json",
    "file_identifier": resource_identifier,
    "hierarchy_level": "product",
    "metadata": {
        "contacts": [{"organisation": {"name": "Mapping and Geographic Information Centre, British Antarctic Survey"}, "role": ["pointOfContact"]}],
        "date_stamp": date(2018, 10, 18),
    },
    "identification": {
        "title": {"value": "Test Record"},
        "dates": {"creation": {"date": date(2018, 1, 1), "date_precision": "year"}},
        "abstract": "Test Record for ISO 19115 metadata standard with MAGIC administration metadata and profile, plus minimal (but not minimal) fields.",
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

# encode admin metadata within record config
set_admin(keys=admin_keys, config=minimalish_config, admin_meta=admin_meta)

# encode configuration into a formal document
config = MetadataRecordConfigV4(**minimalish_config)
record = MetadataRecord(configuration=config)
document = record.generate_xml_document()

# output document
print(document.decode())
```

## Decode administration metadata from an ISO 19115 record

To extract MAGIC administration metadata from an ISO 19115 metadata record:

```python
from pathlib import Path

from jwskate import Jwk

from bas_metadata_library.standards.iso_19115_2 import MetadataRecord
from bas_metadata_library.standards.magic_administration.v1.utils import AdministrationKeys, get_admin

# setup keys for signing and encrypting administration metadata
admin_keys = AdministrationKeys(
    signing_private=Jwk({
        "kty": "EC",
        "kid": "bas_metadata_testing_signing_key",
        "alg": "ES256",
        "crv": "P-256",
        "x": "FzxBM1ZPO5W2bYlhT9AjZUKz5_oH5vIh4_k4aEZ64rM",
        "y": "vmK5PWOoIA9eO0ntLh37AMpVODyj0NWf842FwoN-GRs",
        "d": "FdxFSRF2zAAfn7_GaDk81T8PdBGlzZpRtxd10-kc4PE",
    }),
    encryption_private=Jwk({
        "kty": "EC",
        "kid": "bas_metadata_testing_encryption_key",
        "alg": "ECDH-ES+A128KW",
        "crv": "P-256",
        "x": "kYiwq6MW8lGN6PB2csVMuMRcISVk5eNUpGkjM-mm8QY",
        "y": "raOTT2xAQhHFKhPHy338L8Ql0hvgsDtHwtEc8pCOf2Q",
        "d": "2lBuUtJK2TcV_b4B-bDCPnRVAqMnYvnLZ41IUguprs8",
    }),
)

with Path(f"record.xml").open() as document_file:
    document = document_file.read()

record = MetadataRecord(record=document)
configuration = record.make_config()
config = configuration.config
print(get_admin(keys=admin_keys, config=config).dumps_json())
```

## Validating a record

The formal encoding of a record can be validated against one or more XML schemas relevant to each metadata or data
standard. Records are not validated automatically, and so must be validated explicitly:

```python
from datetime import date

from bas_metadata_library import RecordValidationError
from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV4, MetadataRecord

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

These errors should not happen, and if they do are considered internal bugs and [Reported](/README.md#project-maintainer).

See the [Record Schemas](/docs/implementation.md#record-schemas) section for more information on how validation works.

## Validating a record configuration

[Record configurations](/docs/implementation.md#configuration-classes) will be automatically validated using a JSON
Schema for the metadata standard used.

> [!TIP]
> Where a record configuration states compliance with one or more [Supported Profiles](/README.md#supported-profiles),
> it will also be automatically validated using a JSON Schema for each profile.
>
> For ISO 19115, profile compliance is indicated via a domain consistency data quality element.

To explicitly validate a record configuration:

```python
from datetime import date

from jsonschema import ValidationError
from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV4

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

See the [Record Configuration Schemas](/docs/implementation.md#configuration-schemas) section for more information.

## HTML entities

HTML entities (e.g. `&gt;`) will be double escaped by [Lxml](https://lxml.de) (the XML library used internally) and so
should be avoided. Literal characters (e.g. `>`) should be used instead, which will then be escaped automatically. This
also applies to any Unicode characters, such as accents (e.g. `å`) or symbols (e.g. `µ`).

E.g. If `&gt;`, the HTML entity for `>` (greater than), is used as input, it will be escaped again to the invalid
output `&amp;gt;`.

## Date Precision

Dates and date-times used in Python record configurations MUST be structured as dictionaries with a `date` property,
containing a date or date-time value.

Where this value represents a date with an unknown year or year and month, an additional `date_precision` property MUST
be set with a value of either:

- `year` (month and day are unknown)
- `month` (day is unknown)

Partial dates or date-times will be detected and a `date_precision` property set automatically when decoding records.

Python date and date time objects require values for all elements (even when unknown). Partial/unknown elements SHOULD
use '1' as a workaround value in these cases, which will be ignored when encoded.

When using JSON for [Record configurations](/docs/implementation.md#configuration-classes), date or date times MUST be
written as strings, with partial values expressed naturally (e.g. `2014` or `2012-04`), without the need for wrapping
object and `date_precision` property.

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

## ISO 19115 linkages between transfer options and formats

In ISO 19115, there is no formal mechanism to associate file distribution formats and transfer options, needed to
produce download tables such as [1].

As this library seeks to be fully reversible between a configuration dict and formal XML encoding, associations between
these elements would be lost when records are encoded as XML. In
[Record Configurations](/docs/implementation.md#configuration-classes), these associations are encoded using a
'distribution option' concept.

Within formal XML records, associations are encoded using `xsd:ID` attributes in `gmd:MD_Format` and
`gmd:DigitalTransferOptions` elements, with values allowing associations to be reconstructed when decoding XML records.

> [!CAUTION]
> Do not modify automatically assigned IDs outside of this library.

See the [Automatic transfer option / format IDs](/docs/implementation.md#iso-19115-automatic-transfer-option-and-format-ids)
section for implementation details.

[1]

| Format     | Size   | Download Link                |
|------------|--------|------------------------------|
| CSV        | 68 kB  | [Link](https://example.com/) |
| GeoPackage | 1.2 MB | [Link](https://example.com/) |

## MAGIC Administration metadata

To support the internal management of metadata records,
[Administrative metadata](https://metadata-standards.data.bas.ac.uk/profiles/magic-administration-v1/) (as opposed
to discovery, calibration or other metadata) can be included in ISO 19115 records.

> [!NOTE]
> Administrative metadata uses an internally developed information model and is not intended for external use.
> Administrative metadata is stored in the supplemental information element within the ISO 19115 information model.

The `bas_metadata_library.standards.magic_administration.v1.AdministrationMetadata` Python data class implements
the information model for administration metadata, and encoding/decoding to/from a string encoded JSON value.

The `bas_metadata_library.standards.magic_administration.v1.AdministrationMetadata.utils.AdministrationWrapper` class
implements encoding/decoding a JSON string encoded administration metadata instance within a JSON Web Token (JWT).

Specifically the administration metadata string is included as a custom `pyd` (payload) claim within an asymmetrically
signed, long-lived, JWT. This is nested within a symmetrically encrypted JWE (JSON Web Encryption) string, suitable for
embedding within an ISO 19115 record. JSON Web Keys (JWKs) for signing/verifying JWTs and encrypting/decrypting JWEs
are held in a
`bas_metadata_library.standards.magic_administration.v1.AdministrationMetadata.utils.AdministrationKeys` data class.

The `bas_metadata_library.standards.magic_administration.v1.AdministrationMetadata.utils.get_admin` and `set_admin`
methods implement encoding/decoding a JWE value within an ISO 19115 record configuration via the
[`gmd:supplementalInformation`](https://www.datypic.com/sc/niem21/e-gmd_supplementalInformation-1.html) element, as a
string encoded JSON object under an `admin_metadata` key.

> [!TIP]
> See the [Administrative metadata](https://metadata-standards.data.bas.ac.uk/profiles/magic-administration-v1/) profile
> for more information on the administration metadata information model, and encoding.
