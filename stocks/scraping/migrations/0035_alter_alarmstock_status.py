# Generated by Django 4.0.4 on 2022-06-06 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0034_alter_alarmstock_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarmstock',
            name='status',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
