from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_user_info():
    response = client.get("/account/user/user1")
    assert response.status_code == 200
    assert response.json() == {"userID": "00001", "name": "Alice"}

def test_get_user_id_by_face():
    
    face_id = "known-face-id-1"
    response = client.get(f"/account/face/{face_id}")
    assert response.status_code == 200
    assert response.json().get("userID") == "user1"

def test_get_balance_by_currency():
    response = client.get("/account/card/user1/hkd")
    assert response.status_code == 200
    assert response.json() == {"balance": 3000.0}
