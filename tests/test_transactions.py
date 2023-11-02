import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_begin_transaction():
    response = client.post("/transactions/begin/", cookies={"user": "test_user"})
    assert response.status_code == 200
    assert response.json() == {"message": "Transaction opened"}

    response = client.post("/transactions/begin/")
    assert response.status_code == 401


def test_rollback_transaction():
    client.post("/transactions/begin/", cookies={"user": "test_user"})
    response = client.post("/transactions/rollback/", cookies={"user": "test_user"})
    assert response.status_code == 200
    assert response.json() == {"message": "Last transaction canceled"}


def test_commit_transaction():
    client.post("/transactions/begin/", cookies={"user": "test_user"})
    response = client.post("/transactions/commit/", cookies={"user": "test_user"})
    assert response.status_code == 200
    assert response.json() == "Commit complete"

    response = client.post("/transactions/commit/", cookies={"user": "test_user"})
    assert response.status_code == 400


def test_read_only_during_transaction():
    client.post("/transactions/begin/", cookies={"user": "test_user"})
    response = client.post("/kvs/set_value/", json={"key": "test_key", "value": "new_value"},
                           cookies={"user": "test_user1"})
    assert response.status_code == 400
    assert response.json() == {"detail": "The data is read-only. Transaction opened"}


if __name__ == "__main__":
    pytest.main()
