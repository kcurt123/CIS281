# Generated by Django 5.0.3 on 2024-05-05 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_alter_person_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventoryitem',
            name='barcode',
        ),
    ]