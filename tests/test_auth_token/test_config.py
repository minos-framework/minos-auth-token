"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
import os
import unittest
from unittest import (
    mock,
)

from minos.auth_token import (
    TokenConfig,
    TokenConfigException,
)
from tests.utils import (
    BASE_PATH,
)


class TestApiGatewayConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.config_file_path = BASE_PATH / "config.yml"

    def test_config_ini_fail(self):
        with self.assertRaises(TokenConfigException):
            TokenConfig(path=BASE_PATH / "test_fail_config.yaml")

    def test_config_rest(self):
        config = TokenConfig(path=self.config_file_path)
        rest = config.rest

        self.assertEqual("localhost", rest.host)
        self.assertEqual(5569, rest.port)

    def test_overwrite_with_parameter_rest_host(self):
        config = TokenConfig(path=self.config_file_path, auth_token_rest_host="::1")
        rest = config.rest
        self.assertEqual("::1", rest.host)

    def test_config_database(self):
        config = TokenConfig(path=self.config_file_path)
        database = config.database

        self.assertEqual("token_db", database.dbname)
        self.assertEqual("minos", database.user)
        self.assertEqual("min0s", database.password)
        self.assertEqual(5432, database.port)

    @mock.patch.dict(os.environ, {"AUTH_TOKEN_REST_HOST": "::1"})
    def test_overwrite_with_environment_rest_host(self):
        config = TokenConfig(path=self.config_file_path)
        self.assertEqual("::1", config.rest.host)

    @mock.patch.dict(os.environ, {"AUTH_TOKEN_REST_PORT": "4040"})
    def test_overwrite_with_environment_rest_port(self):
        config = TokenConfig(path=self.config_file_path)
        self.assertEqual(4040, config.rest.port)

    @mock.patch.dict(os.environ, {"AUTH_TOKEN_DATABASE_NAME": "db_test_name"})
    def test_overwrite_with_environment_database_name(self):
        config = TokenConfig(path=self.config_file_path)
        self.assertEqual("db_test_name", config.database.dbname)

    @mock.patch.dict(os.environ, {"AUTH_TOKEN_DATABASE_USER": "test_user"})
    def test_overwrite_with_environment_database_user(self):
        config = TokenConfig(path=self.config_file_path)
        self.assertEqual("test_user", config.database.user)

    @mock.patch.dict(os.environ, {"AUTH_TOKEN_DATABASE_PASSWORD": "some_pass"})
    def test_overwrite_with_environment_database_password(self):
        config = TokenConfig(path=self.config_file_path)
        self.assertEqual("some_pass", config.database.password)

    @mock.patch.dict(os.environ, {"AUTH_TOKEN_DATABASE_HOST": "localhost.com"})
    def test_overwrite_with_environment_database_host(self):
        config = TokenConfig(path=self.config_file_path)
        self.assertEqual("localhost.com", config.database.host)

    @mock.patch.dict(os.environ, {"AUTH_TOKEN_DATABASE_PORT": "2020"})
    def test_overwrite_with_environment_database_port(self):
        config = TokenConfig(path=self.config_file_path)
        self.assertEqual(2020, config.database.port)


if __name__ == "__main__":
    unittest.main()
