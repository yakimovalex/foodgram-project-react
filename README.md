# Foodgram - Продуктовый помощник

http://foodg.sytes.net/
Email-адрес: admin@ya.ru
Логин: admin
Password: admin


## Описание проекта Foodgram
Дает возможность записывать, публиковать и делиться своими кулинарными рецептами, добавлять в свое избранное понравившиес рецепты и подписываться на других авторов. А сервис "список покупок" поможет создать списко продуктов к покупке для приготовления выбранных рецептов.

#### Стек технологий:
 **Python 3.9,
 [Django 3.2.9](https://docs.djangoproject.com/en/4.0/),
 [DjangoRestFramework](https://www.django-rest-framework.org),
 [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/),
 [PostgreSQL](https://www.postgresql.org/docs/),
 [Docker](https://docs.docker.com/),
 [Docker Compose](https://docs.docker.com/compose/),
 [Gunicorn](https://docs.gunicorn.org/en/stable/) 20.0,
 [Nginx](https://docs.nginx.com/) 1.21 ([Ru](https://nginx.org/ru/docs/)).**

## Запуск

Все действия мы будем выполнять в Docker, docker-compose как на локальной машине так и на сервере ВМ Yandex.Cloud. Предварительно установим на ВМ в облаке необходимые компоненты для работы:

# username - ваш логин, ip - ip ВМ под управлением Linux Дистрибутива с пакетной базой deb.
ssh username@ip
sudo apt update && sudo apt upgrade -y && sudo apt install curl -y
sudo curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh && sudo rm get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo systemctl start docker.service && sudo systemctl enable docker.service
Всё, что нам нужно, установлено, далее, создаем папку /infra в домашней директории /home/username/:

cd ~
mkdir infra
Предварительно из папки /backend и /frontend загрузим актуальные данные на DockerHub (на вашем ПК):

docker login -u yaalex
cd backend
docker build -t yaalex/foodgrambackend:latest .
docker push yaalex/foodgrambackend:latest
cd ..
cd frontend
docker build -t yaalex/foodgramfrontend:latest .
docker push yaalex/foodgramfrontend:latest
Перенести файлы docker-compose.yml и default.conf на сервер, из папки infra в текущем репозитории (на вашем ПК).

cd infra
scp docker-compose.yml username@server_ip:/home/username/
scp default.conf username@server_ip:/home/username/
Так же, создаем файл .env в директории infra на ВМ:

touch .env
Заполнить в настройках репозитория секреты .env

DB_ENGINE='django.db.backends.postgresql'
POSTGRES_DB='postgres' # Задаем имя для БД.
POSTGRES_USER='postgres' # Задаем пользователя для БД.
POSTGRES_PASSWORD='postgres' # Задаем пароль для БД.
DB_HOST='db'
DB_PORT='5432'
SECRET_KEY='secret'  # Задаем секрет.
ALLOWED_HOSTS='127.0.0.1, backend' # Вставляем свой IP сервера.
DEBUG = False
На этом настройка закончена, далее в папке infra выполняем команду:

sudo docker-compose up -d --build
Проект запустится на ВМ и будет доступен по указанному вами адресу либо IP. Завершение настройки на ВМ:

В папке infra выполняем команду, что бы собрать контейнеры:

Остановить:

sudo docker-compose stop
Удалить вместе с volumes:

# Все данные удалятся!
sudo docker-compose down -v
Для доступа к контейнеру web и сборки финальной части выполняем следующие команды:

sudo docker-compose exec web python manage.py makemigrations
sudo docker-compose exec web python manage.py migrate --noinput
sudo docker-compose exec web python manage.py createsuperuser
sudo docker-compose exec web python manage.py collectstatic --no-input
Дополнительно можно наполнить DB ингредиентами и #тэгами:

#sudo docker-compose exec web python manage.py load_tags
sudo docker-compose exec web python manage.py importdata
На этом всё, продуктовый помощник запущен, можно наполнять его рецептами и делится с друзьями!

Запуск проекта в Docker на localhost
Для Linux ставим Docker как описано выше, для Windows устанавливаем актуальный Docker Desktop.

В папке infra выполняем команду, что бы собрать контейнеры:

sudo docker-compose up -d --build
Остановить:

sudo docker-compose stop
Удалить вместе с volumes:

# Все данные удалятся!
sudo docker-compose down -v
Для доступа к контейнеру выполняем следующие команды:

sudo docker-compose exec web python manage.py makemigrations
sudo docker-compose exec web python manage.py migrate --noinput
sudo docker-compose exec web python manage.py createsuperuser
sudo docker-compose exec web python manage.py collectstatic --no-input
Дополнительно можно наполнить DB ингредиентами и тэгами:

sudo docker-compose exec web python manage.py load_tags
sudo docker-compose exec web python manage.py load_ingrs
При необходимости, но не обязательно, создаем базу и пользователя в PostgreSql (если будет необходимость запустить без Docker):

sudo -u postgres psql
CREATE DATABASE basename;
CREATE USER username WITH ENCRYPTED PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE basename TO username;
Документация к API доступна после запуска
http://127.0.0.1/api/docs/