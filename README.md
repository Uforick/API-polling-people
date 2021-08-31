# API-polling-people "API для системы опросов пользователей"

Проект API-polling-people "API для системы опросов пользователей" является backend-составляющей API для проведения опросов и тестирований. 

## В данном сервисе реализована возможность создавать вопросы с выбором одного ответа, выбором нескольких ответов, вводом ответа пользователем. 

### Какие технологии использовались:
- Python 3.8.5
- Git (GitHub repository)
- djangorestframework 
- drf-yasg (swagger/redoc)

### Установка и запуск - давайте начнем:
1. Клонируйте репозиторий с проектом 
```bash
git clone https://github.com/Uforick/API-polling-people.git
```
2. Создайте виртуальное окружение и загрузите requirements
```bash 
python -m venv venv
pip install -r requirements.txt 
```
3. Перейдите в папку проекта:
```bash 
cd polling_people/
```
4. Выполните миграции и создание супер-пользователя
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

5. Запустите локальный сервер
```bash
python manage.py runserver
```
---
После запуска проект будет доступен по адресу: http://127.0.0.1:8000/

Документация по API доступна по адресам:
redoc - http://127.0.0.1:8000/redoc/
swagger - http://127.0.0.1:8000/swagger/


Авторство github.com/Uforick
---
