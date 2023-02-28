# Проект "Foodgram-project-react"
Проект/сайт для публикации рецептов. Авторизованные пользователи могут подписаться на избранных авторов, добавить рецепты в избранное, в список покупок.

## Запуск проекта в Docker контейнерах:
* Склонировать репозиторий на ВМ:
git clone https://github.com/AliaBis/foodgram-project-react
```
cd foodgram-project-react
```
* В папке infra заполните .env файл по приложенному образцу, убедитесь, что на вашей ВМ установлены Docker и Docker-compose
* Создайте и загрузите на свой аккаунт Docker Hub образы приложений проекта. В папках frontend и backend имеются соответствующие Dockerfile
* Отредактируйте в файле docker-compose.yml названия имидж файлов на собственные
* В файле nginx.conf укажите адрес или имя своего сервера
* В папке infra выполните команды:
```
docker-compose up -d
```
```
docker-compose exec backend python manage.py collectstatic --no-input`
```


```
docker-compose exec backend python manage.py migrate
```
```
docker-compose exec backend python manage.py createsuperuser
```

```
docker-compose exec backend python manage.py load_ingredients
```

### Проект запустится на адресе http://<Ваш адрес сервера>, увидеть спецификацию API вы сможете по адресу http://<Ваш адрес сервера>/api/docs/

## Для проекта настроена процедура CI/CD через Git Hub actions. Для получения доступа к этой возможности заполните необходимые секреты в своем репозитории:

* DOCKER_USERNAME - имя пользователя в DockerHub
* DOCKER_PASSWORD - пароль пользователя в DockerHub
* HOST - адрес сервера
* USER - пользователь
* SSH_KEY - приватный ssh ключ
* PASSPHRASE - кодовая фраза для ssh-ключа
* DB_ENGINE - django.db.backends.postgresql
* DB_NAME - postgres (по умолчанию)
* POSTGRES_USER - postgres (по умолчанию)
* POSTGRES_PASSWORD - postgres (по умолчанию)
* DB_HOST - db
* DB_PORT - 5432
* SECRET_KEY - секретный ключ приложения django
* TELEGRAM_TO - id своего телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
* TELEGRAM_TOKEN - токен бота (получить токен можно у @BotFather, /token, имя бота)

foodgram_workflow запускается после команды git push в ветку master вашего репозитория.

## Тестовые пользователи:
### Admin-zona
* имя: admin99 (суперюзер)
* Email: admin99@mail.ru
* Пароль: admin99261222

### User 1
* имя: Марина
* Email: mora@mail.ru
* Пароль: mora@mail.ru

### User 2
* имя: Вовка-воровка
* Email: vov4ik@mail.ru
* Пароль: вован88

Проект доступен по ссылке prorecipes.hopto.org  51.250.97.1
