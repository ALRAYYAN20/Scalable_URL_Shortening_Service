# Scalable URL Shortening Service

A production-ready URL shortening service built with **FastAPI**, **PostgreSQL**, and **Redis**. Supports user authentication, custom aliases, click analytics, and link expiration.

🔗 **Live Demo:** https://urlshortenerapi-u6tp.onrender.com/docs  
📦 **GitHub:** https://github.com/ALRAYYAN20/UrlShortenerAPI

---

## Features

- 🔐 **JWT Authentication** — Register and login with secure bcrypt password hashing
- 🔗 **URL Shortening** — Generate cryptographically random short codes
- ✏️ **Custom Aliases** — Create personalized short URLs
- ⚡ **Redis Caching** — Cache redirect lookups to minimize database queries
- 📊 **Click Analytics** — Track how many times each short URL is visited
- ⏳ **Link Expiration** — 24-hour TTL on cached entries
- 🛡️ **Rate Limiting** — IP-based and user-based protection against abuse
- 🐳 **Dockerized** — Fully containerized for consistent deployment

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI |
| Database | PostgreSQL (Neon) |
| Cache | Redis (Upstash) |
| ORM | SQLAlchemy |
| Auth | JWT, bcrypt, OAuth2 |
| Deployment | Docker, Render |
| Validation | Pydantic |

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/register` | ❌ | Create a new user account |
| POST | `/login` | ❌ | Login and receive JWT token |
| POST | `/urls` | ✅ | Shorten a URL |
| GET | `/urls` | ✅ | Get all your shortened URLs |
| GET | `/{short_code}` | ❌ | Redirect to original URL |
| DELETE | `/urls/{id}` | ✅ | Delete a shortened URL |

---

## Project Structure

```
URLShortener/
├── app/
│   ├── __init__.py
│   ├── main.py          # App entry point, router registration
│   ├── models.py        # SQLAlchemy User and URL models
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── database.py      # PostgreSQL connection and session
│   ├── oauth2.py        # JWT token verification
│   ├── cache.py         # Redis client setup
│   └── routers/
│       ├── auth.py      # Register and login endpoints
│       └── urls.py      # URL CRUD and redirect endpoints
├── Dockerfile
├── requirements.txt
└── .env.example
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL
- Redis
- Docker (optional)

### 1. Clone the repository

```bash
git clone https://github.com/ALRAYYAN20/UrlShortenerAPI.git
cd UrlShortenerAPI
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://user:password@localhost/urlshortener
SECRET_KEY=your_secret_key_here
REDIS_URL=redis://localhost:6379
```

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` to explore the API.

---

## Running with Docker

```bash
docker build -t urlshortener .
docker run -p 8000:8000 --env-file .env urlshortener
```

---

## How It Works

### URL Shortening Flow
```
User submits long URL
        ↓
Generate random 6-char short code (secrets.token_urlsafe)
        ↓
Check if short code already exists in DB
        ↓
If unique → save to PostgreSQL with owner_id
        ↓
Return short code to user
```

### Redirect Flow with Redis Caching
```
User visits /{short_code}
        ↓
Check Redis cache first
        ↓
Cache HIT  → redirect instantly (no DB query)
Cache MISS → query PostgreSQL
        ↓
Store result in Redis (1 hour TTL)
        ↓
Increment click count → redirect user
```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | JWT signing secret |
| `REDIS_URL` | Redis connection string |

---

## Author

**Alrayyan Mukadam**  
[GitHub](https://github.com/ALRAYYAN20) · [LinkedIn](https://www.linkedin.com/in/alrayyan-mukadam-9bb96128b)
