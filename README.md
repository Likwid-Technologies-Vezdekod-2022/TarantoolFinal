# TarantoolFinal

Для запуска требуются `docker` и `docker-compose`

## Демонстраци работы

Приложение доступно по адресу: [http://tarantool.bolanebyla.ru/](http://tarantool.bolanebyla.ru/)

### Доступные методы API

1. `GET` `/api/memes/` - получение списка всех мемов в БД
2. `GET` `/api/memes/<int:id>/` - получение мема по id
3. `POST (FormData)` `/api/memes/` - создание нового мема

    _Поля запроса_:
    ```
    top_text: str (может быть пустым)
    bottom_text: str (может быть пустым)
    img: File (может быть пустым)
    ```
    _Пример запроса_

## Запуск проекта

1. Создать `.env` файл с переменными окружения (пример `.env.example`)

```
HOST_URL=http://localhost:8080 # хост на котором будет развернут проект
```

2. Запустить проект

```
docker-compose up -d --build
```

Проект запускается на порту "8080"

При необходимости порт можно изменить в `docker-compose.yaml`