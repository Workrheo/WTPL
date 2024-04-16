from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseBadRequest
from crm.models import *
from crm.forms import *
from authapp.models import *
from settings.models import *
from userapp.models import *
from userapp.forms import ReplyForm, SupportTicketStatusForm
from django.db.models import Sum
from core.decorators import admin_role_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from core.decorators import *

# ====================Dashboard====================
@login_required(login_url='signIn')
@admin_role_required
def crmHome(request):
    # Revenue Expense
    total_revenue = Payments.objects.aggregate(total_revenue=Sum('payment_ammount'))
    total_revenue = total_revenue['total_revenue'] if total_revenue['total_revenue'] is not None else 0

    total_expense = Expense.objects.aggregate(total_expense=Sum('amount'))
    total_expense = total_expense['total_expense'] if total_expense['total_expense'] is not None else 0

    profit = total_revenue - total_expense
    
    if profit < 0:
        result = "Loss"
    else:
        result = "Profitable"

    
    # Invoices
    invoice = Invoice.objects.all()
    paid_count = Invoice.objects.filter(status='PAID').count()
    unpaid_count = Invoice.objects.exclude(status='PAID').count()
    overdue_count = Invoice.objects.filter(status='OVERDUE').count()
    
    # Count tasks for each status
    tasks = crmTasks.objects.all()
    to_do_count = crmTasks.objects.filter(status='to_do').count()
    in_progress_count = crmTasks.objects.filter(status='in_progress').count()
    done_count = crmTasks.objects.filter(status='done').count()
    
    # Project
    project_count = crmProjects.objects.all().count()
    client_project = crmProjects.objects.filter(project_type='client_project').count()
    internal_project = crmProjects.objects.filter(project_type='internal_project').count()
    
    # Payments
    payments = Payments.objects.all().order_by('-payment_date')
    expenses = Expense.objects.all().order_by('-date_of_expense')
    
    # Tickets
    tickets = supportTicket.objects.all()
    
    
    context = {
        'title': 'CRM',
        'payments' : payments,
        'expenses' : expenses,
        'tickets' : tickets,
        
        # Revenue Expense Chart
        'total_revenue': total_revenue,
        'total_expense': total_expense,
        'profit' : profit,
        'result' : result,
        
        # Invoice Chart
        'invoice': invoice,
        'paid_invoice' : paid_count,
        'unpaid_invoice' : unpaid_count,
        'overdue_invoice' : overdue_count,
        
        # Task Chart
        'tasks': tasks,
        'to_do' : to_do_count,
        'in_progress' : in_progress_count,
        'done' : done_count,
        
        # Project Chart
        'project_count' : project_count,
        'client_project' :  client_project,
        'internal_project' : internal_project,
    }
    return render(request, 'crm/main/index.html', context)

# ====================Items/Products/Services====================
@login_required(login_url='signIn')
@admin_role_required
def crmItems(request):
    crmitems = items.objects.all()
    
    context = {
        'title' : 'Items',
        'items' : crmitems,
    }
    
    return render(request, 'crm/main/items/items.html', context)

@login_required(login_url='signIn')
@admin_role_required
def crmItemCreate(request):
    form = CRMItemForm()
    if request.method == 'POST':
        form = CRMItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()
            messages.success(request, f'{item.name} Created Successfully')
            return redirect('crmItems')
    
    context = {
        'title': 'Add New Item',
        'form': form,
    }
    
    return render(request, 'crm/main/items/create.html', context)


@login_required(login_url='signIn')
@admin_role_required
def crmItemEdit(request, slug):
    item = get_object_or_404(items, slug=slug)
    form = CRMItemForm(instance=item)
    if request.method == 'POST':
        form = CRMItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'{item.name} Updated Successfully')
            return redirect('crmItems')
    
    context = {
        'title' : 'Add New Item',
        'form' : form,
        'item' : item,
    }
    
    return render(request, 'crm/main/items/edit.html', context)
    

