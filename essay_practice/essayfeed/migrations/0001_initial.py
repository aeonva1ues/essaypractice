# Generated by Django 3.2.4 on 2022-12-22 06:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('writing', '0004_alter_essay_mentors_email'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Essay_Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.IntegerField(choices=[(0, 'Оффтоп/Спам'), (1, 'Пропаганда/Реклама'), (2, 'Нецензурная лексика')], verbose_name='нарушение')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sended_reports', to=settings.AUTH_USER_MODEL, verbose_name='оставлена пользователем')),
                ('to_essay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='writing.essay', verbose_name='сочинение с нарушением')),
            ],
            options={
                'verbose_name': 'жалоба',
                'verbose_name_plural': 'жалобы',
            },
        ),
    ]
