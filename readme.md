<div align="center">

# 🔗 YaCut

**URL shortener on Flask with asynchronous file uploads to Yandex Disk**

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-3.0-000000?logo=flask&logoColor=white) ![aiohttp](https://img.shields.io/badge/aiohttp-async-2C5BB4?logo=aiohttp&logoColor=white) ![pytest](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white) ![License](https://img.shields.io/badge/license-MIT-lightgrey)

[**English**](README.md) · [Русский](README.ru.md)

</div>

---

## 📖 About

YaCut turns a long URL into a short identifier — either custom or generated. On top of that it can upload several files to Yandex Disk asynchronously and hand out a short download link for each of them. The service ships with a web interface and a small REST API.

---

## ✨ Features

- **Short links** — custom or generated identifier (up to 16 chars)
- **Redirects** — short link forwards to the original URL
- **Async uploads** — multiple files to Yandex Disk via `aiohttp`
- **REST API** — create links and resolve the original URL
- **Custom error pages** for 404 and 500
- **OpenAPI spec** in `openapi.yml`

---

## 🛠 Tech Stack

| Layer | Technologies |
|---|---|
| **Language** | Python 3.11 |
| **Framework** | Flask 3, Flask-WTF, WTForms |
| **Database** | SQLite, SQLAlchemy, Alembic (Flask-Migrate) |
| **Async** | aiohttp (Yandex Disk API) |
| **Frontend** | Jinja2, Bootstrap |
| **Testing** | pytest, Postman |
| **Quality** | flake8, GitHub Actions |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- A Yandex Disk OAuth token (for file uploads)

### Installation

```bash
git clone <адрес вашего репозитория>
cd yacut

python3.11 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Environment

Create a `.env` file in the project root:

```env
FLASK_APP=yacut
FLASK_DEBUG=1
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=your-secret-key
DISK_TOKEN=your-yandex-disk-oauth-token
```

### Run

```bash
flask db upgrade
flask run
```

The app is available at `http://127.0.0.1:5000/`.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/id/` | Create a short link |
| `GET` | `/api/id/{short_id}/` | Get the original URL |
| `GET` | `/{short_id}` | Redirect to the original URL |
| `GET` `POST` | `/files` | Upload files to Yandex Disk |

---

## 🧪 Tests

```bash
pytest
flake8
```

---

## 📁 Project Structure

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

Every push and pull request runs a GitHub Actions workflow that installs dependencies and lints the code with `flake8` using the repository config.

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 👤 Author

**Анна Павлова**
