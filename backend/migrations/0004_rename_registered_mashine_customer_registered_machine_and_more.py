# Generated by Django 4.2 on 2024-12-02 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_customer_registered_mashine'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='registered_mashine',
            new_name='registered_machine',
        ),
        migrations.RenameField(
            model_name='machine',
            old_name='mashine_id',
            new_name='machine_id',
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]