@login_required(login_url='signIn')
@admin_role_required
def crmItemDelete(request, slug):
    try:
        item = items.objects.get(slug=slug)
        messages.success(request, f'{item.name} Deleted Successfully!')
        item.delete()
        return redirect('crmItems')
    except:
        messages.warning(request, 'Something went wrong')
        return redirect('crmItems')
    
# ====================Items/Products/Services Category====================
@login_required(login_url='signIn')
@admin_role_required
def crmItemCategory(request):
    categories = itemCategory.objects.all()
    
    context = {
        'title': 'Item Categories',
        'categories': categories,
    }
    return render(request, 'crm/main/items/partials/category/category.html', context)

@login_required(login_url='signIn')
@admin_role_required
def crmItemCategoryCreate(request):
    if request.method == 'POST':
        form = CRMItemCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully')
            return redirect('crmItemCategories')
    else:
        form = CRMItemCategoryForm()
    
    context = {
        'title': 'Create Item Category',
        'form': form,
    }
    return render(request, 'crm/main/items/partials/category/create.html', context)

@login_required(login_url='signIn')
@admin_role_required
def crmItemCategoryEdit(request, slug):
    category = get_object_or_404(itemCategory, slug=slug)
    if request.method == 'POST':
        form = CRMItemCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully')
            return redirect('crmItemCategories')
    else:
        form = CRMItemCategoryForm(instance=category)
        
    context = {
        'title': 'Edit',
        'form': form,
        'category':category,
    }
    return render(request, 'crm/main/items/partials/category/edit.html', context)

@login_required(login_url='signIn')
@admin_role_required
def crmItemCategoryDelete(request, slug):
    category = get_object_or_404(itemCategory, slug=slug)
    category.delete()
    messages.success(request, 'Category deleted successfully')
    return redirect('crmItemCategories')

# ====================CRM Clients====================
@login_required(login_url='signIn')
@admin_role_required
def crmClientsList(request):
    clients = Guser.objects.all()
    
    context = {
        'title': 'Clients',
        'clients': clients,
    }
    return render(request, 'crm/main/clients/clients.html', context)

@login_required(login_url='signIn')
@admin_role_required
def crmClientCreate(request):
    if request.method == "POST":
        username = request.POST.get('username')
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('login[password]')
        if Guser.objects.filter(username__iexact=username):
             messages.warning(request, 'Username already exists')
             return redirect('crmClientCreate')
        if Guser.objects.filter(email__iexact=email):
            messages.warning(request, 'Email already exists')
            return redirect('crmClientCreate')
        user = Guser.objects.create_user(username = username,  email = email, password=password)
        if user:
            user.userprofile.name = name  # add this line to set the name in UserProfile
            user.userprofile.save()  # save the UserProfile instance
            
            # Send a welcome email to the user
            website_settings = websiteSetting.objects.first()
            subject = f'Welcome to {website_settings.name}'
            from_email = f'"{website_settings.name}" <{settings.DEFAULT_FROM_EMAIL}>'
            to_email = [email]
            
            # Load the HTML email template
            html_message = render_to_string('admin/auth/email/welcome.html', {
                'username': username,
                'settings': website_settings,
            })
            
            email_message = EmailMessage(
                subject=subject,
                body=html_message,
                from_email=from_email,
                to=to_email,
            )
            email_message.content_subtype = 'html'
            email_message.send()
            messages.success(request, 'Client created successfully!')
            return redirect('crmClients')
        
        context = {
            'title': 'Create Client',
        }
    else:
        context = {
            'title': 'Create Client',
        }
    return render(request, 'crm/main/clients/create.html', context)

@login_required(login_url='signIn')
@admin_role_required
def crmClientEdit(request, slug):
    try:
        profile = UserProfile.objects.get(slug=slug)
        client = profile.user
    except UserProfile.DoesNotExist:
        raise Http404("User profile does not exist")

    if request.method == 'POST':
        form = CRMClientForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client updated successfully!')
            return redirect('crmClientEdit', slug=client.userprofile.slug)
    else:
        form = CRMClientForm(instance=profile)

    context = {
        'title': 'Edit',
        'form': form,
        'profile': profile,
        'client': client,
    }
    return render(request, 'crm/main/clients/edit.html', context)

