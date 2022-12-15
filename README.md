# Восьмая команда джангистов
Проект: ---
___
# Роли в команде:
- Николай Павлов - ментор
- Евгений Перов - тимлид
- Дивиров Арсен - модель пользователя, авторизация, бэкэнд просмотра сочинений
- Надежда Тарасенко - модели для сочинения, модель оценки, фронтенд просмотра сочинений (лента, полные сочинения)
___
# Установка

**1. Клонировать репозиторий**

```
git clone https://github.com/aeonva1ues/eighth_team_project.git 
```

**2. Создать и активировать виртуальное окружение**

```
python -m venv venv
.\venv\Scripts\activate
```

**3. Установить зависимости**

```
pip install -r requirements.txt
```

**4. Создать .env файл в папке essay_practice и занести в него:**

```
SECRET_KEY = writesecretkeythere
DEBUG = writeTrueorFalse
ALLOWED_HOSTS = address1 address2 address3 addressN
```

**5. Перенос тем из csv в бд**

```
python manage.py parse_topic_csv
```

**6. Запуск**

```
cd essay_practice
python manage.py runserver
```
