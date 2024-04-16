from django import forms
from legals.models import *

# Agreement Form
class agreementForm(forms.ModelForm):
    class Meta:
        model = agreement
        fields = ['name','phone','email','address','city','state','postal','is_signed']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your phone number', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email', 'required': 'required'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your address', 'required': 'required'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your city', 'required': 'required'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your state', 'required': 'required'}),
            'postal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your postal code', 'required': 'required'}),
            'is_signed': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': 'required'}),
        }
        
class agreementStatusForm(forms.ModelForm):
    class Meta:
        model = agreement
        fields = ['is_approved']
        widgets = {
            'is_approved' : forms.CheckboxInput(attrs={'class' : 'switch-input'}),
        }

class settingFormAgree(forms.ModelForm):
    class Meta:
        model = agreementSettings
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'