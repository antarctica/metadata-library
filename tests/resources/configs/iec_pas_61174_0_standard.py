minimal_record_v1 = {
    "$schema": "https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iec-pas-61174-0-v1.json",
    "route_name": "minimal-test-route",
    "waypoints": [
        {"id": 1001, "revision": 0, "position": {"lat": 5.5, "lon": 50.55}},
        {"id": 1002, "revision": 0, "position": {"lat": 5.5, "lon": 50.55}},
        {"id": 1003, "revision": 0, "position": {"lat": 5.5, "lon": 50.55}},
    ],
}

complete_record_v1 = {
    "$schema": "https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iec-pas-61174-0-v1.json",
    "route_author": "Constance Watson",
    "route_name": "complete-test-route",
    "route_status": "complete",
    "waypoints": [
        {"id": 1001, "revision": 0, "position": {"lat": 5.5, "lon": 50.55}, "leg": {"geometry_type": "Orthodrome"}},
        {"id": 1002, "revision": 0, "position": {"lat": 5.5, "lon": 50.55}, "leg": {"geometry_type": "Orthodrome"}},
        {"id": 1003, "revision": 0, "position": {"lat": 5.5, "lon": 50.55}, "leg": {"geometry_type": "Orthodrome"}},
    ],
}

configs_v1 = {"minimal_v1": minimal_record_v1, "complete_v1": complete_record_v1}
configs_all = {**configs_v1}
