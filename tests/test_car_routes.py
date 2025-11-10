from http import HTTPStatus

def test_auth_required(client):
    r = client.get("/cars")
    assert r.status_code == HTTPStatus.UNAUTHORIZED

def test_create_and_get_car(client, auth_header):
    payload = {
        "make": "Toyota",
        "model": "Corolla",
        "year": 2020,
        "color": "Blue",
        "price": 15000.0,
    }
    r = client.post("/cars", headers=auth_header, json=payload)
    assert r.status_code == HTTPStatus.CREATED, r.text
    created = r.json()
    assert created["id"] == 1

    r = client.get("/cars", headers=auth_header)
    assert r.status_code == HTTPStatus.OK
    cars = r.json()
    assert len(cars) == 1

    r = client.get("/cars/1", headers=auth_header)
    assert r.status_code == HTTPStatus.OK
    car = r.json()
    assert car["make"] == "Toyota"

def test_update_and_delete(client, auth_header):
    payload = {
        "make": "Toyota",
        "model": "Corolla",
        "year": 2021,
        "color": "Black",
        "price": 16000.0,
    }
    r = client.put("/cars/1", headers=auth_header, json=payload)
    assert r.status_code == HTTPStatus.OK
    updated = r.json()
    assert updated["year"] == 2021

    r = client.delete("/cars/1", headers=auth_header)
    assert r.status_code == HTTPStatus.NO_CONTENT

    r = client.get("/cars/1", headers=auth_header)
    assert r.status_code == HTTPStatus.NOT_FOUND
