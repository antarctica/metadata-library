import json

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from importlib_resources import path as resource_path

# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# We don't currently allow untrusted/user-provided XML so this is not a risk
from lxml.etree import Element, SubElement, XMLSchema, fromstring  # nosec

from bas_metadata_library import (
    Namespaces as _Namespaces,
    MetadataRecordConfig as _MetadataRecordConfig,
    MetadataRecord as _MetadataRecord,
    MetadataRecordElement as _MetadataRecordElement,
)


class Namespaces(_Namespaces):
    """
    Overloaded base Namespaces class

    Defines the namespaces for this standard
    """

    rtz = "http://www.cirm.org/RTZ/1/2"
    xsi = "http://www.w3.org/2001/XMLSchema-instance"

    _schema_locations = {
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
    Overloaded base MetadataRecordElement class

    Sets:
     - the type hint of the record attribute to the MetadataRecord class for this metadata standard
     - the namespaces property to the Namespaces class for this metadata standard
    """

    def __init__(
        self,
        record: _MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None,
        xpath: str = None,
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
    Overloaded base MetadataRecordConfig class

    Defines version 1 of the JSON Schema used for this metadata standard
    """

    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)

        self.config = kwargs

        with resource_path(
            "bas_metadata_library.schemas.dist", "iec_pas_61174_0_v1.json"
        ) as configuration_schema_file_path:
            with open(configuration_schema_file_path) as configuration_schema_file:
                configuration_schema_data = json.load(configuration_schema_file)
        self.schema = configuration_schema_data


class MetadataRecord(_MetadataRecord):
    """
    Overloaded base MetadataRecordConfig class

    Defines the root element, and it's sub-elements, for this metadata standard
    """

    def __init__(self, configuration: MetadataRecordConfigV1 = None, record: str = None):
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
            self.attributes = configuration.config

        if record is not None:
            self.record = fromstring(record.encode())

        self.metadata_record = Route(record=self.record, attributes=self.attributes, xpath=self.xpath)

    def make_config(self) -> MetadataRecordConfigV1:
        return MetadataRecordConfigV1(**self.metadata_record.make_config())

    def make_element(self) -> Element:
        return self.metadata_record.make_element()

    def generate_xml_document(self, xml_declaration: bool = True, version: float = 1.2) -> bytes:
        """
        Generates RTZ record

         This standard supports multiple minor versions, which can be set using the `version` parameter.

         The XML document is encoded as a UTF-8 byte string, with pretty-printing, and by default, an XML declaration.

         :type xml_declaration: bool
         :param xml_declaration: Whether to include an XML declaration, defaults to True
         :type version: float
         :param version: minor version of standard to use, valid options: 1.0, 1.2
         :rtype bytes
         :return: XML document in bytes
        """
        if version not in [1.0, 1.2]:
            raise ValueError(f"Invalid standard version [{version}], valid values: 1.0, 1.2")

        if version == 1.2:
            self.validate()

        if version == 1.0:
            self.record.attrib["version"] = str(1.0)
            self.record.attrib[f"{{{self.ns.xsi}}}schemaLocation"] = self.record.attrib[
                f"{{{self.ns.xsi}}}schemaLocation"
            ].replace(
                "https://www.cirm.org/rtz/RTZ%20Schema%20version%201_2.xsd",
                "https://www.cirm.org/rtz/RTZ%20Schema%20version%201_0.xsd",
            )

        return super().generate_xml_document(xml_declaration)

    def generate_rtzp_archive(self, file: Path, rtz_version: float = 1.2):
        """
        Generates RTZ record in a RTZP data container

        A RTZP container is a zip archive containing a single RTZ file. This inner RTZ file is named after the
        'route_name' config property (e.g. if route_name is 'foo', the RTZ file will be named 'foo.rtz').

        :type rtz_version: float
        :param rtz_version: minor version of standard to use, valid options: 1.0, 1.2
        :type file: Path
        :param file: path at which to create RTZP data container
        """
        with TemporaryDirectory() as tmpdirname:
            rtz_path = Path(tmpdirname).joinpath(f"{self.attributes['route_name']}.rtz")
            with open(str(rtz_path), mode="w") as rtz_file:
                rtz_file.write(self.generate_xml_document(version=rtz_version).decode())
            ZipFile(str(file), mode="w").write(filename=rtz_path, arcname=rtz_path.name)

    def load_from_rtzp_archive(self, file: Path):
        """
        Loads a RTZ record from a RTZP data container

        :type file: Path
        :param file: path to RTZP data container
        """
        with ZipFile(str(file)) as rtzp_file:
            self.record = fromstring(rtzp_file.read(rtzp_file.namelist()[0]))
            self.metadata_record = Route(record=self.record, attributes=self.attributes, xpath=self.xpath)

    def validate(self) -> None:
        pass
        with resource_path("bas_metadata_library.schemas.xsd", "rtz_1_2.xsd") as schema_file_path:
            with open(schema_file_path) as validation_schema_file:
                validation_schema_document = fromstring(validation_schema_file.read().encode())

        validation_schema = XMLSchema(validation_schema_document)
        validation_document: MetadataRecord = deepcopy(self)
        validation_schema.assertValid(validation_document.make_element())


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
            _["lat"] = int(lat[0])

        lon = self.record.xpath(
            f"{self.xpath}/rtz:position/@lon",
            namespaces=self.ns.nsmap(suppress_root_namespace=True),
        )
        if len(lon) > 0:
            _["lon"] = int(lon[0])

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
