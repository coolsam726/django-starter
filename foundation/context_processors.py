from .utils import  env
def global_variables(request):
    """
    Context processor to add global variables to the template context.
    """
    return {
        'app_name': env('APP_NAME', 'My Django App'),
        'app_tagline': env('APP_TAGLINE', 'A Django application'),
        'version': '1.0.0',
        'author': 'Sam Maosa',
    }