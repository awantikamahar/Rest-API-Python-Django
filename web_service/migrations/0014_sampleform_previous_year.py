# Generated by Django 2.0 on 2018-01-03 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_service', '0013_auto_20180103_0718'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleform',
            name='previous_year',
            field=models.DateField(null=True),
        ),
    ]
