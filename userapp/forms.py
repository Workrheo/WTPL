from django import forms
from userapp.models import *
from authapp.models import UserProfile
from django.contrib.auth.forms import PasswordChangeForm
from legals.models import agreement

# Support Ticket User Form
class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = supportTicket
        exclude = ['client','status']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-select select2'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description', 'rows' : 4}),
            'priority': forms.Select(attrs={'class': 'form-select select2'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # We get the user from kwargs
        super(SupportTicketForm, self).__init__(*args, **kwargs)
        self.fields['project'].queryset = crmProjects.objects.filter(client=user)

# Support Ticket Status Change Form
class SupportTicketStatusForm(forms.ModelForm):
    class Meta:
        model = supportTicket
        fields = ['status']
        
        widgets = {
            'status' : forms.Select(attrs={'class': 'form-select'})
        }
        
# Support Ticket Reply Form
class ReplyForm(forms.ModelForm):
    class Meta:
        model = TicketReply
        fields = ['reply']
        
        widgets = {
            'reply' : forms.Textarea(attrs={'class' : 'form-control', 'rows' : 4, 'placeholder' : 'Enter you reply'})
        }

# User Profile Related Form

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'name', 'email', 'phone', 'address', 'city', 'state', 'country', 'zipcode', 'facebook', 'instagram', 'linkedin']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'placeholder': 'Enter your current password' , 'class' : 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'placeholder': 'Enter your new password', 'class' : 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'placeholder': 'Confirm your new password', 'class' : 'form-control'})
        

class agreementSignForm(forms.ModelForm):
    class Meta:
        model = agreement
        fields = ['service','name','phone','email','address','city','state','postal','is_signed']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-select select2','required': 'required'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your phone number', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email', 'required': 'required'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your address', 'required': 'required'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your city', 'required': 'required'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your state', 'required': 'required'}),
            'postal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your postal code', 'required': 'required'}),
            'is_signed': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': 'required'}),
        }