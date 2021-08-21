from copy import deepcopy

from tests.resources.configs.iso19115_1_v1_standard import (
    minimal_record as _minimal_record,
    base_simple_record as _base_simple_record,
    base_complex_record as _base_complex_record,
    complete_record as _complete_record,
)

minimal_record = deepcopy(_minimal_record)  # type: dict

base_simple_record = deepcopy(_base_simple_record)  # type: dict

base_complex_record = deepcopy(_base_complex_record)  # type: dict

complete_record = deepcopy(_complete_record)  # type: dict

configs_safe = {
    "minimal": minimal_record,
    "base-simple": base_simple_record,
    "base-complex": base_complex_record,
    "complete": complete_record,
}
del configs_safe["base-simple"]["resource"]["credit"]
del configs_safe["base-complex"]["resource"]["credit"]
del configs_safe["complete"]["resource"]["credit"]
configs_all = {**configs_safe}
