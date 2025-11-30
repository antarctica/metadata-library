from copy import deepcopy

minimal_record = {"$schema": "#", "resource": {"title": {"value": "Test Record"}}}

typical_record = deepcopy(minimal_record)
typical_record["resource"]["title"]["href"] = "https://www.example.com"

complete_record = deepcopy(typical_record)
complete_record["resource"]["title"]["title"] = "Test Record"

record_with_entities = deepcopy(minimal_record)
record_with_entities["resource"]["title"]["value"] = (
    "Test Record with entities: '>' (greater than), 'å' (accent [a-ring]) and 'µ' (micro)"
)

configs_all = {
    "minimal": minimal_record,
    "entities": record_with_entities,
    "complete": complete_record,
    "typical": typical_record,
}
