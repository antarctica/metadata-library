# BAS Metadata Library - Implementation

This library is implemented in Python and consists of a set of classes to generate XML metadata records from a
configuration object (Python dict), or to generate such an object from an XML record.

Each [Supported Standard](/README.md#supported-standards) is implemented as a module under
`bas_metadata_library.standards`. Each [Supported Profile](/README.md#supported-profiles) is implemented as modules
under their respective standard.

## Base classes

For each standard and profile, instances of these base classes are defined:

- `Namespaces`
- `MetadataRecord`
- `MetadataRecordConfig`

The `Namespaces` class is a mapping between XML namespaces, their shorthand aliases and their XML definition XSDs.

The `MetadataRecord` class represents a metadata record and defines the Root [Element](#record-element-classes). These
classes provide methods to generate XML documents or parse an XML document into a `MetadataRecordConfig` class.

The `MetadataRecordConfig` class represents the [Configuration](#configuration-classes) defining the structure and
values for a `MetadataRecord` (either for new records, or derived from existing records). This class provides methods
to validate the configuration and dumping/loading from/to JSON.

## Record element classes

Each supported element, in each [supported standard](/README.md#supported-standards), inherit and use the
`MetadataRecordElement` class to:

- encode configuration values into an XML fragment of at least one element
- decode an XML fragment into one or more configuration values

Specifically, at least two methods are implemented:

- `make_element()` which builds an XML element using values from a configuration object
- `make_config()` which uses typically XPath expressions to build a configuration object from XML

These methods may be simple (if encoding or decoding a simple free text value for example), or quite complex, using
sub-elements (which themselves may contain sub-elements as needed).

## Record schemas

Allowed elements, attributes and values for each [supported Standard](/README.md#supported-standards), and if
applicable, [Supported Profile](/README.md#supported-profiles) are defined using one or more
[XML Schemas](https://www.w3.org/XML/Schema). These schemas define any required entities, and any entities with
enumerated values. Schemas are usually published by standards organisations to facilitate record validation.

For performance, and to ensure required schemas are always available, these schema files are stored within this
package. Schemas are stored as XML Schema Definition (XSD) files in the `bas_metadata_library.schemas.xsd` module.

> [!NOTE]
> To support local validation, imported or included schema locations in local versions of XML schemas, have been
> modified. These changes do not usually change the substance of any schema.
>
> Some material changes *have* had to be made in local schemas in order to workaround specific issues, explained below.

### Altered Metadata Schema - Geographic Metadata (GMD)

The ISO *Geographic Metadata (GMD)* schema (used directly for the ISO 19115-0 standard, and indirectly in the ISO
19115-2 standard) has been modified to:

1. include the ISO *Geographic Metadata XML (GMX)* schema [1]

[1] In order to allow Anchor elements to substitute primitive/simple values (such as character strings and integers),
as defined in the ISO 19139:2007 and ISO 19139:2012 standards.

## Configuration classes

The configuration of each metadata record is held in a Python dictionary, within a `MetadataRecordConfig` class. This
class includes methods to validate its configuration against a relevant [Configuration Schema](#configuration-schemas).

Configuration classes are defined at the root of each standard, alongside its root
[Metadata Element](#record-element-classes) and XML namespaces. Configuration classes exists for each supported
configuration schema, with methods to convert from one version to another.

## Configuration schemas

Allowed properties and values for record configurations for each [supported Standard](/README.md#supported-standards)
and [Supported Profile](/README.md#supported-profiles) are defined using a [JSON Schema](https://json-schema.org).
These schemas define any required properties, and any properties with enumerated values.

Configuration schemas are stored as JSON files in the `bas_metadata_library.schemas` module. Schemas are also made
available externally through `https://metadata-resources.data.bas.ac.uk` to allow:

1. other applications to ensure their output will be compatible with this library
2. schema inheritance/extension - for standards that inherit from other standards (such as extensions or profiles)

> [!WARNING]
> These schemas used to be available at `https://metadata-standards.data.bas.ac.uk`, these URLs no longer work.

Configuration schemas are versioned (e.g. `v1`, `v2`) to allow backwards incompatible changes to be made.
Upgrade/Downgrade methods between versions will be provided for a limited time to assist migrating record
configurations between versions.

### Source and distribution schemas

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
> [Regenerating](/docs/dev.md#generating-configuration-schemas) distribution schemas.

Distribution schemas are used by [Configuration Classes](#configuration-classes), stored in the
`bas_metadata_library.schemas.dist` module and published to the BAS Metadata Standards resources website.

> [!TIP]
> JSON Schema's can be developed using https://www.jsonschemavalidator.net.
>
> For ISO 19115-0/2 schemas only (which are currently essentially identical), a shortcut for resolving references is
> used whereby common members of both schemas are directly copied from the ISO 19115-0 schema into ISO 19115-2.

## ISO 19115 Automatic transfer option and format IDs

ID attributes are automatically added to `gmd:MD_Format` and `gmd:MD_DigitalTransferOptions` elements in order to
reconstruct related formats and transfer options (see the
[Linking transfer options and formats](/docs/usage.md#iso-19115-linkages-between-transfer-options-and-formats) section
for more information).

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
