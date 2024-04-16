from django.shortcuts import render, redirect, get_object_or_404
from uuid import uuid4
from crm.models import crmProjects, Invoice, InvoiceItem
from datetime import date
from order.models import *
from django.contrib import messages
from order.sslcommerze_pay import sslCommerzGateway
from order.paypal import paypalGeteway
from order.stripe import stripeGateway
from order.razorpay import razorpayGetaway
from order.instamojo import mojoGetaway
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from settings.models import websiteSetting
from crm.forms import invoiceForm


"""Product list"""
@login_required(login_url='signIn')
def product_list(request):
    order_settings = websiteSetting.objects.first()
    if order_settings.is_purchasing_enable:
        products = items.objects.all().order_by("-id")
        return render(request, 'user/main/ecom/products.html', {'products': products})
    else:
        return redirect('userDashboard')


"""Add to cart"""
@login_required(login_url='signIn')
def add_to_cart(request, product_id):
    order_settings = websiteSetting.objects.first()
    if order_settings.is_purchasing_enable:
        product = items.objects.get(pk=product_id)
        order, created = Order.objects.get_or_create(user=request.user, is_ordered=False)

        user_quantity = int(request.POST.get('user_quantity', 1))

        order_product, created = Cart.objects.get_or_create(order=order, product=product)

        if created:
            order_product.quantity = user_quantity
            messages.success(request, f'{product} added to cart successfully!')
        else:
            order_product.quantity += user_quantity
            messages.info(request, f'Quantity updated successfully for {product}!')

        if product.rate is not None:
            order_product.unit_price = product.rate
            order_product.subtotal += product.rate * user_quantity
            order_product.unit_type = product.unit_type
            order.total_amount += product.rate * user_quantity
            order.save()

        order_product.save()
        order.products.add(product)

        return redirect('product_list')
    else:
        return redirect('userDashboard')

"""Cart view"""

@login_required(login_url='signIn')
def view_cart(request):
    order_settings = websiteSetting.objects.first()
    if order_settings.is_purchasing_enable:
        return render(request, 'user/main/ecom/cart.html')
    else:
        return redirect('userDashboard')

@login_required(login_url='signIn')
def cart_delete(request, id):
    order_settings = websiteSetting.objects.first()
    if order_settings.is_purchasing_enable:
        cart_item = get_object_or_404(Cart, pk=id)

        if cart_item.order.user != request.user:
            messages.warning(request, "You do not have permission to delete this item.")
            return redirect('view_cart')

        cart_item.order.products.remove(cart_item.product)
        cart_item.order.total_amount -= cart_item.subtotal
        cart_item.order.save()

        cart_item.delete()
        if cart_item.order.products.count() == 0:
            cart_item.order.delete()
        messages.warning(request, f'{cart_item.product.name} is deleted from cart!')
        return redirect('view_cart')
    else:
        return redirect('userDashboard')


"""Checkout"""

