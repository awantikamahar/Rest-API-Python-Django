# Generated by Django 2.0 on 2018-02-01 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_service', '0042_salaryrequest_credited'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
