# Generated by Django 4.2.16 on 2024-10-03 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shuffle', '0005_customuser_city_customuser_is_all_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ringtone',
            name='play_times',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
