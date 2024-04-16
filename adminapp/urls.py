from django.urls import path
from adminapp.views import *
from settings.views import *

urlpatterns = [

    # Admin Agreement Submissions
    path('admin/agreement/submissions/', agreementSubmissonsAdmin, name='agreementSubmissonsAdmin'),
    path('admin/agreement/delete/<int:id>', agreementDeleteAdmin, name='agreementDeleteAdmin'),
    path('admin/agreement/view/<int:id>', agreementDetailAdmin, name='agreementDetailAdmin'),
    
    # Admin Settings
    path('admin/crm/settings/system-settings/', adminWebsiteSettings, name='websiteSettingsadm'),
     path('admin/crm/settings/openai-settings/', adminOpenaiSettings, name='adminOpenaiSettings'),
    path('admin/crm/settings/payment-methods/', adminPaymentMethodsSettings, name='adminPaymentMethodsSettings'),
]