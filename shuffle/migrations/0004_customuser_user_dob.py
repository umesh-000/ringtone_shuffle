# Generated by Django 4.2.16 on 2024-10-01 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shuffle', '0003_remove_ringtone_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_dob',
            field=models.DateField(blank=True, null=True),
        ),
    ]
