from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Category, InventoryItem

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class InventoryItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0)
    # Assuming the barcode can be optionally provided, you can include it like this:
    barcode = forms.CharField(max_length=200, required=False, widget=forms.HiddenInput())

    class Meta:
        model = InventoryItem
        fields = ['name', 'quantity', 'category', 'barcode', 'location', 'supplier', 'notes']