@login_required(login_url='signIn')
@admin_role_required
def crmClientDelete(request, slug):
    profile = UserProfile.objects.get(slug=slug)
    client = profile.user
    client.delete()
    messages.warning(request, 'Client deleted successfully!')
    return redirect('crmClients')

# ====================CRM Projects====================
@login_required(login_url='signIn')
@admin_role_required
def crmProjectsList(request):
    projects = crmProjects.objects.all()
    
    context = {
        'title': 'Projects',
        'projects': projects,
    }
    return render(request, 'crm/main/projects/projects.html', context)

@login_required(login_url='signIn')
@admin_role_required
def crmProjectCreate(request):
    if request.method == 'POST':
        project_form = CRMProjectsForm(request.POST)
        if project_form.is_valid():
            project = project_form.save()

            # Process the uploaded files
            for file in request.FILES.getlist('files'):
                ProjectFile.objects.create(project=project, upload_file=file)
            messages.success(request, 'Project created successfully!')
            return redirect('crmProjects')  # Redirect to the project listing page or other appropriate page

    else:
        project_form = CRMProjectsForm()

    context = {
        'title': 'Create Project',
        'form': project_form,
    }

    return render(request, 'crm/main/projects/create.html', context)

@login_required(login_url='signIn')
@admin_role_required
def crmProjectEdit(request, slug):
    project = get_object_or_404(crmProjects, slug=slug)
    
    if request.method == 'POST':
        form = CRMProjectsForm(request.POST, instance=project)
        if form.is_valid():
            form.save()

            # Handle file replacement or deletion
            file_ids_to_delete = request.POST.getlist('delete_files')
            for file_id in file_ids_to_delete:
                ProjectFile.objects.get(id=file_id).delete()

            uploaded_files = request.FILES.getlist('files')
            for file in uploaded_files:
                ProjectFile.objects.create(project=project, upload_file=file)
            messages.success(request, 'Project updated successfully!')

            return redirect('crmProjectEdit', slug=project.slug)

    else:
        form = CRMProjectsForm(instance=project)

    context = {
        'title': 'Edit',
        'form': form,
        'project': project,
    }
    return render(request, 'crm/main/projects/edit.html', context)

@login_required(login_url='signIn')
@admin_role_required
def crmProjectDelete(request, slug):
    project = get_object_or_404(crmProjects, slug=slug)
    project.delete()
    messages.warning(request, 'Project deleted successfully!')
    return redirect('crmProjects')  

# ====================CRM Tasks====================
@login_required(login_url='signIn')
@admin_role_required
def crmTasksList(request):
    tasks = crmTasks.objects.all()
    
    context = {
        'title': 'Tasks',
        'tasks': tasks,
    }
    return render(request, 'crm/main/tasks/tasks.html', context)

@login_required(login_url='signIn')
@admin_role_required
def crmTaskCreate(request):
    if request.method == 'POST':
        form = CRMTaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task created successfully!')
            return redirect('crmTasks')
    else:
        form = CRMTaskForm()
    
    context = {
        'title': 'Create Task',
        'form': form,
    }
    return render(request, 'crm/main/tasks/create.html', context)

@login_required(login_url='signIn')
@admin_role_required
def crmTaskEdit(request, id):
    task = get_object_or_404(crmTasks, id=id)
    if request.method == 'POST':
        form = CRMTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('crmTasks')
    else:
        form = CRMTaskForm(instance=task)
    
    context = {
        'title': 'Edit',
        'form': form,
        'task': task,
    }
    return render(request, 'crm/main/tasks/edit.html', context)

@login_required(login_url='signIn')
@admin_role_required
def crmTaskDelete(request, id):
    task = get_object_or_404(crmTasks, id=id)
    task.delete()
    messages.warning(request, 'Task deleted successfully!')
    return redirect('crmTasks')

