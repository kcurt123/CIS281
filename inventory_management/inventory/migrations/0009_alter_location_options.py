# Generated by Django 5.0.3 on 2024-03-30 23:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_location_alter_inventoryitem_location'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name': 'location', 'verbose_name_plural': 'locations'},
        ),
    ]
