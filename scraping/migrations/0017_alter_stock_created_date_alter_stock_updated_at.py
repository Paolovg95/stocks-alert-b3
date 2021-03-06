# Generated by Django 4.0.4 on 2022-06-02 23:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0016_delete_alarmstock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='stock',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
