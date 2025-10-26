from .utils import *
from ..routers.auth import (
    get_db,
    authenticate_owner,
    create_access_token,
    SECRET_KEY,
    ALGORITHM,
    get_current_owner,
)
from jose import jwt
from datetime import timedelta
import pytest
from fastapi import HTTPException

app.dependency_overrides[get_db] = override_get_db


def test_authenticate_owner(test_owner):
    db = TestingSessionLocal()

    authenticated_owner = authenticate_owner(test_owner.username, "testpassword", db)
    assert authenticated_owner is not None
    assert authenticated_owner.username == test_owner.username

    non_existent_owner = authenticate_owner("WrongOwnerName", "testpassword", db)
    assert non_existent_owner is False

    wrong_password_owner = authenticate_owner(test_owner.username, "wrongpassword", db)
    assert wrong_password_owner is False


def test_create_access_token():
    username = "testowner"
    owner_id = 1
    role = "owner"
    expires_delta = timedelta(days=1)

    token = create_access_token(username, owner_id, role, expires_delta)

    decoded_token = jwt.decode(
        token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False}
    )

    assert decoded_token["sub"] == username
    assert decoded_token["id"] == owner_id
    assert decoded_token["role"] == role


@pytest.mark.asyncio
async def test_get_current_owner_valid_token():
    encode = {"sub": "testowner", "id": 1, "role": "admin"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    owner = await get_current_owner(token=token)
    assert owner == {"username": "testowner", "id": 1, "owner_role": "admin"}


@pytest.mark.asyncio
async def test_get_current_owner_missing_payload():
    encode = {"role": "owner"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_owner(token=token)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate owner."
