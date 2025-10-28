from .utils import *
from ..routers.owner import get_db, get_current_owner
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_owner] = override_get_current_owner


def test_return_owner(test_owner):
    response = client.get("/owner")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "codingwithrobytest"
    assert response.json()["email"] == "codingwithrobytest@email.com"
    assert response.json()["first_name"] == "Eric"
    assert response.json()["last_name"] == "Roby"
    assert response.json()["role"] == "admin"
    assert response.json()["phone_number"] == "(111)-111-1111"


def test_change_password_success(test_owner):
    response = client.put(
        "/owner/password",
        json={"password": "testpassword", "new_password": "newpassword"},
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_owner):
    response = client.put(
        "/owner/password",
        json={"password": "wrong_password", "new_password": "newpassword"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password change"}


def test_change_phone_number_success(test_owner):
    response = client.put("/owner/phonenumber/2222222222")
    assert response.status_code == status.HTTP_204_NO_CONTENT