# ====================CRM Invoice====================
@login_required(login_url='signIn')
@admin_role_required
def invoiceList(request):
    invoices =Invoice.objects.all().order_by('-date_created')
    
    total = 0
    
    for invoice in invoices:
        discount = invoice.discount_amount
        tax = invoice.tax_amount
        other_fee_amount = invoice.other_fees_amount
        invoice_total = (invoice.sub_total + tax + other_fee_amount) - discount
        total += invoice_total
    
    context = {
        'title': 'Invoices',
        'invoices': invoices,
        'total':total
    }
    return render(request, 'crm/main/invoice/invoice.html', context)

@login_required(login_url='signIn')
@admin_role_required
def createInvoice(request):
    # Create a blank invoice
    number = 'INV-' + str(uuid4()).split('-')[1]
    new_invoice = Invoice.objects.create(number=number)
    new_invoice.save()

    inv = Invoice.objects.get(number=number)

    Invoice.delete_blank_invoices()

    return redirect('create-build-invoice', slug=inv.slug)

@login_required(login_url='signIn')
@admin_role_required
def createBuildInvoice(request, slug):
    try:
        invoice = Invoice.objects.get(slug=slug)
        pass
    except:
        messages.error(request, 'Something went wrong')
        return redirect('crmInvoiceList')

    #fetch all the products - related to this invoice
    discount = invoice.discount_amount or 0
    tax = invoice.tax_amount or 0 
    other_fee_name = invoice.other_fees_name
    other_fee_amount = invoice.other_fees_amount or 0 
    total = (invoice.sub_total or 0) + tax + other_fee_amount - discount

    
    context = {}
    context['invoice'] = invoice
    context['discount'] = discount
    context['tax'] = tax
    context['other_fee_name'] = other_fee_name
    context['other_fee_amount'] = other_fee_amount
    context['total'] = total
    
    if request.method == 'GET':
        prod_form  = CRMItemForm()
        discount_form = discountForm(instance=invoice)
        tax_form = taxForm(instance=invoice)
        other_fee_form = otherFeeForm(instance=invoice)
        inv_form = invoiceForm(instance=invoice)
        client_form = ClientSelectForm(initial_client=invoice.client)
        item_selection_form = ItemSelectionForm()
        
        context['item_selection_form'] = item_selection_form
        context['prod_form'] = prod_form
        context['inv_form'] = inv_form
        context['discount_form'] = discount_form
        context['tax_form'] = tax_form
        context['other_fee_form'] = other_fee_form
        context['client_form'] = client_form
        context['invoice'] = invoice
        return render(request, 'crm/main/invoice/create.html', context)

    if request.method == 'POST':
        prod_form  = CRMItemForm(request.POST)
        inv_form = invoiceForm(request.POST, instance=invoice)
        discount_form = discountForm(request.POST, instance=invoice)
        tax_form = taxForm(request.POST, instance=invoice)
        other_fee_form = otherFeeForm(request.POST, instance=invoice)
        client_form = ClientSelectForm(request.POST, initial_client=invoice.client, instance=invoice)
        item_selection_form = ItemSelectionForm(request.POST)
        
        if item_selection_form.is_valid() and 'quantity' in request.POST:
            selected_item = item_selection_form.cleaned_data['selected_item']
            quantity = item_selection_form.cleaned_data['quantity']

            if invoice.sub_total is None:
                invoice.sub_total = 0.0

            item_instance = items.objects.get(pk=selected_item.pk)

            # Check if an InvoiceItem for the selected item already exists for this invoice
            existing_invoice_item = InvoiceItem.objects.filter(invoice=invoice, item=item_instance).first()

            if existing_invoice_item:
                # Update the existing InvoiceItem
                existing_invoice_item.quantity += quantity
                existing_invoice_item.sub_total += item_instance.rate * quantity
                existing_invoice_item.save()
            else:
                # Create a new InvoiceItem
                invoice_item = InvoiceItem.objects.create(
                    invoice=invoice,
                    item=item_instance,
                    unit_type=item_instance.unit_type,
                    quantity=quantity,
                    unit_price=item_instance.rate,
                    sub_total=item_instance.rate * quantity
                )
                invoice.products.add(item_instance)

            # Update subtotal
            invoice.sub_total += item_instance.rate * quantity

            invoice.save()
            messages.success(request, "Item added to the invoice successfully")
            return redirect('create-build-invoice', slug=slug)
                
        elif inv_form.is_valid and 'status' in request.POST:
            inv_form.save()
            messages.success(request, "Invoice updated succesfully")
            return redirect('create-build-invoice', slug=slug)
        
        elif discount_form.is_valid() and 'discount_amount' in request.POST:
            discount_amount = discount_form.cleaned_data['discount_amount']
            
            if discount_amount < 0:
                messages.warning(request, "Discount amount cannot be less than 0.")
            else:
                discount_form.save()
                messages.success(request, "Discount updated successfully")
            
            return redirect('create-build-invoice', slug=slug)
        
        elif tax_form.is_valid() and 'tax_amount' in request.POST:
            tax_amount = tax_form.cleaned_data['tax_amount']
            
            if tax_amount < 0:
                messages.warning(request, "Tax amount cannot be less than 0.")
            else:
                tax_form.save()
                messages.success(request, "Tax updated successfully")
            
            return redirect('create-build-invoice', slug=slug)
        
        elif other_fee_form.is_valid() and 'other_fees_amount' in request.POST:
            other_fees_name = other_fee_form.cleaned_data['other_fees_name']
            other_fees_amount = other_fee_form.cleaned_data['other_fees_amount']
            
            if other_fees_amount < 0:
                messages.warning(request, "Other fees amount cannot be less than 0.")
            else:
                other_fee_form.save()
                messages.success(request, "Other fees updated successfully")
            
            return redirect('create-build-invoice', slug=slug)
            
        
        elif client_form.is_valid() and 'client' in request.POST:
            client_form.save()
            messages.success(request, "Client added to invoice succesfully")
            return redirect('create-build-invoice', slug=slug)
                
        elif 'send_email' in request.POST:
            website_settings = websiteSetting.objects.first()
            # Send HTML email to the client with the invoice details
            subject = 'Invoice Details'
            from_email = f'"{website_settings.name}" <{settings.DEFAULT_FROM_EMAIL}>'
            html_message = render_to_string('crm/main/email/invoice-email.html', {
                'client_name': invoice.client,
                'invoice' : invoice,
                'invoice_number': invoice.number,
                'discount' : discount,
                'tax' : tax,
                'other_fee_name' : other_fee_name,
                'other_fee_amount' : other_fee_amount,
                'total' : total,
                'settings' : website_settings,
            })

            email_message = EmailMessage(
                subject=subject,
                body=html_message,
                from_email=from_email,
                to=[invoice.client.userprofile.email]
            )
            email_message.content_subtype = 'html'
            email_message.send()
            messages.success(request, "Email has sent succesfully")
            return redirect('create-build-invoice', slug=slug)
        else:
            context['prod_form'] = prod_form
            context['inv_form'] = inv_form
            context['discount_form'] = discount_form
            context['tax_form'] = tax_form
            context['other_fee_form'] = other_fee_form
            context['client_form'] = client_form
            context['item_selection_form'] = item_selection_form
            messages.error(request,"Problem processing your request")
            return render(request, 'crm/main/invoice/create.html', context)


    return render(request, 'crm/main/invoice/create.html', context)

