import threading

_user = threading.local()

def set_current_user(user):
    """Set the current user in the thread-local storage."""
    _user.value = user

def get_current_user():
    """Get the current user from the thread-local storage."""
    return getattr(_user, 'value', None)