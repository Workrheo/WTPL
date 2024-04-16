from django.urls import path
from order.views import *
from order.sslcommerze_pay import *
from order.paypal import *
from order.stripe import *
from order.razorpay import *
from order.instamojo import *

urlpatterns = [
    path('user/products/', product_list, name='product_list'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('user/cart/delete/<int:id>/', cart_delete, name='cart_delete'),
    path('user/cart/', view_cart, name='view_cart'),
    path('user/checkout/', checkout, name='checkout'),
    path('order/confirmation/<int:id>/', order_confirmation, name='order_confirmation'),
    path('order/payment-failed', payment_failed, name='payment_failed'),

    path('order/sslcommerze/success', sslcommerze_success, name='sslcommerz_success'),
    path('order/sslcommerze/failed', sslcommerze_failed, name='sslcommerz_failed'),

    path('order/paypal/success', paypal_success, name='paypal_success'),
    path('order/paypal/failed', paypal_failed, name='paypal_failed'),

    path('order/stripe/success', stripe_success, name='stripe_success'),
    
    path('order/instamojo/success', instamojo_success, name='instamojo_success'),
    path('order/instamojo/failed', instamojo_failed, name='instamojo_failed'),
    # Example in urls.py
    path('order/razorpay/getaway/<int:price>/', razorpayGetaway, name='razorpay_getaway'),

    path('order/razorpay/success/', razorpay_success, name='razorpay_success'),

]
