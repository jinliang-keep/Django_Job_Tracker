# Generated by Django 5.2.3 on 2025-06-29 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_job_delete_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='data_applied',
            new_name='date_applied',
        ),
    ]
