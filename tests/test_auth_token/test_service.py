"""tests.test_api_gateway.test_rest.service module."""

import json
import unittest

from aiohttp.test_utils import (
    AioHTTPTestCase,
)

from minos.auth_token import (
    TokenConfig,
    TokenRestService,
)
from tests.utils import (
    BASE_PATH,
)


class TestCredentialRestService(AioHTTPTestCase):
    CONFIG_FILE_PATH = BASE_PATH / "config.yml"

    def setUp(self) -> None:
        self.config = TokenConfig(self.CONFIG_FILE_PATH)
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """
        rest_service = TokenRestService(address=self.config.rest.host, port=self.config.rest.port, config=self.config)

        return await rest_service.create_application()

    async def test_create_token(self):
        url = "/token"
        response = await self.client.request("POST", url)

        self.assertEqual(200, response.status)
        self.assertIn("token", await response.text())

    async def test_validate_token(self):
        url = "/token"
        response = await self.client.request("POST", url)

        self.assertEqual(200, response.status)
        self.assertIn("token", await response.text())

        content = await response.json()
        url = "/token/validate"

        response = await self.client.request("POST", url, data=json.dumps(content))

        self.assertEqual(200, response.status)
        self.assertEqual("Token valid.", await response.text())

    async def test_validate_token_no_data_passed(self):
        url = "/token/validate"
        response = await self.client.request("POST", url)

        self.assertEqual(400, response.status)
        self.assertIn("Wrong data. Provide token.", await response.text())

    async def test_validate_token_wrong_data_passed(self):
        url = "/token/validate"
        response = await self.client.request("POST", url, data=json.dumps({"abc": "test"}))

        self.assertEqual(400, response.status)
        self.assertIn("Wrong data. Provide token.", await response.text())

    async def test_validate_token_wrong(self):
        url = "/token/validate"
        response = await self.client.request("POST", url, data=json.dumps({"token": "test"}))

        self.assertEqual(400, response.status)
        self.assertIn("Token invalid.", await response.text())

    async def test_refresh_token(self):
        url = "/token"
        response = await self.client.request("POST", url)

        self.assertEqual(200, response.status)
        self.assertIn("token", await response.text())

        content = await response.json()
        url = "/token/refresh"

        response = await self.client.request("POST", url, data=json.dumps(content))

        self.assertEqual(200, response.status)
        self.assertIn("token", await response.text())

    async def test_refresh_token_no_data_passed(self):
        url = "/token/refresh"
        response = await self.client.request("POST", url)

        self.assertEqual(400, response.status)
        self.assertIn("Wrong data. Provide token.", await response.text())

    async def test_refresh_token_wrong_data_passed(self):
        url = "/token/refresh"
        response = await self.client.request("POST", url, data=json.dumps({"abc": "test"}))

        self.assertEqual(400, response.status)
        self.assertIn("Wrong data. Provide token.", await response.text())

    async def test_refresh_token_wrong(self):
        url = "/token/refresh"
        response = await self.client.request("POST", url, data=json.dumps({"token": "test"}))

        self.assertEqual(400, response.status)
        self.assertEqual("Token not found. Provide correct token.", await response.text())


if __name__ == "__main__":
    unittest.main()
