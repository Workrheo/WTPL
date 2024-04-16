from django.shortcuts import render, redirect, get_object_or_404
from authapp.models import *
from adminapp.forms import *
from crm.models import *
from settings.models import *
from legals.models import agreement
from legals.forms import agreementStatusForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from core.decorators import admin_role_required, both_role_required
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from legals.models import agreementSettings

# Agreement Data Admin
@login_required(login_url='signIn')
@admin_role_required
def agreementSubmissonsAdmin(request):
    agreement_data = agreement.objects.all()
    context = {
        'title' : 'Agreement Submissions',
        'agreement_data' : agreement_data
    }
    return render(request, 'crm/main/agreements/index.html', context)

@login_required(login_url='signIn')
@admin_role_required
def agreementDeleteAdmin(request, id):
    single_data = get_object_or_404(agreement, id=id)
    single_data.delete()
    messages.warning(request, 'Deleted successfully!')
    return redirect('agreementSubmissonsAdmin')

@login_required(login_url='signIn')
@admin_role_required
def agreementDetailAdmin(request, id):
    detail_data = get_object_or_404(agreement, id=id)
    a_settings = agreementSettings.objects.first()
    if request.method == 'POST':
        form = agreementStatusForm(request.POST, instance=detail_data)
        if form.is_valid():
            form.save()

            # Send approval confirmation email
            if detail_data.is_approved:  # Check if the agreement is approved
                web_settings = websiteSetting.objects.first()
                subject = 'Agreement Approval Confirmation'
                from_email = f'"{web_settings.name}" <{settings.DEFAULT_FROM_EMAIL}>'
                
                # Render the HTML email template
                html_message = render_to_string('admin/front/main/email/agreement_confirmation.html', {
                    'data': detail_data,
                    'settings': web_settings,
                })

                # Send the HTML email
                email_message = EmailMessage(
                    subject=subject,
                    body=html_message,
                    from_email=from_email,
                    to=[detail_data.email],
                )
                email_message.content_subtype = 'html'
                email_message.send()
            messages.success(request, 'Updated successfully!')
            return redirect('agreementDetailAdmin', id=detail_data.id)
    else:
        form = agreementStatusForm(instance=detail_data)
        
    context = {
        'title' : 'Agreement Details',
        'data': detail_data,
        'form': form,
        'a_settings' : a_settings,
    }
    return render(request, 'crm/main/agreements/view.html', context)

# Admin Settings
@login_required(login_url='signIn')
@admin_role_required
def adminWebsiteSettings(request):
    settings = websiteSetting.objects.first()
    if request.method == 'POST':
        settingForm = WebsiteSettingsForm(request.POST, request.FILES, instance=settings)
        if settingForm.is_valid():
            settingForm.save()
            messages.success(request, 'System settings updated successfully!')
            return redirect('websiteSettingsadm')
    else:
        settingForm = WebsiteSettingsForm(instance=settings)
        
    context = {
        'title': 'Website Settings',
        'settings': settings,
        'settingForm': settingForm,
        'form': settingForm,
    }
    return render(request, 'crm/main/settings/website.html', context)


# ====================Error Page====================
def error_404(request, exception):
    return render(request, 'error/error_404.html', status=404)

def error_500(request):
    return render(request, 'error/error_500.html', status=500)