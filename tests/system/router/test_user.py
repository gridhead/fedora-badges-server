# from fmn.api import api_models

import pytest

from .base import BaseTestAPIV1Handler


class TestUser(BaseTestAPIV1Handler):
    handler_prefix = "/users"

    async def test_select_user_by_username_not_found(self, client):
        response = await client.get(f"{self.path}/username/rules")
        assert response.status_code == 404

    async def test_select_user_by_username_found(self, client):
        response = await client.get(f"{self.path}/username/testuser")
        user = response.json().get("user")
        assert user.get("username") == "testuser"
        assert user.get("mailaddr") == "testuser@badges.test"
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "authenticate_user_username, payload, result",
        [
            (
                "testuser",
                {"username": "newuser", "mailaddr": "newuser@badges.test"},
                {
                    "status_code": 403,
                    "detail": (
                        "Access to this endpoint is now allowed for"
                        " users with inadequate access levels"
                    ),
                },
            ),
            (
                "headuser",
                {"username": "testuser", "mailaddr": "testuser@badges.test"},
                {
                    "status_code": 409,
                    "detail": "Uniqueness constraint failed - Please try again",
                },
            ),
            (
                "headuser",
                {"username": "newuser", "mailaddr": "newuser@badges.test"},
                {
                    "status_code": 201,
                },
            ),
        ],
    )
    async def test_create_user(self, client, authenticate_user, payload, result):
        post_response = await client.post(f"{self.path}/create", json=payload)

        assert post_response.status_code == result.get("status_code")
        assert post_response.json().get("detail") == result.get("detail")

        # check the new user is acutally there.
        if post_response.status_code == 201:
            response = await client.get(f"{self.path}/username/{payload.get('username')}")
            user = response.json().get("user")
            assert user.get("username") == payload.get("username")
            assert user.get("mailaddr") == payload.get("mailaddr")
            assert user.get("desc") == payload.get("desc")
