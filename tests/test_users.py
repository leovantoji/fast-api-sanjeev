import pytest
from fastapi import status
from jose import jwt

from app import schemas
from app.config import settings


def test_login(client, dummy_user):
    res = client.post(
        "/login",
        data={
            "username": dummy_user["email"],
            "password": dummy_user["password"],
        },
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )
    id = payload.get("user_id")

    assert res.status_code == status.HTTP_200_OK
    assert id == dummy_user["id"]
    assert login_res.token_type == "bearer"  # noqa: S105


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "p@ssword123", status.HTTP_403_FORBIDDEN),
        ("test@gmail.com", "wrongpassword", status.HTTP_403_FORBIDDEN),
        ("wrongemail@gmail.com", "wrongpassword", status.HTTP_403_FORBIDDEN),
        (None, "p@ssword123", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("test@gmail.com", None, status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
def test_login_error(email, password, status_code, client):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code


def test_create_user(client):
    res = client.post(
        "/users/",
        json={
            "email": "test@gmail.com",
            "password": "p@ssword123",
        },
    )

    new_user = schemas.UserOut(**res.json())
    assert res.status_code == status.HTTP_201_CREATED
    assert new_user.email == "test@gmail.com"
