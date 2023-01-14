# Generated by Django 3.2.4 on 2023-01-14 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('essayfeed', '0003_alter_commentreport_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='essay_report',
            options={'verbose_name': 'жалоба на сочинение', 'verbose_name_plural': 'жалобы на сочинения'},
        ),
        migrations.AlterField(
            model_name='essay_report',
            name='reason',
            field=models.IntegerField(choices=[(0, 'Оффтоп/Спам'), (1, 'Пропаганда/Реклама'), (2, 'Нецензурная лексика'), (3, 'Плагиат')], verbose_name='нарушение'),
        ),
    ]