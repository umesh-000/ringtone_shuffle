# Generated by Django 4.2.16 on 2024-11-12 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shuffle', '0007_rename_ringtone_year_ringtone_ringtone_year_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (0, 'Inactive')], default=1),
        ),
    ]