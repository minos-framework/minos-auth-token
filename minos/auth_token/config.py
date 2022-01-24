from __future__ import (
    annotations,
)

import abc
import collections
import os
import typing as t
from distutils import (
    util,
)
from pathlib import (
    Path,
)

import yaml

from .exceptions import (
    TokenConfigException,
)

REST = collections.namedtuple("Rest", "host port")
DATABASE = collections.namedtuple("Database", "dbname user password host port")

_ENVIRONMENT_MAPPER = {
    "rest.host": "AUTH_TOKEN_REST_HOST",
    "rest.port": "AUTH_TOKEN_REST_PORT",
    "database.dbname": "AUTH_TOKEN_DATABASE_NAME",
    "database.user": "AUTH_TOKEN_DATABASE_USER",
    "database.password": "AUTH_TOKEN_DATABASE_PASSWORD",
    "database.host": "AUTH_TOKEN_DATABASE_HOST",
    "database.port": "AUTH_TOKEN_DATABASE_PORT",
}

_PARAMETERIZED_MAPPER = {
    "rest.host": "auth_token_rest_host",
    "rest.port": "auth_token_rest_port",
    "database.database": "auth_token_database_name",
    "database.user": "auth_token_database_user",
    "database.password": "auth_token_database_password",
    "database.host": "auth_token_database_host",
    "database.port": "auth_token_database_port",
}


class TokenConfig(abc.ABC):
    """Api Gateway config class."""

    __slots__ = ("_services", "_path", "_data", "_with_environment", "_parameterized")

    def __init__(self, path: t.Union[Path, str], with_environment: bool = True, **kwargs):
        if isinstance(path, Path):
            path = str(path)
        self._services = {}
        self._path = path
        self._load(path)
        self._with_environment = with_environment
        self._parameterized = kwargs

    @staticmethod
    def _file_exit(path: str) -> bool:
        if os.path.isfile(path):
            return True
        return False

    def _load(self, path):
        if self._file_exit(path):
            with open(path) as f:
                self._data = yaml.load(f, Loader=yaml.FullLoader)
        else:
            raise TokenConfigException(f"Check if this path: {path} is correct")

    def _get(self, key: str, **kwargs: t.Any) -> t.Any:
        if key in _PARAMETERIZED_MAPPER and _PARAMETERIZED_MAPPER[key] in self._parameterized:
            return self._parameterized[_PARAMETERIZED_MAPPER[key]]

        if self._with_environment and key in _ENVIRONMENT_MAPPER and _ENVIRONMENT_MAPPER[key] in os.environ:
            if os.environ[_ENVIRONMENT_MAPPER[key]] in ["true", "True", "false", "False"]:
                return bool(util.strtobool(os.environ[_ENVIRONMENT_MAPPER[key]]))  # pragma: no cover
            return os.environ[_ENVIRONMENT_MAPPER[key]]

        def _fn(k: str, data: dict[str, t.Any]) -> t.Any:
            current, _, following = k.partition(".")

            part = data[current]
            if not following:
                return part

            return _fn(following, part)

        return _fn(key, self._data)

    @property
    def rest(self) -> REST:
        """Get the rest config.

        :return: A ``REST`` NamedTuple instance.
        """
        return REST(host=self._get("rest.host"), port=int(self._get("rest.port")))

    @property
    def database(self) -> DATABASE:
        """Get the rest config.

        :return: A ``REST`` NamedTuple instance.
        """
        return DATABASE(
            dbname=self._get("database.dbname"),
            user=self._get("database.user"),
            password=self._get("database.password"),
            host=self._get("database.host"),
            port=int(self._get("database.port")),
        )
