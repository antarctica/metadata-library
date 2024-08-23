from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from importlib_resources import files as resource_file
from lxml.etree import Element, SubElement, fromstring

from bas_metadata_library import (
    MetadataRecord as _MetadataRecord,
)
from bas_metadata_library import (
    MetadataRecordConfig as _MetadataRecordConfig,
)
from bas_metadata_library import (
    MetadataRecordElement as _MetadataRecordElement,
)
from bas_metadata_library import (
    Namespaces as _Namespaces,
)
from bas_metadata_library.standards.iec_pas_61174_common.utils import (
    generate_rtzp_archive as _generate_rtzp_archive,
)
from bas_metadata_library.standards.iec_pas_61174_common.utils import (
    load_record_from_rtzp_archive,
)


class Namespaces(_Namespaces):
    """Defines the namespaces for this standard."""

    rtz = "http://www.cirm.org/RTZ/1/2"
    xsi = "http://www.w3.org/2001/XMLSchema-instance"

    _schema_locations = {  # noqa: RUF012
        "rtz": "https://www.cirm.org/rtz/RTZ%20Schema%20version%201_2.xsd",
    }

    def __init__(self):
        self._namespaces = {
            "rtz": self.rtz,
            "xsi": self.xsi,
        }

        super().__init__(namespaces=self._namespaces, root_namespace=self.rtz)


class MetadataRecordElement(_MetadataRecordElement):
    """
    Overloaded base MetadataRecordElement class.

    Sets:
     - the type hint of the record attribute to the MetadataRecord class for this metadata standard
     - the namespaces property to the Namespaces class for this metadata standard
    """

    def __init__(
        self,
        record: _MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict | None = None,
        xpath: str | None = None,
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes,
            xpath=xpath,
        )
        self.ns = Namespaces()


class MetadataRecordConfigV1(_MetadataRecordConfig):
    """
    Overloaded base MetadataRecordConfig class.

    Defines version 1 of the JSON Schema used for this metadata standard.
    """

    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)

        self.config = kwargs

        schema_path = resource_file("bas_metadata_library.schemas.dist").joinpath("iec_pas_61174_1_v1.json")
        with schema_path.open() as schema_file:
            schema_data = json.load(schema_file)
        self.schema = schema_data

        # Workaround - will be addressed in #149
        self.schema_uri = schema_data["$id"]
        self.config = {"$schema": self.schema_uri, **kwargs}


class MetadataRecord(_MetadataRecord):
    """Defines the root element, and it's sub-elements, for this metadata standard."""

    def __init__(self, configuration: MetadataRecordConfigV1 = None, record: str | None = None):
        self.ns = Namespaces()
        self.attributes = {}
        self.record = Element(
            f"{{{self.ns.rtz}}}route",
            attrib={
                "version": str(1.2),
                f"{{{self.ns.xsi}}}schemaLocation": self.ns.schema_locations(),
            },
            nsmap=self.ns.nsmap(),
        )
        self.xpath = "/rtz:route"

        if configuration is not None:
            configuration.validate()
            self.attributes: dict[str, Any] = configuration.config

        if record is not None:
            self.record = fromstring(record.encode())  # noqa: S320 (see '`lxml` package (security)' README section)

        self.metadata_record = Route(record=self.record, attributes=self.attributes, xpath=self.xpath)

    def make_config(self) -> MetadataRecordConfigV1:
        return MetadataRecordConfigV1(**self.metadata_record.make_config())

    def make_element(self) -> Element:
        return self.metadata_record.make_element()

    def generate_rtzp_archive(self, file: Path) -> None:
        """
        Generates RTZ/XML record in a RTZP data container.

        A RTZP container is a zip archive containing a single RTZ file.

        :param file: path at which to create RTZP data container
        """
        _generate_rtzp_archive(
            file=file, rtz_name=self.attributes["route_name"], rtz_document=self.generate_xml_document().decode()
        )

    def load_from_rtzp_archive(self, file: Path) -> None:
        """Loads a RTZ record from a RTZP data container."""
        self.record = load_record_from_rtzp_archive(file=file)
        self.metadata_record = Route(record=self.record, attributes=self.attributes, xpath=self.xpath)

    # noinspection PyMethodOverriding
    def validate(self) -> None:
        super().validate(xsd_path=Path("rtz/rtz_1_2.xsd"))


