# Generated by Django 4.2 on 2024-12-07 17:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0008_customer_pin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district', models.CharField(blank=True, max_length=100, null=True, verbose_name='District Supporting Ward')),
                ('ward', models.CharField(blank=True, max_length=100, null=True, verbose_name='Supporting Ward')),
                ('hfrcode', models.CharField(blank=True, max_length=15, null=True, verbose_name='HFR Code')),
                ('supporting_facility', models.CharField(blank=True, max_length=100, null=True, verbose_name='Supporting Facility')),
                ('responsible_cso', models.CharField(blank=True, max_length=100, null=True, verbose_name='Responsible CSO')),
                ('responsible_person', models.CharField(blank=True, max_length=100, null=True, verbose_name='Responsible Person')),
                ('mobile_no', models.CharField(blank=True, max_length=15, null=True, verbose_name='Mobile Number')),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('machine', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.machine')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'District Support',
                'verbose_name_plural': 'District Supports',
                'ordering': ['district', 'ward'],
            },
        ),
    ]