from django.shortcuts import render, redirect
from django.contrib import messages
from settings.models import websiteSetting
from core.decorators import admin_role_required
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.conf import settings
from django.core.mail import send_mail
from twilio.rest import Client
from authapp.models import *
from marketing.forms import *

# Email Marketing
@login_required(login_url='signIn')
@admin_role_required
def emailMarketing(request):
    if request.method == "POST":
        form = EmailSelectForm(request.POST)

        if form.is_valid():
            website_settings = websiteSetting.objects.first()
            select_all = form.cleaned_data['select_all']
            selected_users = form.cleaned_data['users']
            email_subject = form.cleaned_data['subject']
            message_content = mark_safe(form.cleaned_data['message'])
            manually_added_emails = form.cleaned_data['manually_added_emails']

            recipients = []

            if select_all:
                recipients.extend([s.email for s in Guser.objects.all()])
            else:
                recipients.extend([s.email for s in selected_users])

            if manually_added_emails:
                recipients.extend([email.strip() for email in manually_added_emails.split(',')])

            # Loop through recipients and send individual emails
            for email in recipients:
                send_mail(
                    email_subject,
                    message_content,
                    f'"{website_settings.name}" <{settings.EMAIL_HOST_USER}>',
                    [email],  # Each email is sent to a single recipient
                    fail_silently=False,
                    html_message=message_content  # Set the HTML content of the email
                )

            messages.success(request, 'Emails sent successfully!')

            return redirect('emailMarketing')

    else:
        form = EmailSelectForm()

    context = {
        'title': 'Email Marketing',
        'form': form
    }

    return render(request, 'crm/main/marketing/email-marketing.html', context)

# SMS Marketing
@login_required(login_url='signIn')
@admin_role_required
def smsMarketing(request):
    try:
        settings = websiteSetting.objects.first()
        account_sid = str(settings.twilio_sid)
        auth_token = str(settings.twilio_auth_token)
        from_number = str(settings.twilio_from_number)

        client = Client(account_sid, auth_token)
    except AttributeError:
        messages.error(request, 'Twilio settings are not properly configured.')
        return redirect('smsMarketing')

    if request.method == "POST":
        numbers = request.POST.get('numbers', '')
        message = request.POST.get('message', '')

        if not numbers or not message:
            messages.warning(request, 'Numbers and message are required')
            return redirect('smsMarketing')

        phone_numbers = numbers.split(',')

        status_list = []

        successful_numbers = []
        failed_numbers = []

        for number in phone_numbers:
            try:
                message = client.messages.create(
                    to=number.strip(), 
                    from_=from_number,
                    body=message
                )
                successful_numbers.append(number)
            except Exception as e:
                failed_numbers.append(number)

        if successful_numbers:
            messages.success(request, f'SMS sent to {", ".join(successful_numbers)}')

        if failed_numbers:
            messages.warning(request, f'SMS sent failed for {", ".join(failed_numbers)}')

        return redirect('smsMarketing')

    return render(request, 'crm/main/marketing/sms-marketing.html')

@login_required(login_url='signIn')
def emailFormator(request):

    context ={
        'title' : 'Email Formator'
    }
    return render(request, 'crm/main/marketing/email-formator.html', context)

@login_required(login_url='signIn')
def numberFormator(request):

    context ={
        'title' : 'Number Formator'
    }
    return render(request, 'crm/main/marketing/number-formator.html', context)


# ====================Error Page====================
def error_404(request, exception):
    return render(request, 'error/error_404.html', status=404)

def error_500(request):
    return render(request, 'error/error_500.html', status=500)