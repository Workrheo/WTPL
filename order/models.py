from django.db import models
from crm.models import items
from authapp.models import User
import time

class Order(models.Model):
    PAYMENT_METHOD = [
        ('ssl_commerz' , 'SSLCOMMERZ'),
        ('paypal' , "Paypal"),
        ('stripe' , "Stripe"),
        ('razorpay' , "Razorpay"),
        ('instamojo' , "Instamojo"),
        ('offlinepayment' , "Offline Payment"),
    ]
    STATUS = [
        ("pending" , 'Pending'),
        ("confirmed", 'Confirmed'),
        ("completed", 'Completed') ,
        ('canceled' , 'Canceled')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(items)
    total_amount = models.FloatField(default=0.0)
    order_id = models.CharField(max_length=15, unique=True, blank=True, null=True)
    transaction_id = models.CharField(max_length=555, blank=True, null=True)
    payment_method = models.CharField(max_length=255 ,choices=PAYMENT_METHOD)
    status = models.CharField( choices= STATUS , max_length=255 , default='pending')
    is_ordered = models.BooleanField(default=False)
    ordered_at = models.DateField(auto_now_add=True)
    
    def generate_order_id(self):
        return f"{int(time.time())}{int(self.user.id)}{int(self.total_amount * 100)}"[:15]

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generate_order_id()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'Order of {self.user}'
    
class Cart(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(items, on_delete=models.CASCADE)
    unit_type = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    unit_price = models.FloatField(default=0.0)
    subtotal = models.FloatField(default=0.0)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"