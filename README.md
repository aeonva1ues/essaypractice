# Восьмая команда джангистов
Проект: ---
___
# Роли в команде:
- Николай Павлов - ментор
- Евгений Перов - тимлид
- Дивиров Арсен - модель пользователя, авторизация
- Надежда Тарасенко -
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

**4. Создать .env файл в папке _тут будет папка_ и занести в него:**

```
SECRET_KEY = writesecretkeythere
DEBUG = writeTrueorFalse
ALLOWED_HOSTS = address1 address2 address3 addressN
```

**5. Запуск**

```
cd тутбудетпапка
python manage.py runserver
```
