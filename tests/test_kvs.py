import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_set_value():
    response = client.post("/kvs/set_value/", json={"key": "test_key", "value": "test_value"})
    assert response.status_code == 200
    assert response.json() == {"message": "The value is saved"}

    response = client.post("/kvs/set_value/", json={"key": "test_key", "value": "new_value"})
    assert response.status_code == 400
    assert response.json() == {'detail': 'The key already exists'}


def test_get_value():
    response = client.get("/kvs/get_value/?key=test_key")
    assert response.status_code == 200
    assert response.json() == {"value": "test_value"}
    response = client.get("/kvs/get_value/?key=non_existent_key")
    assert response.status_code == 404


def test_delete_value():
    response = client.delete("/kvs/delete_value/", params={"key": "test_key"})
    assert response.status_code == 200
    assert response.json() == {"message": "Value removed"}

    response = client.delete("/kvs/delete_value/", params={"key": "non_existent_key"})
    assert response.status_code == 404

def test_find_keys():
    response = client.get("/kvs/find_keys?value=test_value")
    assert response.status_code == 200
    assert response.json() == {"keys": ["test_key"]}

if __name__ == "__main__":
    pytest.main()