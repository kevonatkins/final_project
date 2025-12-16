import requests

def test_password_change_flow(fastapi_server, fake_user_data):
    base = fastapi_server.rstrip("/")

    # Register
    r = requests.post(f"{base}/auth/register", json={
        **fake_user_data,
        "confirm_password": fake_user_data["password"]
    })
    assert r.status_code in (200, 201), r.text

    # Login
    r = requests.post(f"{base}/auth/login", json={
    "username_or_email": fake_user_data["username"],
    "password": fake_user_data["password"]
    })

    assert r.status_code == 200, r.text
    token = r.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Change password
    new_pass = "NewPass123!"
    r = requests.put(f"{base}/users/me/password", json={
        "current_password": fake_user_data["password"],
        "new_password": new_pass,
        "confirm_new_password": new_pass
    }, headers=headers)
    assert r.status_code == 200, r.text

    # Login with new password
    r = requests.post(f"{base}/auth/login", json={
    "username_or_email": fake_user_data["username"],
    "password": new_pass
    })
    assert r.status_code == 200, r.text
