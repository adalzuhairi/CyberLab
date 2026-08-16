from fastapi.testclient import TestClient

def test_read_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "application" in data
    assert data["status"] == "running"

def test_create_asset(client: TestClient):
    response = client.post(
        "/assets/",
        json={
            "hostname": "PC-TEST-01",
            "type": "Laptop",
            "manufacturer": "Lenovo",
            "model": "ThinkPad T14",
            "user": "Alice",
            "ip": "192.168.1.100"
        },
    )
    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    assert data["hostname"] == "PC-TEST-01"
    assert "id" in data

def test_read_assets(client: TestClient):
    # On crée d'abord un élément
    client.post(
        "/assets/",
        json={
            "hostname": "PC-TEST-02",
            "type": "Desktop",
            "manufacturer": "HP",
            "model": "ProDesk",
            "user": "Bob",
            "ip": "192.168.1.101"
        },
    )
    response = client.get("/assets/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_read_asset_by_id(client: TestClient):
    # Création
    create_res = client.post(
        "/assets/",
        json={
            "hostname": "PC-TEST-03",
            "type": "Server",
            "manufacturer": "Dell",
            "model": "PowerEdge",
            "user": "Admin",
            "ip": "192.168.1.102"
        },
    )
    asset_id = create_res.json()["id"]

    # Lecture par ID
    response = client.get(f"/assets/{asset_id}")
    assert response.status_code == 200
    assert response.json()["hostname"] == "PC-TEST-03"

def test_update_asset(client: TestClient):
    # Création
    create_res = client.post(
        "/assets/",
        json={
            "hostname": "PC-TEST-04",
            "type": "Laptop",
            "manufacturer": "Apple",
            "model": "MacBook Pro",
            "user": "Charlie",
            "ip": "192.168.1.103"
        },
    )
    asset_id = create_res.json()["id"]

    # Mise à jour
    update_res = client.put(
        f"/assets/{asset_id}",
        json={
            "hostname": "PC-TEST-04-UPDATED",
            "type": "Laptop",
            "manufacturer": "Apple",
            "model": "MacBook Pro M3",
            "user": "Charlie Updated",
            "ip": "192.168.1.103"
        },
    )
    assert update_res.status_code == 200
    assert update_res.json()["hostname"] == "PC-TEST-04-UPDATED"

def test_delete_asset(client: TestClient):
    # Création
    create_res = client.post(
        "/assets/",
        json={
            "hostname": "PC-TEST-05",
            "type": "Tablet",
            "manufacturer": "Samsung",
            "model": "Galaxy Tab",
            "user": "David",
            "ip": "192.168.1.104"
        },
    )
    asset_id = create_res.json()["id"]

    # Suppression
    delete_res = client.delete(f"/assets/{asset_id}")
    assert delete_res.status_code == 200

    # Vérification que l'élément n'existe plus (doit renvoyer une 404)
    get_res = client.get(f"/assets/{asset_id}")
    assert get_res.status_code == 404
