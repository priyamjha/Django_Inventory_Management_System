from django import forms
from .models import *

class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'amount']


class UpdateItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name']
        
        
class IssueItemForm(forms.ModelForm):
    class Meta:
        model = IssueItem
        fields = ['item', 'issued_amount', 'issued_to', 'department', 'return_date']
        
        
class ReturnItemForm(forms.ModelForm):
    class Meta:
        model = ReturnItem
        fields = ['item','returned_amount' ,'returned_by']
        
        
class RestockItemForm(forms.ModelForm):
    class Meta:
        model = RestockItem
        fields = ['item', 'amount']