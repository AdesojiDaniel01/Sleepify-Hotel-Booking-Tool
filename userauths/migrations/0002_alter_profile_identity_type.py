# Generated by Django 5.0.7 on 2024-09-21 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='identity_type',
            field=models.CharField(blank=True, choices=[('National Identification Number', 'National Identification Number'), ("Driver's License", "Driver's License"), ('International Passport', 'International Passport')], max_length=200, null=True),
        ),
    ]
