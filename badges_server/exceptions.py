class BadgesServerException(Exception):
    """Custom exceptions for Badges Server."""


class BadgesServerConfigurationError(BadgesServerException):
    """Something is wrong with the configuration of Badges Server."""


class BadgesServerShellUnavailableError(BadgesServerException):
    """Selected interactive shell type is not available."""
