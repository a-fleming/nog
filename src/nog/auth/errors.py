class AuthError(Exception):
    """Base exception for nog authentication failures."""

class BrowserLoginError(AuthError):
    """Raised when browser-assisted login fails unexpectedly."""

class LoginCancelled(AuthError):
    """Raised when the user cancels browser-assisted login."""

class SessionCookieNotFound(AuthError):
    """Raised when no usable Advent of Code session cookie is found."""