def delete_invoice_product(request, slug, product_id):
    invoice = get_object_or_404(Invoice, slug=slug)
    product = get_object_or_404(items, id=product_id)
    invoice_item = InvoiceItem.objects.filter(invoice=invoice, item=product).first()

    invoice.products.remove(product)

    if invoice_item:
        invoice.sub_total -= invoice_item.sub_total
        invoice_item.delete()

    if not invoice.products.exists():
        invoice.discount_amount = 0
        invoice.tax_amount = 0
        invoice.other_fees_amount = 0

    invoice.save()
    messages.success(request, 'Item removed successfully!')
    return redirect('create-build-invoice', slug=slug)

@login_required(login_url='signIn')
@admin_role_required
def viewPrintnvoice(request, slug):
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
        'discount' : discount,
        'tax' : tax,
        'other_fee_name' : other_fee_name,
        'other_fee_amount' : other_fee_amount,
        'total' : total,
    }
    return render(request, 'crm/main/invoice/partials/inv.html', context)

@login_required(login_url='signIn')
@admin_role_required
def deleteInvoice(request, slug):
    try:
        Invoice.objects.get(slug=slug).delete()
        messages.success(request, 'Invoice deleted successfully')
    except:
        messages.error(request, 'Something went wrong')
        return redirect('crmInvoiceList')

    return redirect('crmInvoiceList')