class Route(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        route_information = RouteInformation(record=self.record, attributes=self.attributes, xpath=f"{self.xpath}")
        _route_information = route_information.make_config()
        if bool(_route_information):
            if "author" in _route_information:
                _["route_author"] = _route_information["author"]
            if "name" in _route_information:
                _["route_name"] = _route_information["name"]
            if "status" in _route_information:
                _["route_status"] = _route_information["status"]

        waypoints = Waypoints(record=self.record, attributes=self.attributes, xpath=f"{self.xpath}")
        _waypoints = waypoints.make_config()
        if bool(_waypoints):
            _["waypoints"] = _waypoints

        return _

    def make_element(self) -> None:
        if (
            "route_author" in self.element_attributes
            or "route_name" in self.element_attributes
            or "route_status" in self.element_attributes
        ):
            route_information = RouteInformation(
                record=self.record,
                attributes=self.attributes,
                element_attributes=self.attributes,
                parent_element=self.record,
            )
            route_information.make_element()
        if "waypoints" in self.element_attributes:
            waypoints = Waypoints(
                record=self.record,
                attributes=self.attributes,
                element_attributes=self.attributes,
                parent_element=self.record,
            )
            waypoints.make_element()

        return self.record


class RouteInformation(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        route_author = self.record.xpath(
            f"{self.xpath}/rtz:routeInfo/@routeAuthor",
            namespaces=self.ns.nsmap(suppress_root_namespace=True),
        )
        if len(route_author) > 0:
            _["author"] = route_author[0]

        route_name = self.record.xpath(
            f"{self.xpath}/rtz:routeInfo/@routeName",
            namespaces=self.ns.nsmap(suppress_root_namespace=True),
        )
        if len(route_name) > 0:
            _["name"] = route_name[0]

        route_status = self.record.xpath(
            f"{self.xpath}/rtz:routeInfo/@routeStatus",
            namespaces=self.ns.nsmap(suppress_root_namespace=True),
        )
        if len(route_status) > 0:
            _["status"] = route_status[0]

        return _

    def make_element(self) -> None:
        attributes = {}

        if "route_author" in self.element_attributes:
            attributes["routeAuthor"] = self.element_attributes["route_author"]
        if "route_name" in self.element_attributes:
            attributes["routeName"] = self.element_attributes["route_name"]
        if "route_status" in self.element_attributes:
            attributes["routeStatus"] = self.element_attributes["route_status"]

        SubElement(self.parent_element, f"{{{self.ns.rtz}}}routeInfo", attrib=attributes)


class Waypoints(MetadataRecordElement):
    def make_config(self) -> list:
        _ = []

        waypoints_length = int(
            self.record.xpath(
                f"count({self.xpath}/rtz:waypoints/rtz:waypoint)",
                namespaces=self.ns.nsmap(suppress_root_namespace=True),
            )
        )
        for waypoint_index in range(1, waypoints_length + 1):
            _waypoint = {}

            waypoint_id = self.record.xpath(
                f"{self.xpath}/rtz:waypoints/rtz:waypoint[{waypoint_index}]/@id",
                namespaces=self.ns.nsmap(suppress_root_namespace=True),
            )
            if len(waypoint_id) > 0:
                _waypoint["id"] = int(waypoint_id[0])

            waypoint_revision = self.record.xpath(
                f"{self.xpath}/rtz:waypoints/rtz:waypoint[{waypoint_index}]/@revision",
                namespaces=self.ns.nsmap(suppress_root_namespace=True),
            )
            if len(waypoint_revision) > 0:
                _waypoint["revision"] = int(waypoint_revision[0])

            position = Position(
                record=self.record,
                attributes=self.attributes,
                xpath=f"{self.xpath}/rtz:waypoints/rtz:waypoint[{waypoint_index}]",
            )
            _position = position.make_config()
            if bool(_position):
                _waypoint["position"] = _position

            leg = self.record.xpath(
                f"{self.xpath}/rtz:waypoints/rtz:waypoint[{waypoint_index}]/rtz:leg",
                namespaces=self.ns.nsmap(suppress_root_namespace=True),
            )
            if len(leg) > 0:
                leg = Leg(
                    record=self.record,
                    attributes=self.attributes,
                    xpath=f"{self.xpath}/rtz:waypoints/rtz:waypoint[{waypoint_index}]",
                )
                _leg = leg.make_config()
                if bool(_leg):
                    _waypoint["leg"] = _leg

            if bool(_waypoint):
                _.append(_waypoint)

        return _

    def make_element(self) -> None:
        waypoints_element = SubElement(self.parent_element, f"{{{self.ns.rtz}}}waypoints")
        for waypoint in self.element_attributes["waypoints"]:
            attributes = {"id": str(waypoint["id"]), "revision": str(waypoint["revision"])}
            waypoint_element = SubElement(waypoints_element, f"{{{self.ns.rtz}}}waypoint", attrib=attributes)

            position = Position(
                record=self.record,
                attributes=self.attributes,
                element_attributes=waypoint["position"],
                parent_element=waypoint_element,
            )
            position.make_element()

            if "leg" in waypoint:
                leg = Leg(
                    record=self.record,
                    attributes=self.attributes,
                    element_attributes=waypoint["leg"],
                    parent_element=waypoint_element,
                )
                leg.make_element()


class Position(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        lat = self.record.xpath(
            f"{self.xpath}/rtz:position/@lat",
            namespaces=self.ns.nsmap(suppress_root_namespace=True),
        )
        if len(lat) > 0:
            _["lat"] = float(lat[0])

        lon = self.record.xpath(
            f"{self.xpath}/rtz:position/@lon",
            namespaces=self.ns.nsmap(suppress_root_namespace=True),
        )
        if len(lon) > 0:
            _["lon"] = float(lon[0])

        return _

    def make_element(self) -> None:
        attributes = {"lat": str(self.element_attributes["lat"]), "lon": str(self.element_attributes["lon"])}
        SubElement(self.parent_element, f"{{{self.ns.rtz}}}position", attrib=attributes)


class Leg(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        geometry_type = self.record.xpath(
            f"{self.xpath}/rtz:leg/@geometryType",
            namespaces=self.ns.nsmap(suppress_root_namespace=True),
        )
        if len(geometry_type) > 0:
            _["geometry_type"] = geometry_type[0]

        return _

    def make_element(self) -> None:
        attributes = {}
        if "geometry_type" in self.element_attributes:
            attributes["geometryType"] = self.element_attributes["geometry_type"]
        SubElement(self.parent_element, f"{{{self.ns.rtz}}}leg", attrib=attributes)
