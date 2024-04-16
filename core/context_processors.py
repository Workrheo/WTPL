from settings.models import *
from authapp.models import UserProfile
from userapp.models import supportTicket

from django.conf import settings

## Settings Context Proccessor
def website_settings_context(request):
    settings = websiteSetting.objects.first()
    return {'settings': settings}

## User Profile Context Proccessor
def user_profile_context(request):
    user_profile = None
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.filter(user=request.user).first()
    return {
        'user_profile': user_profile
    }

## Ticket Context Proccessor
def unsolved_tickets_context(request):
    opened_ticket = supportTicket.objects.filter(status='open')
    return {'opened_ticket' : opened_ticket}

## Cookie Context Proccessor
def cookie_consent_processor(request):
    cookie_consent = request.COOKIES.get('cookie_consent')
    return {'cookie_consent': cookie_consent}

## Demo Mode Template Context Proccessor
def demo_mode_enabled(request):
    return {'demo_mode_enabled': 'core.middleware.middleware.DemoModeMiddleware' in settings.MIDDLEWARE}