minimal_record_v1 = {
    "route_name": "minimal-test-route",
    "waypoints": [
        {"id": 1001, "revision": 0, "position": {"lat": 5, "lon": 50}},
        {"id": 1002, "revision": 0, "position": {"lat": 5, "lon": 50}},
        {"id": 1003, "revision": 0, "position": {"lat": 5, "lon": 50}},
    ],
}

complete_record_v1 = {
    "route_author": "Constance Watson",
    "route_name": "complete-test-route",
    "route_status": "complete",
    "waypoints": [
        {"id": 1001, "revision": 0, "position": {"lat": 5, "lon": 50}},
        {"id": 1002, "revision": 0, "position": {"lat": 5, "lon": 50}},
        {"id": 1003, "revision": 0, "position": {"lat": 5, "lon": 50}},
    ],
}

configs_v1 = {"minimal_v1": minimal_record_v1, "complete_v1": complete_record_v1}
configs_all = {**configs_v1}
