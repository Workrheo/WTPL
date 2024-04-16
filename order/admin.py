from django.contrib import admin
from order.models import Order, Cart

admin.site.register(Order)
admin.site.register(Cart)