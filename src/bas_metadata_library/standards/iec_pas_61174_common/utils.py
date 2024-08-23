from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from lxml.etree import Element, fromstring


def generate_rtzp_archive(file: Path, rtz_name: str, rtz_document: str) -> None:
    """
    Generates RTZ record in a RTZP data container.

    A RTZP container is a zip archive containing a single RTZ file. This inner RTZ file must be named after the
    'route_name' config property in the record (e.g. if route_name is 'foo', the RTZ file must be named 'foo.rtz').

    :param file: path at which to create RTZP data container
    :param rtz_name: Name to use for the inner RTZ file
    :param rtz_document: Contents of the inner RTZ file as a string
    """
    with TemporaryDirectory() as tmpdirname:
        rtz_path = Path(tmpdirname).joinpath(f"{rtz_name}.rtz")
        with rtz_path.open(mode="w") as rtz_file:
            rtz_file.write(rtz_document)
        ZipFile(str(file), mode="w").write(filename=rtz_path, arcname=rtz_path.name)


def load_record_from_rtzp_archive(file: Path) -> Element:
    """
    Loads a RTZ record from a RTZP data container.

    :param file: path to RTZP data container
    :returns Parsed RTZ record as an XML element
    """
    with ZipFile(str(file)) as rtzp_file:
        return fromstring(rtzp_file.read(rtzp_file.namelist()[0]))  # noqa: S320 (see '`lxml` package (security)' README section)
