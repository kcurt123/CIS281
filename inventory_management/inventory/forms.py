from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Department, Supplier, InventoryItem, Checkout, Person

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class InventoryItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), required=False)
    pc_name = forms.CharField(label='PC Name') 
    serial_number = forms.CharField(required=False, label='Serial Number') 
    model_number = forms.CharField(required=False, label='Model Number')  
    device_type = forms.CharField(required=False, label='Device Type')  
    Category = forms.CharField(required=False, label='Category')  


    class Meta:
        model = InventoryItem
        fields = [
            'pc_name', #'domain_user', 'department',
            'notes',  'device_type',
            'costs', 'date_delivered', 'serial_number', 'model_number', 'supplier', 
            'category', 'is_computer', 'new_computer', 'has_dock', 'has_lcd', 'has_lcd2', 
            'has_stand', 'has_keyboard', 'has_cd', 'last_checked_out_at'
        ]

class CheckoutForm(forms.ModelForm):
    checked_out_to = forms.ModelChoiceField(queryset=Person.objects.all(), required=True)

    class Meta:
        model = Checkout
        fields = ['item', 'checked_out_by', 'checked_out_to']

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'other_identifier']   