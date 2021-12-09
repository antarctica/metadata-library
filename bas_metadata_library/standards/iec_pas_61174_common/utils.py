from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# We don't currently allow untrusted/user-provided XML so this is not a risk
from lxml.etree import Element, fromstring  # nosec


def generate_rtzp_archive(file: Path, rtz_name: str, rtz_document: str) -> None:
    """
    Generates RTZ record in a RTZP data container

    A RTZP container is a zip archive containing a single RTZ file. This inner RTZ file must ne named after the
    'route_name' config property in the record (e.g. if route_name is 'foo', the RTZ file must be named 'foo.rtz').

    :type file: Path
    :param file: path at which to create RTZP data container
    :type rtz_name: str
    :param rtz_name: Name to use for the inner RTZ file
    :type rtz_document: str
    :param rtz_document: Contents of the inner RTZ file as a string
    """
    with TemporaryDirectory() as tmpdirname:
        rtz_path = Path(tmpdirname).joinpath(f"{rtz_name}.rtz")
        with open(str(rtz_path), mode="w") as rtz_file:
            rtz_file.write(rtz_document)
        ZipFile(str(file), mode="w").write(filename=rtz_path, arcname=rtz_path.name)


def load_record_from_rtzp_archive(file: Path) -> Element:
    """
    Loads a RTZ record from a RTZP data container

    :type file: Path
    :param file: path to RTZP data container
    :rtype Element
    :returns Parsed RTZ record as an XML element
    """
    with ZipFile(str(file)) as rtzp_file:
        return fromstring(rtzp_file.read(rtzp_file.namelist()[0]))
