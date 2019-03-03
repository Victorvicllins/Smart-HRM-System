# Generated by Django 2.1.3 on 2019-02-03 18:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0009_auto_20190203_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyprofile',
            name='company_url',
            field=models.UUIDField(default=uuid.UUID('08ed6af1-281f-4767-b4c0-0c884a8a6ae9'), editable=False),
        ),
        migrations.AlterField(
            model_name='historicalcompanyprofile',
            name='company_url',
            field=models.UUIDField(default=uuid.UUID('08ed6af1-281f-4767-b4c0-0c884a8a6ae9'), editable=False),
        ),
    ]
