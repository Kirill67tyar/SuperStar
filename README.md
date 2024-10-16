
# SuperStars

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

## Сайт доступен по адресу: 
https://super-stars.online

## Инструкция как развернуть в докере

У вам есть возможность развернуть проект в Docker через конфиг для Docker Compose:
```
1. Клонируйте репозиторий к себе на компьютер

   git clone https://github.com/Kirill67tyar/SuperStar.git
   
   или

   git clone git@github.com:Kirill67tyar/SuperStar.git

2. Находясь в корневой директории проекта введите команду:

   sudo docker compose up -d --build

3. Проверьте, что все нужные контейнеры запущены (должны быть запущены контейнеры):

   sudo docker compose ps

4. После того как проект развернулся на вашем компьютере, соберите статику django:

   sudo docker compose exec backend python manage.py collectstatic

5. Копируйте статику:

   sudo docker compose exec backend cp -r /app/collected_static/. /backend_static/static/

6. Примените миграции:

   sudo docker compose exec backend python manage.py migrate

7. Загрузите фикстуры:

   sudo docker compose exec backend python manage.py loaddata fixtures/db_data.json
```


## __Установка на локальном компьютере__
1. Клонируйте репозиторий:
    ```
    git clone https://github.com/Kirill67tyar/SuperStar.git
    ```
    или
    ```
     git clone git@github.com:Kirill67tyar/SuperStar.git
    ```
2. Установите и активируйте виртуальное окружение:
    ```
    python3 -m venv venv
    source venv/Scripts/activate  - для Windows
    source venv/bin/activate - для Linux
    ```
3. Установите зависимости:
    ```
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```
4. Выполните миграции:
    ```
    python manage.py migrate
    ```
5. Загрузите фикстуры:
    ```
    python manage.py loaddata fixtures/fixtures/db_data.json
    ```
6. Создайте суперпользователя:
    ```
    python manage.py createsuperuser
    ```
7. Соберите статику  (нужно для swagger):
    ```
    python manage.py collectstatic
    ```
8. Запустите проект:
    ```
    python manage.py runserver
    ```
## Стек технологий

#### для backend:
Python 3.9
PostgreSQL 13
Gunicorn 20.1.0
Nginx 1.22.1

#### для frontend
Node.js 13.12.0

#### для развёртывания на компьютере
Docker 26.1.1
Docker Compose 3

### Авторство

[Кирилл Богомолов](https://github.com/Kirill67tyar).