
# Restapimodel

## Описание проекта

**Restapimodel** — это REST API проект, реализованный на [Django](https://www.djangoproject.com/) с использованием [Django REST Framework](https://www.django-rest-framework.org/). Проект построен по модульному принципу и предназначен для быстрого старта разработки серверных приложений с поддержкой асинхронных задач (Celery), пользователей, валидации данных, пагинации и интеграцией с платежными сервисами.

## Основные возможности

- Работа с пользователями (регистрация, аутентификация)
- API для работы с сущностями (пример: info)
- Асинхронные задачи и фоновые процессы ([Celery](https://docs.celeryq.dev/en/stable/))
- Докеризированное развертывание и минимальная настройка окружения
- Интеграция с платежной системой (есть файл stripe_service.py)
- Возможность загрузки и хранения изображений
- Nginx в качестве reverse proxy

## Структура проекта

<details>
<summary>Структура папок</summary>

- `info/` — приложение для основной бизнес-логики (модели, сериализаторы, задачи)
- `users/` — всё для пользователей (модели, сериализаторы, управление правами)
- `Restapimodel/` — настройки Django, celery, маршрутизация
- `fixtures/` — фикстуры с данными для быстрой загрузки
- `static/`, `staticfiles/`, `templates/` — медиа и шаблоны
- `nginx/` — конфигурация nginx для production-окружения
- `data/cache/` — директория для кэша
- `Dockerfile`, `docker-compose.yml` — для контейнеризации
</details>

## Предварительные требования

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Быстрый старт

1. **Клонируйте репозиторий**
   ```bash
   git clone <url до вашего репозитория>
   cd Restapimodel
   ```
2. **Скопируйте и настройте переменные окружения:**
   ```bash
   cp .env.example .env
   ```
   Отредактируйте файл `.env` при необходимости (укажите пароли, ключи сервисов и т.д.)

3. **Соберите и запустите контейнеры:**
   ```bash
   docker-compose up --build -d
   ```

4. **Остановите контейнеры:**
   ```bash
   docker-compose down
   ```

5. **Загрузка тестовых данных (опционально):**
   ```bash
   docker-compose exec web python manage.py loaddata fixtures/data.json
   ```

## Дополнительная информация

- Основные настройки приложения находятся в папке `Restapimodel/`
- Celery и Redis используются для асинхронных/фоновых задач (см. файл `celery.py`)
- Nginx (директория `nginx/`) используется для проксирования запросов к Django и статики
- В директориях `info/` и `users/` хранятся отдельные бизнес-модули
- Для работы требуется PostgreSQL (для настройки см. docker-compose.yml и ваш `.env`)

## Запуск тестов

```bash
docker-compose exec web python manage.py test
```

## Полезные ссылки

- [Документация Django](https://docs.djangoproject.com/ru/4.0/)
- [Документация DRF](https://www.django-rest-framework.org/)
- [Официальный гайд по Docker Compose](https://docs.docker.com/compose/)

---

### Автор(ы):  
Добавьте информацию о себе или команде, ссылку на портфолио или контакты.

