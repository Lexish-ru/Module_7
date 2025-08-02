
# DRFPractice

## Описание

Веб-приложение на Django REST Framework с автотестами, Docker и автоматическим CI/CD на GitHub Actions.  
Автодеплой на VPS через SSH (docker-compose).

---

## Структура проекта

- `config/` — конфиги Django, celery и пр.
- `study/`, `users/` — основные приложения проекта
- `.github/workflows/ci.yml` — файл GitHub Actions
- `Dockerfile`, `docker-compose.yml` — сборка и запуск в Docker
- `.env.example` — шаблон переменных окружения

---

## Быстрый старт

### 1. Локальный запуск

```bash
cp .env.example .env
docker-compose up --build
```

- Приложение будет доступно на http://localhost:8000/

---

### 2. Переменные окружения

Все переменные хранятся в `.env` и/или [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets).

**Пример:**
```
POSTGRES_DB=Module_7
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_HOST=db
POSTGRES_PORT=5432

SECRET_KEY=your-secret-key
DEBUG=True
```

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

- [alexey](https://github.com/your-github-nickname)

---