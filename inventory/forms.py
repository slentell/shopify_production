from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Inventory

class ItemForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['name', 'description', 'price', 'quantity', 'storage_location']

class DeleteForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['deletion_comment']
    

    