# ====================CRM Payments====================
@login_required(login_url='signIn')
@admin_role_required
def paymentsList(request):
    payments = Payments.objects.all()
    
    context = {
        'title': 'Payments',
        'payments': payments,
    }
    return render(request, 'crm/main/payments/payments.html', context)

@login_required(login_url='signIn')
@admin_role_required
def paymentCreate(request):
    if request.method == 'POST':
        form = PaymentsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment created successfully!')
            return redirect('payments')
    else:
        form = PaymentsForm()
    
    context = {
        'title': 'Create Payment',
        'form': form,
    }
    return render(request, 'crm/main/payments/create.html', context)

@login_required(login_url='signIn')
@admin_role_required
def paymentEdit(request, slug):
    payment = get_object_or_404(Payments, slug=slug)
    if request.method == 'POST':
        form = PaymentsForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment updated successfully!')
            return redirect('payments')
    else:
        form = PaymentsForm(instance=payment)
    
    context = {
        'title': 'Edit',
        'form': form,
        'payment': payment,
    }
    return render(request, 'crm/main/payments/edit.html', context)

@login_required(login_url='signIn')
@admin_role_required
def paymentDelete(request, slug):
    payment = get_object_or_404(Payments, slug=slug)
    payment.delete()
    messages.warning(request, 'Payment deleted successfully!')
    return redirect('payments')

# ====================CRM Expense====================
@login_required(login_url='signIn')
@admin_role_required
def expensesList(request):
    expenses = Expense.objects.all()
    
    context = {
        'title': 'Expenses',
        'expenses': expenses,
    }
    return render(request, 'crm/main/expenses/expenses.html', context)

