# Generated by Django 4.2 on 2024-12-02 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('location', models.CharField(blank=True, max_length=50, null=True)),
                ('type', models.TextField(choices=[('General Population', 'General Population'), ('Client Group', 'Client Group')], max_length=200)),
                ('client_group', models.TextField(blank=True, choices=[('FSW', 'FSW'), ('MSM', 'MSM'), ('PWID,', 'PWID,'), ('MAT,', 'MAT,'), ('AGYW,', 'AGYW,')], max_length=200, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=50, null=True)),
                ('age', models.CharField(blank=True, max_length=50, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('mashine_id', models.CharField(max_length=50, unique=True)),
                ('location', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('product_type', models.CharField(blank=True, choices=[('Condoms', 'Condoms'), ('Kits', 'Kits')], max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.customer')),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.machine')),
            ],
        ),
    ]