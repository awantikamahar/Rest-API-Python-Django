# Generated by Django 2.0 on 2018-01-10 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_service', '0023_auto_20180110_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='start_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='dealerform',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='dealerform',
            name='safety_deposit_ammount',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='items',
            name='discount_amount',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='items',
            name='rate',
            field=models.FloatField(null=True),
        ),
    ]
