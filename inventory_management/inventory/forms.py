from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Department, Supplier, InventoryItem, Checkout

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class InventoryItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), required=False)

    class Meta:
        model = InventoryItem
        fields = ['pc_name', 'domain_user', 'user', 'notes', 'department', 'device_type', 'costs', 'new_computer', 'date_delivered', 'is_computer', 'has_dock', 'has_lcd', 'has_lcd2', 'has_stand', 'has_keyboard', 'has_cd', 'serial_number', 'model_number', 'is_checked_out', 'last_checked_out_by', 'last_checked_out_at']

class CheckoutForm(forms.ModelForm):
    checked_out_to = forms.ModelChoiceField(queryset=User.objects.all(), required=True)
    
    class Meta:
        model = Checkout
        fields = ['item', 'user', 'checked_out_by', 'checked_out_to']