@login_required(login_url='signIn')
def checkout(request):
    order_settings = websiteSetting.objects.first()
    if order_settings.is_purchasing_enable:
        current_host = request.get_host()
        protocol = 'https' if request.is_secure() else 'http'
        number = 'INV-' + str(uuid4()).split('-')[1]

        if request.user.is_authenticated:
            try:
                order = Order.objects.get(user=request.user, is_ordered=False)
            except Order.DoesNotExist:
                return redirect('view_cart')

            if request.method == 'POST':
                form = invoiceForm()
                if form.is_valid():
                    form.save()

            if request.method == 'POST':
                name = request.POST.get('name')
                email = request.POST.get('email')
                phone = request.POST.get('phone')
                city = request.POST.get('city')
                address = request.POST.get('address')
                country = request.POST.get('country')

                if not all([name, email, phone, city, address, country]):
                    messages.warning(request, 'Billing information is required! Please add from profile.')
                    return render(request, 'user/main/ecom/checkout.html', {'order': order})

                if 'sslcommerze' in request.POST:
                    response = sslCommerzGateway(name=name, email=email, price=order.total_amount, phone=phone,
                                                address=address, city=city, country=country, user=request.user.pk,
                                                host=current_host, protocol=protocol)
                    if response['status'] == 'SUCCESS':
                        redirect_url = response['GatewayPageURL']
                        return redirect(redirect_url)
                    else:
                        print(response)
                        return redirect('view_cart')

                elif 'paypal' in request.POST:
                    price = order.total_amount
                    paypal_url = paypalGeteway(price=price, host=current_host, protocol=protocol)
                    return redirect(paypal_url)

                elif 'instamojo' in request.POST:
                    price = order.total_amount
                    mojo_url = mojoGetaway(request, price=price, email=email, protocol=protocol, host=current_host)
                    print(request)

                    if mojo_url is not None:
                        return redirect(mojo_url)
                    else:
                        print("Error: Instamojo payment processing failed.")
                
                elif 'stripe' in request.POST:
                    price = order.total_amount
                    gateway_url = stripeGateway(host=current_host, protocol=protocol, price=price)
                    return redirect(gateway_url)

                elif 'razorpay' in request.POST:
                    # Get Razorpay order details
                    response = razorpayGetaway(request, price=order.total_amount)
                    if 'order_id' in response and 'amount' in response:
                        order.payment_method = 'razorpay'
                        order.save()

                        return JsonResponse(response)
                    else:
                        print(response)
                        return redirect('view_cart')

                elif 'offlinepayment' in request.POST:
                    order.payment_method = 'offlinepayment'
                    order.is_ordered = True
                    order.status = "pending"
                    order.transaction_id = "Offline Payment"
                    order.save()

                    if order_settings.is_auto_invoice_enable:

                        # Creating a project for the invoice
                        project = crmProjects.objects.create(
                            title=f"Project of Order {order.order_id}",
                            start_date=date.today(),
                            deadline=date.today(),
                            price=order.total_amount,
                            client=order.user,
                            label='started',
                        )

                        # Creating an invoice for the user
                        invoice = Invoice.objects.create(
                            number=number,
                            client=order.user,
                            billDate=date.today(),
                            dueDate=date.today(),
                            project=project,
                            title=f"Invoice for Order {order.order_id}",
                            sub_total=order.total_amount,
                            discount_amount=0,
                            tax_amount=0,
                            other_fees_name="Other Fees",
                            other_fees_amount=0,
                        )
                        invoice.products.set(order.products.all())

                        # Adding invoice items based on order products
                        for cart_item in Cart.objects.filter(order=order):
                            InvoiceItem.objects.create(
                                invoice=invoice,
                                item=cart_item.product,
                                unit_type=cart_item.unit_type,
                                quantity=cart_item.quantity,
                                unit_price=cart_item.unit_price,
                                sub_total=cart_item.subtotal,
                            )

                        invoice.sub_total = invoice.get_total()
                        invoice.save()

                    messages.success(request, 'Order placed successfully!')
                    redirect_url = reverse('order_confirmation', args=[order.id]) + '?first_visit=true'
                    return redirect(redirect_url)

                else:
                    pass

            return render(request, 'user/main/ecom/checkout.html', {'order': order})
        else:
            return redirect('signIn')
    else:
        return redirect('userDashboard')


@login_required(login_url='signIn')
def order_confirmation(request, id):
    order = get_object_or_404(Order, id=id, user=request.user, is_ordered=True)

    first_visit = request.GET.get('first_visit', None)

    if first_visit:
        cart_items = Cart.objects.filter(order=order)
        return render(request, 'user/main/ecom/order_confirm.html', {'order': order, 'cart_items': cart_items})

    return redirect('product_list')


@login_required(login_url='signIn')
def payment_failed(request):
    return render(request, 'user/main/ecom/payment-fail.html')


# ====================Error Page====================
def error_404(request, exception):
    return render(request, 'error/error_404.html', status=404)

def error_500(request):
    return render(request, 'error/error_500.html', status=500)