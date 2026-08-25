<div align="center">

# 🔗 YaCut

**Сервис коротких ссылок на Flask с асинхронной загрузкой файлов на Яндекс Диск**

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-3.0-000000?logo=flask&logoColor=white) ![aiohttp](https://img.shields.io/badge/aiohttp-async-2C5BB4?logo=aiohttp&logoColor=white) ![pytest](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white) ![License](https://img.shields.io/badge/license-MIT-lightgrey)

[English](README.md) · [**Русский**](README.ru.md)

</div>

---

## 📖 О проекте

YaCut превращает длинную ссылку в короткий идентификатор — заданный пользователем или сгенерированный автоматически. Дополнительно сервис умеет асинхронно загружать несколько файлов на Яндекс Диск и выдавать на каждый файл короткую ссылку для скачивания. Есть веб-интерфейс и небольшое REST API.

---

## ✨ Возможности

- **Короткие ссылки** — свой или сгенерированный идентификатор (до 16 символов)
- **Редиректы** — переход с короткой ссылки на исходный адрес
- **Асинхронная загрузка** — несколько файлов на Яндекс Диск через `aiohttp`
- **REST API** — создание ссылок и получение оригинального адреса
- **Собственные страницы ошибок** 404 и 500
- **Спецификация OpenAPI** в `openapi.yml`

---

## 🛠 Стек технологий

| Слой | Технологии |
|---|---|
| **Язык** | Python 3.11 |
| **Фреймворк** | Flask 3, Flask-WTF, WTForms |
| **База данных** | SQLite, SQLAlchemy, Alembic (Flask-Migrate) |
| **Асинхронность** | aiohttp (Yandex Disk API) |
| **Фронтенд** | Jinja2, Bootstrap |
| **Тестирование** | pytest, Postman |
| **Качество кода** | flake8, GitHub Actions |

---

## 🚀 Запуск

### Требования

- Python 3.11+
- OAuth-токен Яндекс Диска (для загрузки файлов)

### Установка

```bash
git clone <адрес вашего репозитория>
cd yacut

python3.11 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Переменные окружения

Создайте файл `.env` в корне проекта:

```env
FLASK_APP=yacut
FLASK_DEBUG=1
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=your-secret-key
DISK_TOKEN=your-yandex-disk-oauth-token
```

### Запуск

```bash
flask db upgrade
flask run
```

Приложение доступно по адресу `http://127.0.0.1:5000/`.

---

## 🔌 Эндпоинты API

| Метод | Эндпоинт | Описание |
|---|---|---|
| `POST` | `/api/id/` | Создание короткой ссылки |
| `GET` | `/api/id/{short_id}/` | Получение оригинального адреса |
| `GET` | `/{short_id}` | Редирект на оригинальный адрес |
| `GET` `POST` | `/files` | Загрузка файлов на Яндекс Диск |

---

## 🧪 Тесты

```bash
pytest
flake8
```

---

## 📁 Структура проекта

```
async-yacut/
├── yacut/
│   ├── api_views.py       # REST API
│   ├── views.py           # web interface
│   ├── models.py          # URLMap model
│   ├── forms.py           # WTForms
│   ├── error_handlers.py  # 404 / 500 and API errors
│   ├── templates/
│   └── static/
├── migrations/            # Alembic migrations
├── openapi.yml            # OpenAPI specification
├── tests/                 # pytest test suite
├── settings.py
└── requirements.txt
```

---

## ⚙️ CI

На каждый push и pull request запускается workflow GitHub Actions: устанавливает зависимости и проверяет код `flake8` по конфигу репозитория.

---

## 📄 Лицензия

Проект распространяется под лицензией MIT. Подробности — в файле [LICENSE](LICENSE).

---

## 👤 Автор

**Анна Павлова**