@login_required(login_url='signIn')
@admin_role_required
def expenseCreate(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense created successfully!')
            return redirect('expenses')
    else:
        form = ExpenseForm()
    
    context = {
        'title': 'Create Expense',
        'form': form,
    }
    return render(request, 'crm/main/expenses/create.html', context)

@login_required(login_url='signIn')
@admin_role_required
def expenseEdit(request, slug):
    expense = get_object_or_404(Expense, slug=slug)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('expenses')
    else:
        form = ExpenseForm(instance=expense)
    
    context = {
        'title': 'Edit',
        'form': form,
        'expense': expense,
    }
    return render(request, 'crm/main/expenses/edit.html', context)

@login_required(login_url='signIn')
@admin_role_required
def expenseDelete(request, slug):
    expense = get_object_or_404(Expense, slug=slug)
    expense.delete()
    messages.warning(request, 'Expense deleted successfully!')
    return redirect('expenses')

# ====================Crm Tickets====================
@login_required(login_url='signIn')
@both_role_required
def ticketList(request):
    tickets = supportTicket.objects.all()
    
    context = {
        'title': 'Tickets',
        'tickets': tickets,
    }
    return render(request, 'crm/main/tickets/tickets.html', context)

@login_required(login_url='signIn')
@both_role_required
def ticketView(request, id):
    ticket = get_object_or_404(supportTicket, id=id)
    replyform = ReplyForm()
    statusForm = SupportTicketStatusForm(instance=ticket)
    if request.method == 'POST':
        if 'status' in request.POST: 
            statusForm = SupportTicketStatusForm(request.POST, instance=ticket)
            if statusForm.is_valid():
                statusForm.save()
                messages.success(request, 'Status updated successfully!')
                return redirect('ticketView', id=ticket.id)
            else:
                return HttpResponseBadRequest('Invalid status form')
    context ={
        'title' : 'View Ticket',
        'ticket' : ticket,
        'replyform' : replyform,
        'statusform' : statusForm,
        'replies' : ticket.replies.all()
    }
    return render(request, 'crm/main/tickets/view.html', context)

@login_required(login_url='signIn')
@both_role_required
def ticketDelete(request, id):
    ticket = get_object_or_404(supportTicket, id=id)
    ticket.delete()
    messages.warning(request, 'Ticket deleted successfully!')
    return redirect('tickets')

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


# CRM Service
@login_required(login_url='signIn')
@both_role_required
def serviceList(request):
    services = crmServices.objects.all()
    
    context = {
        'title' : 'Services',
        'services' : services,
    }
    return render(request, 'crm/main/services/index.html', context)

@login_required(login_url='signIn')
@both_role_required
def serviceCreate(request):
    if request.method == 'POST':
        form = serviceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service created successfully!')
            return redirect('serviceList')
    else:
        form = serviceForm()
        
    context ={
        'title' : 'Create Service',
        'form' : form,
    }
    return render(request, 'crm/main/services/create.html', context)

@login_required(login_url='signIn')
@both_role_required
def serviceEdit(request, id):
    service = get_object_or_404(crmServices, id=id)
    if request.method == 'POST':
        form = serviceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully!')
            return redirect('serviceList')
    else:
        form = serviceForm(instance=service)
        
    context ={
        'title' : 'Edit Service',
        'form' : form,
    }
    return render(request, 'crm/main/services/edit.html', context)

@login_required(login_url='signIn')
@both_role_required
def serviceDelete(request, id):
    service = get_object_or_404(crmServices, id=id)
    service.delete()
    messages.warning(request, 'Service deleted successfully!')
    return redirect('serviceList')

# Admin Custom Page Views
class adminCustomPage(LoginRequiredMixin,ListView):
    model = crmCustomPage
    template_name = 'crm/main/custompage/index.html'
    context_object_name = 'pages'
    extra_context = {'title': 'All Custom Pages'}
    login_url = reverse_lazy('signIn')

class adminCustomPageCreate(LoginRequiredMixin,CreateView):
    model = crmCustomPage
    form_class = customPageForm
    template_name = 'crm/main/custompage/create.html'
    success_url = reverse_lazy('adminCustomPage')
    extra_context = {'title': 'Create Page'}
    login_url = reverse_lazy('signIn')

    def form_valid(self, form):
        messages.success(self.request, 'Page created successfully!')
        return super().form_valid(form)

class adminCustomPageEdit(LoginRequiredMixin,UpdateView):
    model = crmCustomPage
    form_class = customPageForm
    template_name = 'crm/main/custompage/edit.html'
    success_url = reverse_lazy('adminCustomPage')
    extra_context = {'title': 'Edit Page'}
    login_url = reverse_lazy('signIn')
    
    def form_valid(self, form):
        messages.success(self.request, 'Page updated successfully!')
        return super().form_valid(form)
    
@login_required(login_url='logIn')
def adminCustomPageDelete(request,id):
    page = get_object_or_404(crmCustomPage, id=id)
    messages.warning(request, 'Page deleted successfully!')
    page.delete()
    return redirect('adminCustomPage')

# Custom Page Front
def customPageFront(request, slug):
    page = get_object_or_404(crmCustomPage, slug=slug)
    return render(request, 'crm/main/custompage/view.html', {'page': page})

# ====================Error Page====================
def error_404(request, exception):
    return render(request, 'error/error_404.html', status=404)

def error_500(request):
    return render(request, 'error/error_500.html', status=500)