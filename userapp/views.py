from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from userapp.models import *
from authapp.models import *
from crm.models import *
from userapp.forms import *
from legals.models import *
from django.contrib.auth.decorators import login_required
from core.decorators import user_role_required
from django.db.models import F, Sum, Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from settings.models import websiteSetting
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from order.models import *

# User Home Dashboard
@login_required
def userDashboard(request):
    user = request.user

    # User Project
    projects = crmProjects.objects.filter(client=user).order_by('-start_date')

    # User Invoicing
    user_invoices = Invoice.objects.filter(client=user).order_by('-date_created')
    user_payments = Payments.objects.filter(invoice__client=user).order_by('-payment_date')
    total_invoiced = 0
    for invoice in user_invoices:
        total_product_price = invoice.sub_total
        total_product_price -= invoice.discount_amount
        total_product_price += invoice.tax_amount + invoice.other_fees_amount
        total_invoiced += total_product_price
    total_payments = Payments.objects.filter(invoice__client=user).aggregate(
        total=Sum('payment_ammount'))['total'] or 0

    # User Due
    total_due = total_invoiced - total_payments

    # Calculate the percentage paid by the user
    percentage_paid = (total_payments / total_invoiced) * 100 if total_invoiced != 0 else 0

    # Round the percentage to two decimal places
    percentage_paid = round(percentage_paid, 2)

    # Tickets
    tickets = supportTicket.objects.filter(client=user).order_by('-created_at')

    context = {
        'title': 'Dashboard',
        'invoices': user_invoices,
        'payments': user_payments,
        'projects': projects,
        'tickets': tickets,
        'total_invoiced': total_invoiced,
        'total_payments': total_payments,
        'total_due': total_due,
        'percentage_paid': percentage_paid,
    }
    return render(request, 'user/main/index.html', context)

# User Tickets
@login_required(login_url='signIn')
@user_role_required
def ticketList(request):
    tickets = supportTicket.objects.filter(client=request.user)
    
    context = {
        'title': 'Tickets',
        'tickets': tickets,
    }
    return render(request, 'user/main/tickets/tickets.html', context)

@login_required(login_url='signIn')
@user_role_required
def userTicketCreate(request):
    if request.method == "POST":
        form = SupportTicketForm(request.POST, user=request.user)
        if form.is_valid():
            new_ticket = form.save(commit=False)
            new_ticket.client = request.user
            new_ticket.save()
            messages.success(request, 'Ticket created successfully!')
            return redirect('userTickets')
    else:
        form = SupportTicketForm(user=request.user)
    
    context = {
        'title': 'Create Ticket',
        'form' : form,
    }
    return render(request, 'user/main/tickets/create.html', context)


@login_required(login_url='signIn')
@user_role_required
def userTicketDelete(request, id):
    ticket_list = supportTicket.objects.filter(client=request.user)
    ticket=get_object_or_404(ticket_list, id=id)
    ticket.delete()
    return redirect('userTickets') 
    
@login_required(login_url='signIn')
@user_role_required
def userticketView(request, id):
    ticket = get_object_or_404(supportTicket, id=id)
    replyform = ReplyForm()

    context ={
        'title' : 'View Ticket',
        'ticket' : ticket,
        'replyform' : replyform,
        'replies' : ticket.replies.all()
    }
    return render(request, 'user/main/tickets/view.html', context)

@login_required(login_url='signIn')
@csrf_exempt 
def ajax_reply(request, id):
    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.ticket = get_object_or_404(supportTicket, id=id)
            reply.user = request.user
            reply.save()
            return JsonResponse({
                'success': True,
                'username': request.user.username,
                'userimage': request.user.userprofile.getUserImage(),
                'reply': reply.reply,
                'created_at' : reply.created_at.strftime('%B %d, %Y')
                
            })
        else:
            return JsonResponse({'success': False, 'error': 'Invalid form'})
    else:
        return JsonResponse({'success': False, 'error': 'Not a POST request'})

# User Projects
@login_required(login_url='signIn')
@user_role_required
def userProjects(request):
    user = request.user
    projects = crmProjects.objects.filter(client=user).order_by('-start_date')

    context = {
        'title': 'Projects',
        'projects': projects,
    }
    return render(request, 'user/main/projects/projects.html', context)


