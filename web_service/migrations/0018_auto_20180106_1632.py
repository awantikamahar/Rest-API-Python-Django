# Generated by Django 2.0 on 2018-01-06 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_service', '0017_appliedleave_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='description',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='end_time',
            field=models.TimeField(null=True),
        ),
    ]
