# Generated by Django 5.0.3 on 2024-05-05 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0015_remove_inventoryitem_barcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryitem',
            name='model_number',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
