from django.contrib import admin
from settings.models import *

@admin.register(websiteSetting)
class WebsiteSettingAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'email_address']
    
admin.site.register(paymentMethod)

