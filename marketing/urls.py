from django.urls import path
from marketing.views import *

urlpatterns = [
    path('admin/crm/marketing/email-marketing/', emailMarketing, name='emailMarketing'),
    path('admin/crm/marketing/email-formator/', emailFormator, name='emailFormator'),
    
    path('admin/crm/marketing/sms-marketing/', smsMarketing, name='smsMarketing'),
    path('admin/crm/marketing/number-formator/', numberFormator, name='numberFormator'),
]
