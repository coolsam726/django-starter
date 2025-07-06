from .threadinglocals import set_current_user

class CurrentUserMiddleware:
    """
    Middleware to set the current user in thread-local storage.
    This allows access to the current user in other parts of the application.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Set the current user in thread-local storage
        set_current_user(request.user)

        # Call the next middleware or view
        response = self.get_response(request)

        return response