# Generated by Django 2.1.3 on 2019-02-04 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0010_auto_20190203_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeprofile',
            name='staff_key',
            field=models.CharField(default='x4713a334', max_length=100),
        ),
        migrations.AlterField(
            model_name='historicalemployeeprofile',
            name='staff_key',
            field=models.CharField(default='x4713a334', max_length=100),
        ),
    ]
