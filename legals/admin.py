from django.contrib import admin
from legals.models import *

    
# Agreement
@admin.register(agreement)
class agreementAdmin(admin.ModelAdmin):
    list_display = ['service', 'client', 'name', 'email', 'is_signed' , 'is_approved']

admin.site.register(agreementSettings)