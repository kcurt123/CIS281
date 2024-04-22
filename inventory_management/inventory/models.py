from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Department(models.Model):
    department = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'department'
        verbose_name_plural = 'departments'

    def __str__(self):
        return self.department

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    website = models.TextField(blank=True)
    contact_info = models.TextField(blank=True)  

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    pc_name = models.CharField(max_length=255)
    domain_user = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, default='')
    barcode = models.CharField(max_length=100, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    device_type = models.CharField(max_length=50, default='Laptop')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    costs = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    new_computer = models.BooleanField(default=False)
    date_delivered = models.DateTimeField(blank=True, null=True, default=timezone.now)
    is_computer = models.BooleanField(default=False)  # True for computer, False for laptop
    has_dock = models.BooleanField(default=False)
    has_lcd = models.BooleanField(default=False)
    has_lcd2 = models.BooleanField(default=False)
    has_stand = models.BooleanField(default=False)
    has_keyboard = models.BooleanField(default=False)
    has_cd = models.BooleanField(default=False)
    serial_number = models.CharField(max_length=200)
    model_number = models.CharField(max_length=200)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    is_checked_out = models.BooleanField(default=False)
    last_checked_out_by = models.ForeignKey(User, related_name='last_checked_out_items', on_delete=models.SET_NULL, null=True, blank=True)
    last_checked_out_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        permissions = [
            ("can_checkout_items", "Can check out items"),
        ]

    def __str__(self):
        return self.pc_name

class Checkout(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='checkouts')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='checkouts')
    checked_out_at = models.DateTimeField(auto_now_add=True)
    checked_out_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='checked_out_by_user')
    checked_out_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='checked_out_to_user')
    returned = models.BooleanField(default=False)

    def __str__(self):
        user_name = self.user.username if self.user else "Unknown"
        item_name = self.item.pc_name if self.item else "No Item"
        return f"{item_name} checked out to {user_name}"
