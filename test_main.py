import pytest
from fastapi.testclient import TestClient
from main import app, create_access_token

client = TestClient(app)


# Fixtures pour créer un jeton d'accès et un client
@pytest.fixture
def token():
    return create_access_token(data={"sub": "user"})


@pytest.fixture
def new_client():
    return {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "zip": "12345",
            "country": "USA"
        }
    }


# Test pour l'authentification
def test_authentication():
    response = client.post("/token", data={"username": "user", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()


# Test pour créer un nouveau client
def test_create_client(token, new_client):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/clients", json=new_client, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == new_client["name"]


# Test pour obtenir tous les clients
def test_get_clients(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/clients", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Test pour obtenir un client par ID
def test_get_client_by_id(token, new_client):
    headers = {"Authorization": f"Bearer {token}"}
    create_response = client.post("/clients", json=new_client, headers=headers)
    client_id = create_response.json()["id"]

    response = client.get(f"/clients/{client_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == client_id


# Test pour mettre à jour un client
def test_update_client(token, new_client):
    headers = {"Authorization": f"Bearer {token}"}
    create_response = client.post("/clients", json=new_client, headers=headers)
    client_id = create_response.json()["id"]

    updated_client = new_client.copy()
    updated_client["name"] = "Jane Doe"

    update_response = client.put(f"/clients/{client_id}", json=updated_client, headers=headers)
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Jane Doe"


# Test pour supprimer un client
def test_delete_client(token, new_client):
    headers = {"Authorization": f"Bearer {token}"}
    create_response = client.post("/clients", json=new_client, headers=headers)
    client_id = create_response.json()["id"]

    delete_response = client.delete(f"/clients/{client_id}", headers=headers)
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Client supprimé avec succès"
