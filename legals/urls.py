from django.urls import path
from legals.views import *

urlpatterns = [
    
    # Agreement Front URLS
    
    path('admin/crm/agreement-settings/', settingsView, name='settingsView'),
]
