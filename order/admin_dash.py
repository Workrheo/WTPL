from order.models import *
from django.shortcuts import render, redirect, get_object_or_404
from order.forms import orderStatusForm
from django.contrib import messages
from core.decorators import admin_role_required
from django.contrib.auth.decorators import login_required

# Admin All Orders
@login_required(login_url='signIn')
@admin_role_required
def adminAllOrders(request):
    orders = Order.objects.filter(is_ordered=True).order_by('-ordered_at')
    pending_orders = Order.objects.filter(status='pending', is_ordered=True).count()
    confirmed_orders = Order.objects.filter(status='confirmed', is_ordered=True).count()
    canceled_orders = Order.objects.filter(status='canceled', is_ordered=True).count()
    
    context = {
        'title' : 'All Orders',
        'orders' : orders,
        'pending_orders' : pending_orders,
        'confirmed_orders' : confirmed_orders,
        'canceled_orders' : canceled_orders,
    }
    
    return render(request, 'crm/main/ecom/orders.html', context)

@login_required(login_url='signIn')
@admin_role_required
def adminOrderDelete(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    order.delete()
    messages.success(request, 'Order deleted successfully!')
    return redirect('adminAllOrders')

# Admin Confirmed Orders
@login_required(login_url='signIn')
@admin_role_required
def adminPendingOrders(request):
    orders = Order.objects.filter(status='pending', is_ordered=True).order_by('-ordered_at')
    
    context = {
        'title' : 'Pending Orders',
        'orders': orders
    }
    
    return render(request, 'crm/main/ecom/pending-orders.html', context)

# Admin Confirmed Orders
@login_required(login_url='signIn')
@admin_role_required
def adminConfirmedOrders(request):
    orders = Order.objects.filter(status='confirmed', is_ordered=True).order_by('-ordered_at')
    
    context = {
        'title' : 'Confirmed Orders',
        'orders': orders
    }
    
    return render(request, 'crm/main/ecom/confirmed-orders.html', context)

# Admin Completed Orders
@login_required(login_url='signIn')
@admin_role_required
def adminCompletedOrders(request):
    orders = Order.objects.filter(status='completed', is_ordered=True).order_by('-ordered_at')
    
    context = {
        'title' : 'Completed Orders',
        'orders': orders
    }
    
    return render(request, 'crm/main/ecom/completed-orders.html', context)

# Admin Canceled Orders
@login_required(login_url='signIn')
@admin_role_required
def adminCanceledOrders(request):
    orders = Order.objects.filter(status='canceled', is_ordered=True).order_by('-ordered_at')
    
    context = {
        'title' : 'Canceled Orders',
        'orders': orders
    }
    
    return render(request, 'crm/main/ecom/canceled-orders.html', context)

# Admin Order Details
@login_required(login_url='signIn')
@admin_role_required
def adminOrderDetails(request, order_id, user):
    order = get_object_or_404(Order, order_id=order_id, user=user, is_ordered=True)
    cart_items = Cart.objects.filter(order=order)
    
    if request.method == 'POST':
        form = orderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order status updated successfully!')
            return redirect('adminOrderDetails', order.user.id, order.order_id)
    else:
        form = orderStatusForm(instance=order)
    
    context = {
        'order' : order,
        'cart_items' : cart_items,
        'form' : form,
    }
    
    return render(request, 'crm/main/ecom/partials/order-details.html', context)