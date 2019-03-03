# Generated by Django 2.1.3 on 2019-03-02 02:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0017_auto_20190228_0816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyprofile',
            name='company_url',
            field=models.UUIDField(default=uuid.UUID('70986d87-d8ae-48d2-8c92-15d1e28e473b'), editable=False),
        ),
        migrations.AlterField(
            model_name='historicalcompanyprofile',
            name='company_url',
            field=models.UUIDField(default=uuid.UUID('70986d87-d8ae-48d2-8c92-15d1e28e473b'), editable=False),
        ),
    ]
