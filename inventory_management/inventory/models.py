from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_info = models.TextField(blank=True)  

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)  
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True)  
    notes = models.TextField(blank=True)  
	# if a new field is to be created, create it then in the command line run "python3 manage.py makemigrations"
	#																		  "python3 manage.py migrate"																		

    def __str__(self):
        return self.name