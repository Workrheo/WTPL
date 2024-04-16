from django import forms 
from settings.models import websiteSetting, paymentMethod

class openaiSettingsForm(forms.ModelForm):
    class Meta: 
        model = websiteSetting
        fields = ['openai_api', 'max_token', 'is_enabled_for_user']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget = forms.CheckboxInput(attrs={'class': 'switch-input'})
            else:
                field.widget.attrs['class'] = 'form-control'
            
class paymentMethodsForm(forms.ModelForm):
    class Meta:
        model = paymentMethod
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget = forms.CheckboxInput(attrs={'class': 'switch-input'})
            else:
                field.widget.attrs['class'] = 'form-control'
    