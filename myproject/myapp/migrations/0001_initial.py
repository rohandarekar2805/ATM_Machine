# Generated by Django 5.1.1 on 2024-12-18 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=12, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pin', models.CharField(max_length=4)),
            ],
        ),
    ]
