# Generated by Django 2.0 on 2017-12-28 06:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('web_service', '0009_auto_20171228_0610'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmerdetails',
            name='form_filled_on',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]