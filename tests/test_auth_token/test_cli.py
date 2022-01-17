import unittest
from unittest.mock import (
    patch,
)

from typer.testing import (
    CliRunner,
)

from minos.auth_token.cli import app as cli_app

runner = CliRunner()

class TestCli(unittest.TestCase):
    def test_app(self):
        raise NotImplementedError

if __name__ == "__main__":
    unittest.main()
