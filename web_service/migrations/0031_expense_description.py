# Generated by Django 2.0 on 2018-01-13 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_service', '0030_auto_20180113_1217'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
