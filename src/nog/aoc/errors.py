class AoCError(Exception):
    """Base exception for Advent of Code related errors."""

class AoCClientResponseError(AoCError):
    """Raised when Advent of Code returns a 4XX response."""

class AoCServerResponseError(AoCError):
    """Raised when Advent of Code returns a 5XX response."""

class NetworkError(AoCError):
    """Raised when a request to Advent of Code fails due to a network error."""

class NotLoggedInError(AoCError):
    """Raised when Advent of Code requires authentication and no valid session is available."""

class UnexpectedResponseError(AoCError):
    """Raised when Advent of Code returns an unexpected response."""