@login_required(login_url='signIn')
@user_role_required
def projectDetail(request, slug):
    user = request.user
    # User Project Overview
    user_project = crmProjects.objects.filter(client=user)
    project_single = get_object_or_404(user_project, slug=slug)

    # User Payment Overview
    user_invoices = Invoice.objects.filter(client=user).order_by('-date_created')
    total_invoiced = 0
    for invoice in user_invoices:
        total_product_price = invoice.sub_total
        total_product_price -= invoice.discount_amount
        total_product_price += invoice.tax_amount + invoice.other_fees_amount
        total_invoiced += total_product_price
    total_payments = Payments.objects.filter(invoice__client=user).aggregate(
        total=Sum('payment_ammount'))['total'] or 0

    # User Due
    total_due = total_invoiced - total_payments

    # Check if either total_payments or total_invoiced is zero
    if total_payments == 0 or total_invoiced == 0:
        percentage_paid = 0
    else:
        percentage_paid = (total_payments / total_invoiced) * 100
        percentage_paid = round(percentage_paid, 2)

    # User Tasks for Particular Project
    task_list = crmTasks.objects.filter(project=project_single)
    paginator = Paginator(task_list, 10)
    page_number = request.GET.get('page')
    tasks = paginator.get_page(page_number)

    # User Tickets For Particular Project
    ticket_list = supportTicket.objects.filter(client=request.user, project=project_single)
    paginator = Paginator(ticket_list, 10)
    page_number = request.GET.get('page')
    tickets = paginator.get_page(page_number)

    # User Invoice for Particular Project
    invoice_list = Invoice.objects.filter(client=user, project=project_single)
    paginator = Paginator(invoice_list, 10)
    page_number = request.GET.get('page')
    invoices = paginator.get_page(page_number)

    # User Payment for particular Project Invoice)
    payments_list = Payments.objects.filter(invoice__in=invoice_list)
    paginator = Paginator(payments_list, 10)
    page_number = request.GET.get('page')
    payments = paginator.get_page(page_number)

    context = {
        'project': project_single,
        'percentage_paid': int(percentage_paid),
        'total_invoiced': total_invoiced,
        'total_payments': total_payments,
        'total_due': total_due,
        'tickets': tickets,
        'invoices': invoices,
        'payments': payments,
        'tasks': tasks,
    }
    return render(request, 'user/main/projects/view.html', context)


# User Invoices
@login_required(login_url='signIn')
@user_role_required
def userInvoices(request):
    user = request.user

    invoice_list = Invoice.objects.filter(client=user).order_by('-date_created')

    context = {
        'title': 'Invoices',
        'invoices': invoice_list,
    }
    return render(request, 'user/main/invoice/invoice.html', context)


@login_required(login_url='signIn')
@user_role_required
def viewUserPDFInvoice(request, slug):
    # fetch that invoice
    try:
        invoice = Invoice.objects.get(slug=slug)
    except:
        messages.error(request, 'Something went wrong')
        return redirect('invoices')

    discount = invoice.discount_amount or 0
    tax = invoice.tax_amount or 0
    other_fee_name = invoice.other_fees_name
    other_fee_amount = invoice.other_fees_amount or 0
    total = (invoice.sub_total or 0) + tax + other_fee_amount - discount

    context = {
        'invoice': invoice,
        'discount': discount,
        'tax': tax,
        'other_fee_name': other_fee_name,
        'other_fee_amount': other_fee_amount,
        'total': total,
    }

    return render(request, 'user/main/invoice/partials/inv.html', context)


# User Payments
@login_required(login_url='signIn')
@user_role_required
def userPayments(request):
    user = request.user
    invoice_list = Invoice.objects.filter(client=user)
    payments = Payments.objects.filter(invoice__in=invoice_list).order_by('-payment_date')

    context = {
        'title': 'Payments',
        'payments': payments,
    }
    return render(request, 'user/main/payments/payments.html', context)

