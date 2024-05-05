from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

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

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    other_identifier = models.CharField(max_length=100, blank=True, null=True)
    domain_user = models.CharField(max_length=101, blank=True) 
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.domain_user:
            initial = self.first_name[0].upper() if self.first_name else ''
            last_name_capitalized = self.last_name.capitalize() if self.last_name else ''
            self.domain_user = f"{initial}{last_name_capitalized}"
        super().save(*args, **kwargs)  

    class Meta:
        verbose_name = 'person'
        verbose_name_plural = 'persons'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    website = models.TextField(blank=True)
    contact_info = models.TextField(blank=True)  

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    pc_name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, default='')
    device_type = models.CharField(max_length=50, default='Laptop')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    costs = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    new_computer = models.BooleanField(default=False)
    date_delivered = models.DateTimeField(blank=True, null=True, default=timezone.now)
    is_computer = models.BooleanField(default=False)  
    has_dock = models.BooleanField(default=False)
    has_lcd = models.BooleanField(default=False)
    has_lcd2 = models.BooleanField(default=False)
    has_stand = models.BooleanField(default=False)
    has_keyboard = models.BooleanField(default=False)
    has_cd = models.BooleanField(default=False)
    serial_number = models.CharField(max_length=200)
    model_number = models.CharField(max_length=200, null=True)
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
    checked_out_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='checked_out_by')
    checked_out_to = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, related_name='checked_out_to')
    returned = models.BooleanField(default=False)

    def mark_as_returned(self):
        self.returned = True
        self.checked_out_to = None  # Clearing the person
        self.save()

    def get_department(self):
        return self.checked_out_to.department if self.checked_out_to else "No Department"

    def __str__(self):
        person_name = self.checked_out_to if self.checked_out_to else "Unknown"
        person_domain_user = self.checked_out_to.domain_user if self.checked_out_to else "None"
        item_name = self.item.pc_name if self.item else "No Item"
        return f"{item_name} checked out to {person_name}"

@receiver(post_save, sender=Checkout)
def update_last_checked_out_details(sender, instance, created, **kwargs):
    if created:  # This ensures the action happens only on creation of a new Checkout
        item = instance.item
        item.last_checked_out_at = instance.checked_out_at
        item.last_checked_out_by = instance.checked_out_by
        item.save()
