# Generated by Django 2.1.3 on 2019-02-03 18:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0008_auto_20190203_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyprofile',
            name='company_url',
            field=models.UUIDField(default=uuid.UUID('97d9f8d2-7219-4287-8d61-fdec7c997e47'), editable=False),
        ),
        migrations.AlterField(
            model_name='historicalcompanyprofile',
            name='company_url',
            field=models.UUIDField(default=uuid.UUID('97d9f8d2-7219-4287-8d61-fdec7c997e47'), editable=False),
        ),
    ]
