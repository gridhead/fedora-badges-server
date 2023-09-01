# from fmn.api import api_models

from unittest import mock
from uuid import UUID

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
        "theuuid, result",
        [
            pytest.param(
                "bobateee",
                {
                    "status_code": 404,
                    "detail": "User with the requested UUID 'bobateee' was not found",
                },
                id="Invalid UUID hex value that also doesnt exist",
            ),
            pytest.param(
                "bobaboba",
                {
                    "status_code": 404,
                    "detail": "User with the requested UUID 'bobaboba' was not found",
                },
                id="Valid UUID hex value that also doesnt exist in the DB",
            ),
            pytest.param(
                "aaaaaaaa",
                {
                    "status_code": 200,
                    "user": {"username": "testuser", "mailaddr": "testuser@badges.test"},
                },
                id="a UUID hex value that actually is a user in the DB",
            ),
        ],
    )
    async def test_select_user_by_uuid(self, client, theuuid, result):
        response = await client.get(f"{self.path}/uuid/{theuuid}")

        assert response.status_code == result.get("status_code")
        assert response.json().get("detail") == result.get("detail")
        if result.get("user"):
            assert result.get("user").items() <= response.json().get("user").items()

    @pytest.mark.parametrize(
        "authenticate_user_username, payload, result",
        [
            pytest.param(
                "headuser",
                {
                    "username": "newuser",
                    "mailaddr": "newuser@badges.test",
                    "desc": "a user description",
                },
                {
                    "status_code": 201,
                },
                id="Actual valid user creation",
            ),
            pytest.param(
                "testuser",
                {"username": "newuser", "mailaddr": "newuser@badges.test"},
                {
                    "status_code": 403,
                    "detail": (
                        "Access to this endpoint is now allowed for"
                        " users with inadequate access levels"
                    ),
                },
                id="Try to create a new user with a user that is not a headuser",
            ),
            pytest.param(
                "headuser",
                {"username": "testuser", "mailaddr": "testuser@badges.test"},
                {
                    "status_code": 409,
                    "detail": "Uniqueness constraint failed - Please try again",
                },
                id="Try to create a new user with a username that already exists",
            ),
            pytest.param(
                "headuser",
                {},
                {
                    "status_code": 422,
                    "detail": [
                        {
                            "loc": ["body", "mailaddr"],
                            "msg": "field required",
                            "type": "value_error.missing",
                        },
                        {
                            "loc": ["body", "username"],
                            "msg": "field required",
                            "type": "value_error.missing",
                        },
                    ],
                },
                id="Try to create a user with invalid parameters",
            ),
            pytest.param(
                "headuser",
                {
                    "UZERNAM": "asdfsadf",
                    "username": "newuser",
                    "mailaddr": "newuser@badges.test",
                },
                {
                    "status_code": 201,
                },
                id="Create a user, but send some junky parameters this should still work tho",
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

    @pytest.mark.parametrize("authenticate_user_username", ["headuser"])
    @mock.patch("badges_server.system.router.user.uuid4")
    async def test_create_user_made_access_uniqueness(self, mock_uuid, client, authenticate_user):
        mock_uuid.side_effect = (
            UUID(hex="0" * 32),
            UUID(hex="f72d0cec666445308e6b2e1df02f240d"),
            UUID(hex="1" * 32),
            UUID(hex="2" * 32),
            UUID(hex="f72d0cec666445308e6b2e1df02f240d"),
            UUID(hex="3" * 32),
        )
        post_response1 = await client.post(
            f"{self.path}/create", json={"username": "newuser", "mailaddr": "newuser@badges.test"}
        )
        post_response2 = await client.post(
            f"{self.path}/create", json={"username": "newuser2", "mailaddr": "newuser2@badges.test"}
        )

        # first user should cbe created
        assert post_response1.status_code == 201

        # second user should not be created becuase the Access code property is the same
        assert post_response2.status_code == 409
        assert (
            post_response2.json().get("detail") == "Uniqueness constraint failed - Please try again"
        )

    @pytest.mark.parametrize(
        "authenticate_user_username, payload, result",
        [
            pytest.param(
                "headuser",
                {"uuid": "aaaaaaaa", "head": "true"},  # the uuid of testuser
                {
                    "status_code": 200,
                    "user": {
                        "username": "testuser",
                        "mailaddr": "testuser@badges.test",
                        "headuser": True,
                    },
                },
                id="change testuser's permission to headuser=true",
            ),
            pytest.param(
                "headuser",
                {"uuid": "bbbbbbbb", "head": "false"},  # the uuid of headuser
                {
                    "status_code": 200,
                    "user": {
                        "username": "headuser",
                        "mailaddr": "headuser@badges.test",
                        "headuser": False,
                    },
                },
                id="change headuser's permission to headuser=false",
            ),
            pytest.param(
                "testuser",
                {"uuid": "aaaaaaaa", "head": "true"},  # the uuid of testuser
                {
                    "status_code": 403,
                    "detail": (
                        "Access to this endpoint is now allowed for users with inadequate "
                        "access levels"
                    ),
                },
                id="try to change a permission with a non-headuser user",
            ),
            pytest.param(
                "headuser",
                {"uuid": "bobaboba", "head": "true"},
                {
                    "status_code": 404,
                    "detail": "User with the requested UUID 'bobaboba' was not found",
                },
                id="try to change a permission with unknown UUID",
            ),
            pytest.param(
                "headuser",
                {"uuid": "cccccccc", "head": "true"},  # UUID of testuser_withdrawn
                {
                    "status_code": 422,
                    "detail": (
                        "User with the requested UUID 'cccccccc' have withdrawn "
                        "from the service so their access levels cannot be modified"
                    ),
                },
                id="try to change permission of a withdrawn user",
            ),
            pytest.param(
                "headuser",
                {"uuid": "bbbbbbbb", "head": "true"},  # UUID of headuser
                {
                    "status_code": 422,
                    "detail": (
                        (
                            "User with the requested UUID 'bbbbbbbb' already have the ADMIN access "
                            "levels"
                        )
                    ),
                },
                id="try to change permission of headuser to head=true",
            ),
            pytest.param(
                "headuser",
                {"uuid": "aaaaaaaa", "head": "false"},  # UUID of testuser
                {
                    "status_code": 422,
                    "detail": (
                        "User with the requested UUID 'aaaaaaaa' does not have ADMIN access levels"
                    ),
                },
                id="try to change permission of testuser to head=false",
            ),
        ],
    )
    async def test_update_permisson(self, client, authenticate_user, payload, result):
        response = await client.put(f"{self.path}/updateperm", json=payload)

        assert response.status_code == result.get("status_code")

        assert response.json().get("detail") == result.get("detail")
        if result.get("user"):
            assert result.get("user").items() <= response.json().get("user").items()

    @pytest.mark.parametrize(
        "authenticate_user_username, payload, result",
        [
            pytest.param(
                "headuser",
                {"uuid": "aaaaaaaa", "withdraw": "true"},  # the uuid of testuser
                {
                    "status_code": 200,
                    "user": {
                        "username": "testuser",
                        "mailaddr": "testuser@badges.test",
                        "withdraw": True,
                    },
                },
                id="change testuser's activity to withdraw=true",
            ),
            pytest.param(
                "headuser",
                {"uuid": "cccccccc", "withdraw": "false"},  # the uuid of testuser_withdrawn
                {
                    "status_code": 200,
                    "user": {
                        "username": "testuser_withdrawn",
                        "mailaddr": "testuser_withdrawn@badges.test",
                        "withdraw": False,
                    },
                },
                id="change testuser_withdrawn's activity to withdraw=false",
            ),
            pytest.param(
                "testuser",
                {"uuid": "aaaaaaaa", "withdraw": "true"},  # the uuid of testuser
                {
                    "status_code": 403,
                    "detail": (
                        "Access to this endpoint is now allowed for users with inadequate "
                        "access levels"
                    ),
                },
                id="try to change a the activity with a non-headuser user",
            ),
            pytest.param(
                "headuser",
                {"uuid": "bobaboba", "withdraw": "true"},
                {
                    "status_code": 404,
                    "detail": "User with the requested UUID 'bobaboba' was not found",
                },
                id="try to change a permission with unknown UUID",
            ),
            pytest.param(
                "headuser",
                {"uuid": "cccccccc", "withdraw": "true"},  # UUID of testuser_withdrawn
                {
                    "status_code": 422,
                    "detail": (
                        "User with the requested UUID 'cccccccc' "
                        "have already withdrawn from the service"
                    ),
                },
                id="try to withdraw of a withdrawn user",
            ),
            pytest.param(
                "headuser",
                {"uuid": "bbbbbbbb", "withdraw": "false"},  # UUID of headuser
                {
                    "status_code": 422,
                    "detail": (
                        (
                            "User with the requested UUID 'bbbbbbbb' "
                            "have already enabled their account"
                        )
                    ),
                },
                id="try to change enable a user that is already enabled",
            ),
        ],
    )
    async def test_update_activity(self, client, authenticate_user, payload, result):
        response = await client.put(f"{self.path}/updateactivity", json=payload)

        assert response.status_code == result.get("status_code")

        assert response.json().get("detail") == result.get("detail")
        if result.get("user"):
            assert result.get("user").items() <= response.json().get("user").items()
