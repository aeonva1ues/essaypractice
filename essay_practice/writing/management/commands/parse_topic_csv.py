'''
Наполнение бд из csv файла
Использование: python manage.py parse_topic_csv
'''


import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from writing.models import Section, Topic


class Command(BaseCommand):
    help = 'Перенос тем из csv в бд'

    def get_sections_dict(self):
        '''
        Запрос на получение разделов
        '''
        sections = list(Section.objects.all())
        sections_dict = {}
        for section in sections:
            sections_dict[section.name] = section
        return sections_dict

    def handle(self, *args, **kwargs):
        '''
        Парсинг csv и перенос в бд одним запросом
        '''
        with open(
            settings.BASE_DIR / 'writing/management/topics.csv', 'r',
                encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter='=', quotechar='"')
            objs = []
            Section.objects.bulk_create([
                Section(
                    name='Духовно-нравственные ориентиры в жизни человека.'),
                Section(name='Семья, общество, Отечество в жизни человека.'),
                Section(name='Природа и культура в жизни человека.')
            ]
            )
            sections = self.get_sections_dict()
            for line in reader:
                objs.append(
                    Topic(name=line[0], section=sections[line[1]])
                )
        Topic.objects.bulk_create(objs)
        self.stdout.write('Перенос завершился успешно')
