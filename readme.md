
# DRFPractice

## Описание
Проект реализован на Django REST Framework. Система сборки и запуска полностью контейнеризирована с помощью Docker Compose. Для CI/CD используется GitHub Actions, а переменные окружения собираются из GitHub Secrets.

## Структура проекта
```
.
├── config/         # Основная конфигурация Django
├── study/          # Приложение курсов
├── users/          # Приложение пользователей
├── static/         # Статические файлы (collectstatic)
├── media/          # Медиа-файлы (user uploads)
├── requirements.txt
├── docker-compose.yaml
├── nginx/
│   └── nginx.conf
├── .env            # Файл переменных окружения (генерируется из GitHub Secrets)
└── ...
```

## Быстрый старт (Docker Compose)
1. Клонируйте репозиторий:
    ```sh
    git clone https://github.com/Lexish-ru/Module_7.git
    cd Module_7
    ```
2. Убедитесь, что у вас есть рабочий `.env`. В CI/CD он собирается из GitHub Secrets (см. раздел ниже).
3. Запустите сборку и запуск:
    ```sh
    docker-compose up --build
    ```
4. Nginx будет слушать порт 80, бекенд (Django + Gunicorn) — на 8000.

## Работа с GitHub Actions (workflows)
- Автоматически запускаются тесты, линтеры и деплой на сервер при каждом push/pull_request в ветки репозитория.
- Все чувствительные переменные окружения передаются в CI/CD как GitHub Secrets.
- На сервере автоматически собирается `.env` из секретов для корректной работы приложения.

## Как формируется .env
- В файле `.env` не хранится никаких секретов — он генерируется в рантайме workflow на сервере с помощью секретов GitHub (`Settings → Secrets and variables → Actions`).

---

### 3. CI/CD и деплой

- При каждом push в репозиторий запускается GitHub Actions:
    - lint (flake8)
    - тесты (manage.py test)
    - сборка и пуш Docker-образа (опционально)
    - деплой на VPS через SSH и docker-compose

#### **Файл workflow:**  
`.github/workflows/ci.yml`

#### **Secrets** (GitHub):
- SSH_KEY — приватный ключ
- SSH_USER, SSH_HOST — логин и адрес сервера
- DEPLOY_DIR — директория на сервере
- SECRET_KEY и др.

---

## Деплой на сервер

1. Добавьте свой SSH-ключ на сервер и в secrets репозитория.
2. Укажите переменные окружения в секрете GitHub.
3. На сервере должен быть установлен Docker и docker-compose.
4. Деплой осуществляется автоматически через Actions.

---

## Документация API

Swagger доступен по адресу:  
`/swagger/` после запуска проекта.

---

## Авторы

- [alexey](https://github.com/Lexish-ru/)

---