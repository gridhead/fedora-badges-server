# from fmn.api import api_models

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
