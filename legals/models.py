from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from crm.models import crmServices
from settings.models import websiteSetting
        
# Agreement
class agreement(models.Model):
    service = models.ForeignKey(crmServices, on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal = models.CharField(max_length=100)
    is_signed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    
    
    
    
class agreementSettings(models.Model):
    terms_url = models.CharField(max_length=1000)
    policy_url = models.CharField(max_length=1000)