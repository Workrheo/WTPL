from django import forms
from settings.models import *




# Admin Settings Forms
class WebsiteSettingsForm(forms.ModelForm):
    class Meta:
        model = websiteSetting
        fields = '__all__'
        exclude = ['openai_api', 'max_token', 'is_enabled_for_user']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget = forms.CheckboxInput(attrs={'class': 'switch-input'})
            else:
                field.widget.attrs['class'] = 'form-control'


            
            