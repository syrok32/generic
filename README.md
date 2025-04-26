
# Restapimodel

## Описание проекта

**Restapimodel** — это REST API проект, реализованный на [Django](https://www.djangoproject.com/) с использованием [Django REST Framework](https://www.django-rest-framework.org/). Поддерживает асинхронные задачи (Celery), пользователей, валидацию, пагинацию и интеграцию с платежными сервисами. Проект легко развернуть как локально, так и на сервере благодаря Docker и Docker Compose.

---

## 🌐 Демо-версия

Задеплоенное приложение доступно по адресу:  
**http://45.139.78.64/**  
(Замените на реальный адрес после деплоя!)

---

## Структура проекта

<details>
<summary>Структура папок</summary>

- `info/` — бизнес-логика (модели, сериализаторы, задачи)
- `users/` — всё для пользователей (модели, сериализаторы, права)
- `Restapimodel/` — настройки Django, celery, маршрутизация
- `fixtures/` — тестовые данные
- `static/`, `staticfiles/`, `templates/` — статика и шаблоны
- `nginx/` — конфигурация nginx
- `Dockerfile`, `docker-compose.yml` — для контейнеризации
</details>

---

## 🚀 Запуск проекта локально

...  
<!-- Оставить локальные шаги без изменений, фокус изменить только на CI/CD раздел -->

---

## 🌍 Развертывание на удалённом сервере (production)

...  
<!-- Оставить production-инструкции, только подверстать объяснение про образы -->

---

## 🤖 CI/CD: Автоматизация деплоя через Github Actions + Docker Hub

### Схема работы деплоя

1. При пуше в main (или другую ветку) GitHub Actions:
    - Собирает Docker-образ приложения.
    - Логинится в Docker Hub.
    - Пушит новый образ на Docker Hub в ваш репозиторий.
2. На сервере (production) обновление происходит командой:
    ```bash
    docker-compose pull
    docker-compose up -d
    ```
    Это подтянет новый образ из Docker Hub и перезапустит ваши контейнеры.

### Пример workflow файла (.github/workflows/deploy.yml)

```yaml
name: Build and Push to Docker Hub

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout source
        uses: actions/checkout@v3

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          file: ./Dockerfile
          push: true
          tags: yourdockerhubusername/restapimodel:latest
```

- Замените `yourdockerhubusername/restapimodel:latest` на ваш namespace и имя репозитория в Docker Hub.
- Аккаунт и пароль Docker Hub должны быть добавлены в GitHub Settings → Secrets как `DOCKER_USERNAME` и `DOCKER_PASSWORD`.

### Деплой на сервере через Docker Hub

1. На сервере должен быть настроен docker-compose и идентичный `docker-compose.yml` (образ должен ссылаться на тот же `yourdockerhubusername/restapimodel:latest`). Пример:

```yaml
services:
  web:
    image: yourdockerhubusername/restapimodel:latest
    ...
```
2. Чтобы обновить проект до самой свежей версии образа:
```bash
docker-compose pull
docker-compose up -d
```
Для полного обновления рекомендуется вызывать также:
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
```

---

## 📝 Полезные ссылки

- [Docker Hub](https://hub.docker.com/)
- [GitHub Actions Docker docs](https://docs.github.com/en/actions/publishing-packages/publishing-docker-images)
- [Docs: docker/build-push-action](https://github.com/docker/build-push-action)
- [Документация Django](https://docs.djangoproject.com/ru/4.0/)
- [Документация DRF](https://www.django-rest-framework.org/)

---

## 📧 Контакты/Автор(ы)
Добавьте сюда информацию о себе, email или ссылку на портфолио.

