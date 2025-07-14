from django.urls import reverse

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

def navigation_menu(request):
    menu = [
        {"label": "Dashboard", "url": "/", "icon": "fas fa-dashboard", "sort": 1},
        {"label": "Layouts", "icon": "fa-solid fas fa-layer-group", "sort": 2, "children": [
            {"label": "Stacked", "url": "/layouts/stacked/",  "sort": 1,},
            {"label": "Sidebar", "url": "/layouts/sidebar/",  "sort": 2,},
        ]},
        # Add more items as needed...
    ]
    if not request.user.is_authenticated:
        menu.append({"label": "Login", "url": reverse('auth:login'), "fas fa-login": "login", "sort": 100})
        # menu.append({"label": "Register", "url": "/register/", "icon": "register",  "sort": 101,})
    if request.user.is_superuser:
        menu.append({"label": "Admin", "url": "/admin/", "icon": "fas fa-user", "sort": 200})

    # Determine the active menu item based on the request path
    active_path = request.path.strip('/')
    for item in menu:
        if 'url' in item and item['url'].strip('/') == active_path:
            item['active'] = True
        elif 'children' in item:
            for child in item['children']:
                if child["url"].strip('/') == active_path:
                    child['active'] = True
                    item['active'] = True
    # Set the first item as active if no other item is active
    if not any('active' in item for item in menu):
        if menu:
            menu[0]['active'] = True
    # Ensure the menu is sorted by label
    return {"navigation_menu": menu}