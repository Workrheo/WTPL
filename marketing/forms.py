from django import forms
from authapp.models import User
from ckeditor.widgets import CKEditorWidget

class EmailSelectForm(forms.ModelForm):
    select_all = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role=User.Role.Guser),
        widget=forms.SelectMultiple(),
        required=False
    )
    subject = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=CKEditorWidget())
    manually_added_emails = forms.CharField(
        label="Manually Add Emails (comma-separated)",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder' : 'email1@gmail.com,email2@gmail.com,email3@gmail.com', 'rows' : 3})
    )

    class Meta:
        model = User
        fields = ['select_all', 'users', 'manually_added_emails', 'subject', 'message']