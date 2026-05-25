"""
pytest tests — verify insert/retrieve through the Flask server (via DB).
These run against an in-memory SQLite DB so no MySQL is needed in CI.
"""
import json


# ── Guest CRUD ────────────────────────────────────────────────────────────────

def test_create_guest(client):
    resp = client.post("/api/guests", json={
        "name": "ישראל ישראלי",
        "phone": "+972501234567",
        "group_name": "family",
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["name"] == "ישראל ישראלי"
    assert data["phone"] == "+972501234567"
    assert data["id"] is not None


def test_insert_and_retrieve_guest_from_db(client):
    """Core test: insert guest → retrieve it back → verify data integrity."""
    # Insert via server
    client.post("/api/guests", json={
        "name": "שרה כהן",
        "phone": "+972521111111",
        "group_name": "friends",
        "notes": "חברה טובה",
    })

    # Retrieve via server
    resp = client.get("/api/guests")
    assert resp.status_code == 200
    guests = resp.get_json()
    assert len(guests) == 1
    assert guests[0]["name"] == "שרה כהן"
    assert guests[0]["phone"] == "+972521111111"
    assert guests[0]["group_name"] == "friends"


def test_get_guest_by_id(client):
    create = client.post("/api/guests", json={
        "name": "דוד לוי",
        "phone": "+972509999999",
        "group_name": "work",
    })
    guest_id = create.get_json()["id"]

    resp = client.get(f"/api/guests/{guest_id}")
    assert resp.status_code == 200
    assert resp.get_json()["name"] == "דוד לוי"


def test_update_guest(client):
    create = client.post("/api/guests", json={
        "name": "מיכל גולן",
        "phone": "+972508888888",
        "group_name": "friends",
    })
    guest_id = create.get_json()["id"]

    resp = client.put(f"/api/guests/{guest_id}", json={"name": "מיכל גולן-כץ"})
    assert resp.status_code == 200
    assert resp.get_json()["name"] == "מיכל גולן-כץ"


def test_delete_guest(client):
    create = client.post("/api/guests", json={
        "name": "לזחוק",
        "phone": "+972500000001",
        "group_name": "friends",
    })
    guest_id = create.get_json()["id"]

    del_resp = client.delete(f"/api/guests/{guest_id}")
    assert del_resp.status_code == 200

    # Should be gone
    resp = client.get("/api/guests")
    assert all(g["id"] != guest_id for g in resp.get_json())


def test_filter_guests_by_group(client):
    client.post("/api/guests", json={"name": "א", "phone": "+972501", "group_name": "family"})
    client.post("/api/guests", json={"name": "ב", "phone": "+972502", "group_name": "friends"})

    resp = client.get("/api/guests?group=family")
    guests = resp.get_json()
    assert all(g["group_name"] == "family" for g in guests)


# ── Event ─────────────────────────────────────────────────────────────────────

def test_create_and_retrieve_event(client):
    resp = client.put("/api/event", json={
        "bride_name": "רות",
        "groom_name": "אברהם",
        "wedding_date": "2025-12-20T19:00",
        "venue": "אולם הזהב",
        "venue_address": "תל אביב",
        "reminder_days_before": 7,
    })
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["bride_name"] == "רות"
    assert data["groom_name"] == "אברהם"

    # Retrieve
    get_resp = client.get("/api/event")
    assert get_resp.status_code == 200
    assert get_resp.get_json()["venue"] == "אולם הזהב"


# ── Health ────────────────────────────────────────────────────────────────────

def test_health_endpoint(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"
