from django import forms
from rest_framework.authtoken.models import Token

class RefreshDeleteApiKeyForm(forms.ModelForm):
    key = forms.CharField(label='', disabled=True, required=False, max_length=40)
    class Meta:
        model = Token
        fields = ['key', ]
