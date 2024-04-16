from django.shortcuts import render, redirect
from legals.models import *
from legals.forms import *
from django.contrib.auth.decorators import login_required
from core.decorators import admin_role_required
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.core.mail import EmailMessage
from settings.models import websiteSetting
from django.template.loader import render_to_string
from core.decorators import *

# Agreement Page Front
@login_required(login_url='signIn')
def signAgreement(request):
    if request.method == 'POST':
        form = agreementForm(request.POST)
        if form.is_valid():
            new_agreement = form.save(commit=False)
            new_agreement.client = request.user
            new_agreement.save()

            # Email content
            terms_page_url = request.build_absolute_uri(reverse('termsPageFront'))
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
            return redirect('signAgreement')
    else:
        form = agreementForm()
    
    context = {
        'title': 'Sign Agreement',
        'form': form
    }
    return render(request, 'front/main/agreement.html', context)

@login_required(login_url='signIn')
@admin_role_required
def settingsView(request):
    agreesettings = agreementSettings.objects.first()
    
    if request.method == 'POST':
        form = settingFormAgree(request.POST, instance=agreesettings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated successfully!')
            return redirect('settingsView')
    else:
        form = settingFormAgree(instance=agreesettings)
    
    context = {
        'title' : 'Agreement Settings',
        'form' : form,
        'agreesettings' : agreesettings,
    }
    
    return render(request, 'crm/main/agreements/settings.html', context)
        
# ====================Error Page====================
def error_404(request, exception):
    return render(request, 'error/error_404.html', status=404)

def error_500(request):
    return render(request, 'error/error_500.html', status=500)