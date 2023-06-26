# Backend

Бэкенд для веб-интерфейса ChatGPT.

## Требования

* [Docker](https://docs.docker.com/)
* [docker-compose](https://docs.docker.com/compose/)

## Сборка и запуск

```bash
$ cd backend
$ cp .env.example .env
$ docker network create gpt-net
$ docker-compose build
$ docker-compose up
```

API доступно на localhost:8080. Документация: localhost:8080/redoc.
