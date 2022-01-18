class TokenConfigException(Exception):
    """Base Api Gateway Exception."""


class NoTokenException(TokenConfigException):
    """Exception to be raised when token is not available."""


class ApiGatewayConfigException(TokenConfigException):
    """Base config exception."""
