from copy import deepcopy

from tests.resources.configs.iso19115_1_standard import (
    minimal_record_v2 as _minimal_record_v2,
    base_simple_record_v2 as _base_simple_record_v2,
    base_complex_record_v2 as _base_complex_record_v2,
    complete_record_v2 as _complete_record_v2,
    minimal_record_v3 as _minimal_record_v3,
    base_simple_record_v3 as _base_simple_record_v3,
    base_complex_record_v3 as _base_complex_record_v3,
    complete_record_v3 as _complete_record_v3,
)

minimal_record_v2 = deepcopy(_minimal_record_v2)  # type: dict

base_simple_record_v2 = deepcopy(_base_simple_record_v2)  # type: dict

base_complex_record_v2 = deepcopy(_base_complex_record_v2)  # type: dict

complete_record_v2 = deepcopy(_complete_record_v2)  # type: dict

minimal_record_v3 = deepcopy(_minimal_record_v3)  # type: dict

base_simple_record_v3 = deepcopy(_base_simple_record_v3)  # type: dict

base_complex_record_v3 = deepcopy(_base_complex_record_v3)  # type: dict

complete_record_v3 = deepcopy(_complete_record_v3)  # type: dict

configs_safe_v2 = {
    "minimal_v2": minimal_record_v2,
    "base-simple_v2": base_simple_record_v2,
    "base-complex_v2": base_complex_record_v2,
    "complete_v2": complete_record_v2,
}
configs_v2_all = {**configs_safe_v2}

configs_safe_v3 = {
    "minimal_v3": minimal_record_v3,
    "base-simple_v3": base_simple_record_v3,
    "base-complex_v3": base_complex_record_v3,
    "complete_v3": complete_record_v3,
}
configs_v3_all = {**configs_safe_v3}

configs_safe_all = {**configs_safe_v2, **configs_safe_v3}
configs_all = {**configs_v2_all, **configs_v3_all}