# User Profile
@login_required(login_url='signIn')
@user_role_required
def customUserProfile(request):
    user = request.user
    
    # Overview
    user_project = crmProjects.objects.filter(client=user)
    invoices = Invoice.objects.filter(client=user)
    tickets = supportTicket.objects.filter(client=user)
    
    # User Project Pagination
    paginator = Paginator(user_project, 10)
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)
    
    # Password Change
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been changed.')
            return redirect('customUserProfile')  # Replace 'dashboard' with the URL name for your user dashboard.
    else:
        form = CustomPasswordChangeForm(request.user)
        print(form.errors)
        
    context = {
        'title' : 'Profile',
        'projects_count' : user_project, 
        'projects' : projects,
        'invoices' : invoices,
        'tickets' : tickets,
        'form': form
    }
    return render(request, 'user/main/profile/profile.html', context)

@login_required(login_url='signIn')
@user_role_required
def profile_edit_view(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('customUserProfile')  # Replace 'dashboard' with the URL name for your user dashboard.
    else:
        form = UserProfileForm(instance=user_profile)
        
    context = {
        'title' : 'Edit Profile',
        'form': form,
        'profile' : user_profile,
    }
    return render(request, 'user/main/profile/edit.html', context)

# User Agreements
@login_required(login_url='signIn')
@user_role_required
def userAgreements(request):
    user = request.user
    user_agreement = agreement.objects.filter(client=user)
    context = {
        'title' : 'Agreements',
        'user_agreement' : user_agreement,
    }
    return render(request, 'user/main/agreement/agreements.html', context)

@login_required(login_url='signIn')
@user_role_required
def userAgreementDetail(request, id):
    user = request.user
    user_agreement = agreement.objects.filter(client=user)
    a_settings= agreementSettings.objects.first()
    
    agreement_data = get_object_or_404(user_agreement, id=id)
    context = {
        'data' : agreement_data,
        'a_settings' : a_settings,
    }
    return render(request, 'user/main/agreement/detail.html', context)

# Agreement Sign
@login_required(login_url='signIn')
@user_role_required
def signAgreement(request):
    a_settings= agreementSettings.objects.first()
    if request.method == 'POST':
        form = agreementSignForm(request.POST)
        if form.is_valid():
            new_agreement = form.save(commit=False)
            new_agreement.client = request.user
            new_agreement.save()

            # Email content
            terms_page_url = a_settings.terms_url
            website_settings = websiteSetting.objects.first()
            subject = 'Agreement Signed Successfully'
            html_message = render_to_string('admin/front/main/email/agreement_sign.html', {
            'agreement': new_agreement,
            'terms_page_url': terms_page_url,
            'settings' : website_settings,
            })

            
            from_email = f'"{website_settings.name}" <{settings.DEFAULT_FROM_EMAIL}>'
            email_message = EmailMessage(
                subject=subject,
                body=html_message,
                from_email=from_email,
                to=[new_agreement.email],  # Use the email from the agreement form
            )
            email_message.content_subtype = 'html'  # Set content type to HTML
            email_message.send()

            messages.success(request, "Agreement signed successfully. We will get back to you soon. You can check your email for details and confirmation.")
            return redirect('userAgreements')
    else:
        form = agreementSignForm()
    
    context = {
        'title': 'Sign Agreement',
        'form': form,
        'a_settings' : a_settings,
    }
    return render(request, 'user/main/agreement/create.html', context)


# User Orders
@login_required(login_url='signIn')
@user_role_required
def userOrders(request):
    user = request.user
    orders = Order.objects.filter(user=user, is_ordered=True).order_by('-ordered_at')
    pending_orders = Order.objects.filter(user=user, status='pending', is_ordered=True).count()
    confirmed_orders = Order.objects.filter(user=user, status='confirmed', is_ordered=True).count()
    canceled_orders = Order.objects.filter(user=user, status='canceled', is_ordered=True).count()
    
    context = {
        'title': 'Orders',
        'orders': orders,
        'pending_orders': pending_orders,
        'confirmed_orders': confirmed_orders,
        'canceled_orders': canceled_orders,
    }
    return render(request, 'user/main/orders/orders.html', context)


# User Order Details
@login_required(login_url='signIn')
@user_role_required
def userOrderDetail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, is_ordered=True, user=request.user)
    cart_items = Cart.objects.filter(order=order)
    
    context = {
        'order' : order,
        'cart_items' : cart_items,
    }
    
    return render(request, 'user/main/orders/order-detail.html', context)

# ====================Error Page====================
def error_404(request, exception):
    return render(request, 'error/error_404.html', status=404)

def error_500(request):
    return render(request, 'error/error_500.html', status=500)