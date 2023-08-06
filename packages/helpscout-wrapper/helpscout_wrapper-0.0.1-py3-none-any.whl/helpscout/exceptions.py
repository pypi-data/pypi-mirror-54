class BadRequestException(Exception):
    """Raise if the request doesn’t meet all requirements."""


class NotAuthorizedException(Exception):
    """OAuth2 token is either not provided or not valid."""
