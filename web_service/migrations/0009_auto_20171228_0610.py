# Generated by Django 2.0 on 2017-12-28 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_service', '0008_auto_20171227_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmerdetails',
            name='activity',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activity_farmer', to='web_service.Activity'),
        ),
    ]
