# Generated by Django 5.0.3 on 2024-05-05 07:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_remove_inventoryitem_domain_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventoryitem',
            name='department',
        ),
        migrations.AddField(
            model_name='person',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.department'),
        ),
    ]
