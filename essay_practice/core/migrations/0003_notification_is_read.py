# Generated by Django 3.2.4 on 2023-01-14 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_notification_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='is_read',
            field=models.BooleanField(default=False, verbose_name='прочитано'),
        ),
    ]
