# База знаний
Backend базы знаний для хранения информации о всех знаниях по обучению для тьюторов 

## Содержание
- [Технологии](#Технологии)
- [Структура](#Структура)
- [Начало работы](#Начало-работы)

## Технологии
- [FAST API](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Minio]

## Структура
```sh
src
...
...
```

## Начало работы

### Первая сборка и запуск
Для запустка потребуется [Docker](https://www.docker.com/) 

Склонируйте репозиторий себе на ПК с помощью команды: 
```sh
$ git clone ...
```

Создать файл .env по примеру 

```sh
#Main
URL_FRONT=<http://localhost:8000> #URL фронта

#Postgres
POSTGRES_HOST=<postgres> #Название контейнера в Docker
POSTGRES_PORT=<5432> #Порт по умолчанию
POSTGRES_USER=<postgres> #Пользователь
POSTGRES_PASSWORD=<postgres> #Пароль
POSTGRES_DB=<postgres> #Название базы данных

#Minio
MINIO_ROOT_USER=<minioadmin> #Логин для входа в minio
MINIO_ROOT_PASSWORD=<minioadmin> #Пароль для входа в minio
MINIO_URL=<http://localhost:9000> #URL minio
MINIO_BUCKET_NAME=<test> #Название бакета


#Pgadmin
PGADMIN_DEFAULT_EMAIL=<admin@example.com> #Логин для входа в pgadmin
PGADMIN_DEFAULT_PASSWORD=<admin> #Пароль для входа в pgadmin
```


Соберите и запустите проект с помощью docker:
```sh
$ docker-compose up -d
```

Чтобы создать таблицы в базе данных и бакет в Minio
```sh
$ docker exec server_knowledge_base make first-start
```

### API

Документация API http://localhost:8000/docs#
Web-интерфейс файлового хранилища http://localhost:9001
Web PgAdmin http://localhost:8001