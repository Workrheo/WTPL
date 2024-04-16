from django.db import models
from ckeditor.fields import RichTextField

class websiteSetting(models.Model):
    name = models.CharField(max_length=500, default='Application Name', blank=True, null=True)
    logo = models.ImageField(upload_to='app_config/', blank=True, null=True)
    logo_width = models.IntegerField(blank=True, null=True)
    invoice_logo = models.ImageField(upload_to='app_config', blank=True, null=True)
    invoice_logo_width = models.IntegerField(blank=True, null=True)
    favicon = models.ImageField(upload_to='app_config/', blank=True, null=True)
    
    author = models.CharField(max_length=200, default='Author Name', blank=True, null=True)
    email_address = models.EmailField(max_length=500, default='test@gmail.com', blank=True, null=True)
    phone_or_whatsapp = models.CharField(max_length=20, default='88012454784', blank=True, null=True)
    price_ragne = models.CharField(max_length=50, default='60$ to 7000$', blank=True, null=True)
    country = models.CharField(max_length=300, default='Your Country', blank=True, null=True)
    address = models.CharField(max_length=700, default='Your Address', blank=True, null=True)
    state = models.CharField(max_length=200, default='Your State', blank=True, null=True)
    Zip = models.IntegerField(default=12345)
    
    analytics_code = models.CharField(max_length=300, blank=True, null=True, default="GA_MEASUREMENT_ID")
    facebook_pixel_code = models.TextField(blank=True, null=True)
    facebook_chat_code = models.TextField(blank=True, null=True)
    
    currency_name = models.CharField(max_length=100, default='USD' , blank=True, null=True)
    currency_symbol = models.CharField(max_length=150, default='$', blank=True, null=True)
    
    twilio_sid = models.CharField(max_length=500, blank=True, null=True)
    twilio_auth_token = models.CharField(max_length=500, blank=True, null=True)
    twilio_from_number = models.CharField(max_length=15, blank=True, null=True)
    
    openai_api = models.CharField(max_length=1000, blank=True, null=True)
    max_token = models.IntegerField(default=150, blank=True, null=True)
    is_enabled_for_user = models.BooleanField(default=False)
    
    is_purchasing_enable = models.BooleanField(default=True)
    is_auto_invoice_enable = models.BooleanField(default=True)

    custom_css = models.TextField(blank=True, null=True)
    custom_js = models.TextField(blank=True, null=True)
    
    footer_copyright = models.CharField(max_length=600)

class paymentMethod(models.Model):
    # SSL Commerze
    ssl_commerze_store_id = models.CharField(max_length=255, blank=True, null=True)
    ssl_commerze_store_pass = models.CharField(max_length=255, blank=True, null=True)
    ssl_commerze_is_sandbox = models.BooleanField(default=False)
    ssl_commerze_is_active = models.BooleanField(default=False)
    
    # PayPal
    paypal_client_id = models.CharField(max_length=5000, blank=True, null=True)
    paypal_client_secret = models.CharField(max_length=5000, blank=True, null=True)
    paypal_is_sandbox = models.BooleanField(default=False)
    paypal_is_active = models.BooleanField(default=False)
    
    # Stripe
    stripe_publish_key = models.CharField(max_length=5000, blank=True, null=True)
    stripe_secret_key = models.CharField(max_length=5000, blank=True, null=True)
    stripe_is_sandbox = models.BooleanField(default=False)
    stripe_is_active = models.BooleanField(default=False)
    
    # Stripe
    instamojo_api_key = models.CharField(max_length=5000, blank=True, null=True)
    instamojo_auth_token = models.CharField(max_length=5000, blank=True, null=True)
    instamojo_is_sandbox = models.BooleanField(default=False)
    instamojo_is_active = models.BooleanField(default=False)
    
    # Razorpay
    razorpay_api_key = models.CharField(max_length=5000, blank=True, null=True)
    razorpay_api_secret = models.CharField(max_length=5000, blank=True, null=True)
    razorpay_is_active = models.BooleanField(default=False)
    
    # Offline Payment
    offline_payment_instruction = RichTextField()
    offline_payment_is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Payment Methods'