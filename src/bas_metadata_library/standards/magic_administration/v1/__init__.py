import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Final, Optional, TypeVar

import cattrs

TAdministrationMetadata = TypeVar("TAdministration", bound="AdministrationMetadata")


@dataclass
class Permission:
    """
    Access permission.

    Represents a group with access to a resource or resource description within a given directory for a given time.

    Where not specified, the expiry is set to the maximum future time by default representing an unbounded duration.

    A freetext comment can optionally be added for any additional context (e.g. why a non-obvious group has access).

    Note: Comments are ignored in equality comparisons.

    Schema definition: permission [1]

    [1] https://github.com/antarctica/metadata-library/blob/v0.16.0/src/bas_metadata_library/schemas/dist/magic_administration_content_v1.json#L7
    """

    directory: str
    group: str
    expiry: datetime = field(default_factory=lambda: datetime.max.replace(tzinfo=timezone.utc))
    comment: Optional[str] = None

    def __eq__(self, other: object) -> bool:
        """Equality comparison ignoring comment."""
        if not isinstance(other, type(self)):
            raise TypeError() from None
        self_dict = asdict(self)
        other_dict = asdict(other)
        self_dict.pop("comment", None)
        other_dict.pop("comment", None)
        return self_dict == other_dict


@dataclass
class AdministrationMetadata:
    """
    Representation of non-public, non-standard, metadata for internal administrative use.

    This class is a complete mapping of the BAS MAGIC Administration Metadata v1 content schema [1] to Python
    dataclasses.

    This class supports conversion to/from plain types and JSON strings. It does not support signing and/or encryption.

    Schema definition: administration [2]

    Note: in Python 3.10+ set kw_only=True in dataclass decorator.

    [1] https://github.com/antarctica/metadata-library/blob/v0.16.0/src/bas_metadata_library/schemas/dist/magic_administration_content_v1.json
    [2] https://github.com/antarctica/metadata-library/blob/v0.16.0/src/bas_metadata_library/schemas/dist/magic_administration_content_v1.json-L107
    """

    id: str
    gitlab_issues: list[str] = field(default_factory=list)
    metadata_permissions: list[Permission] = field(default_factory=list)
    resource_permissions: list[Permission] = field(default_factory=list)
    _schema: Final[str] = (
        "https://metadata-resources.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/magic-administration-content-v1.json"
    )

    def __post_init__(self) -> None:
        """Validate."""
        if not self.id:
            msg = "Administration metadata requires an id."
            raise TypeError(msg) from None
        for issue in self.gitlab_issues:
            if "/-/issues/" not in issue:
                msg = f"URL '{issue}' is not a valid GitLab issue."
                raise ValueError(msg) from None

    @classmethod
    def structure(cls: type[TAdministrationMetadata], value: dict) -> "AdministrationMetadata":
        """
        Parse AdministrationMetadata class from plain types.

        Returns a new class instance with parsed data. Intended to be used as a cattrs structure hook.
        E.g. `converter.register_structure_hook(AdministrationMetadata, lambda d, t: AdministrationMetadata.structure(d))`
        """
        if value["$schema"] != AdministrationMetadata._schema:
            msg = "Unsupported JSON Schema in data."
            raise ValueError(msg) from None

        converter = cattrs.Converter()
        converter.register_structure_hook(datetime, lambda d, t: datetime.fromisoformat(d))
        return converter.structure(value, cls)

    def unstructure(self) -> dict:
        """
        Convert AdministrationMetadata class into plain types.

        Intended to be used as a cattrs unstructure hook.
        E.g. `converter.register_unstructure_hook(AdministrationMetadata, lambda d: d.unstructure())`
        """
        converter = cattrs.Converter()
        converter.register_unstructure_hook(datetime, lambda d: d.isoformat())
        value = converter.unstructure(self)

        # remove internal keys (ensuring order)
        value.pop("_schema", None)

        return value

    @classmethod
    def loads_json(cls: type[TAdministrationMetadata], value: str) -> "AdministrationMetadata":
        """Parse AdministrationMetadata class from a JSON encoded string."""
        return AdministrationMetadata.structure(json.loads(value))

    def dumps_json(self) -> str:
        """Convert AdministrationMetadata class into a JSON encoded string."""
        return json.dumps({"$schema": self._schema, **self.unstructure()}, indent=2, ensure_ascii=False)
