import logging

from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from packaging.utils import _
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponseRedirect

from authentication.forms import CustomLoginForm

logger = logging.getLogger()

def logout(request):
    """Logout Post request """
    from django.contrib.auth import logout as auth_logout
    auth_logout(request)
    from django.shortcuts import redirect
    return redirect('auth:login')

# Perform login
@require_http_methods(["GET", "POST", "HEAD"])
def login(request):
    """
    Handle the login logic.
    """
    form = CustomLoginForm(data=request.POST or None)
    if request.method == 'POST':
        logger.info('Processing login form submission')
        if form.is_valid():
            logger.info('Form is valid, authenticating user')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'))
            else:
                logger.warning('Invalid login credentials')
                form.add_error('username', _('Invalid username or password.'))
        else:
            form.add_error('username', _('Invalid username or password.'))
    return render(request, 'authentication/login.html', {'form': form})