from django import forms
from .models import CustomerData

class ChangeSubscription(forms.ModelForm):
    id = forms.CharField()
 
    class Meta:
        model = CustomerData
        fields = ['data']