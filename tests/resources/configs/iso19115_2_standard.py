from copy import deepcopy

from tests.resources.configs.iso19115_1_standard import (
    minimal_record_v1 as _minimal_record_v1,
    base_simple_record_v1 as _base_simple_record_v1,
    base_complex_record_v1 as _base_complex_record_v1,
    complete_record_v1 as _complete_record_v1,
    minimal_record_v2 as _minimal_record_v2,
    base_simple_record_v2 as _base_simple_record_v2,
    base_complex_record_v2 as _base_complex_record_v2,
    complete_record_v2 as _complete_record_v2,
)

minimal_record_v1 = deepcopy(_minimal_record_v1)  # type: dict

base_simple_record_v1 = deepcopy(_base_simple_record_v1)  # type: dict

base_complex_record_v1 = deepcopy(_base_complex_record_v1)  # type: dict

complete_record_v1 = deepcopy(_complete_record_v1)  # type: dict

minimal_record_v2 = deepcopy(_minimal_record_v2)  # type: dict

base_simple_record_v2 = deepcopy(_base_simple_record_v2)  # type: dict

base_complex_record_v2 = deepcopy(_base_complex_record_v2)  # type: dict

complete_record_v2 = deepcopy(_complete_record_v2)  # type: dict

configs_safe_v1 = {
    "minimal_v1": minimal_record_v1,
    "base-simple_v1": base_simple_record_v1,
    "base-complex_v1": base_complex_record_v1,
    "complete_v1": complete_record_v1,
}
configs_safe_v2 = {
    "minimal_v2": minimal_record_v2,
    "base-simple_v2": base_simple_record_v2,
    "base-complex_v2": base_complex_record_v2,
    "complete_v2": complete_record_v2,
}
configs_safe_all = {**configs_safe_v1, **configs_safe_v2}

configs_v1_all = {**configs_safe_v1}
configs_v2_all = {**configs_safe_v2}
configs_all = {**configs_v1_all, **configs_v2_all}
