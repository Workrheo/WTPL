from django import forms 
from order.models import Order

# Order status form
class orderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-select select2'
        