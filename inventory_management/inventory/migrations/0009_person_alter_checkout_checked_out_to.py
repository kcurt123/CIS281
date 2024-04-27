# Generated by Django 5.0.3 on 2024-04-27 03:45

import django.db.models.deletion
from django.db import migrations, models


def set_checked_out_to_null(apps, schema_editor):
    Checkout = apps.get_model('inventory', 'Checkout')
    # Set checked_out_to to None for all existing Checkout records to avoid ForeignKey constraint failure
    Checkout.objects.update(checked_out_to=None)

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_alter_department_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('other_identifier', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.RunPython(set_checked_out_to_null, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='checkout',
            name='checked_out_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='checked_out_to_person', to='inventory.person'),
        ),
    ]

