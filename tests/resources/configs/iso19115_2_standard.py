from copy import deepcopy

from tests.resources.configs.iso19115_0_standard import base_complex_record_v4 as _base_complex_record_v4
from tests.resources.configs.iso19115_0_standard import base_simple_record_v4 as _base_simple_record_v4
from tests.resources.configs.iso19115_0_standard import complete_record_v4 as _complete_record_v4
from tests.resources.configs.iso19115_0_standard import minimal_record_v4 as _minimal_record_v4

minimal_record_v4 = deepcopy(_minimal_record_v4)  # type: dict
minimal_record_v4["$schema"] = (
    "https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v4.json"
)

base_simple_record_v4 = deepcopy(_base_simple_record_v4)  # type: dict
base_simple_record_v4["$schema"] = (
    "https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v4.json"
)

base_complex_record_v4 = deepcopy(_base_complex_record_v4)  # type: dict
base_complex_record_v4["$schema"] = (
    "https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v4.json"
)

complete_record_v4 = deepcopy(_complete_record_v4)  # type: dict
complete_record_v4["$schema"] = (
    "https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v4.json"
)

configs_v4_all = {
    "minimal_v4": minimal_record_v4,
    "base-simple_v4": base_simple_record_v4,
    "base-complex_v4": base_complex_record_v4,
    "complete_v4": complete_record_v4,
}

configs_all = {**configs_v4_all}
