from copy import deepcopy

from tests.resources.configs.iec_pas_61174_0_standard import minimal_record_v1 as _minimal_record_v1
from tests.resources.configs.iec_pas_61174_0_standard import complete_record_v1 as _complete_record_v1

minimal_record_v1 = deepcopy(_minimal_record_v1)  # type: dict
minimal_record_v1[
    "$schema"
] = "https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iec-pas-61174-1-v1.json"

complete_record_v1 = deepcopy(_complete_record_v1)  # type: dict
complete_record_v1[
    "$schema"
] = "https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iec-pas-61174-1-v1.json"

configs_v1 = {"minimal_v1": minimal_record_v1, "complete_v1": complete_record_v1}
configs_all = {**configs_v1}
