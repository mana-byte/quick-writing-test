import re
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.backend.api import app, addPerformanceRequest

client = TestClient(app)


def test_get_all_performance():
    response = client.get("/api/all_performance")
    assert response.status_code == 200
    # Assuming the response is a list of performance records
    data = response.json()
    assert isinstance(data, list)
    if data:  # If there are any performance records
        record = data[0]
        assert "id" in record
        assert "name" in record
        assert "time_taken" in record


def test_add_remove_performance():
    response = client.post(
        "/api/add_performance",
        json={
            "name": "ToRemove",
            "time_taken": 1234,
        },
    )
    id = response.json().get("id")
    assert response.status_code == 201
    assert response.json() == {"id": id, "name": "ToRemove", "time_taken": 1234}
    response_ = client.delete(f"api/remove_performance/{id}")
    assert response_.status_code == 200
    response_ = client.delete("api/remove_performance/-1")
    assert response_.status_code == 404


def test_update_Performance():
    response = client.post(
        "/api/add_performance",
        json={
            "name": "ToUpdate",
            "time_taken": 1234,
        },
    )
    id = response.json().get("id")
    assert response.status_code == 201
    assert response.json() == {"id": id, "name": "ToUpdate", "time_taken": 1234}
    response_ = client.put(
        f"/api/update_performance/{id}",
        json={
            "name": "UpdatedName",
            "time_taken": 4321,
        },
    )
    assert response_.status_code == 200
    assert response_.json() == {"id": id, "name": "UpdatedName", "time_taken": 4321}
    response_ = client.put(
        "/api/update_performance/-1",
        json={
            "name": "Nope",
            "time_taken": 1111,
        },
    )
    assert response_.status_code == 404
    response_ = client.delete(f"api/remove_performance/{id}")
    assert response_.status_code == 200
