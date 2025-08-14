# Simple Blog Flask

A **simple blog application built with Flask**.\
It features user authentication, CRUD operations for posts, templating and is ready for deployment using **Docker + Nginx** with HTTPS.

---

## Features

- User authentication (login/register/logout)
- CRUD operations for blog posts
- Template rendering using **Jinja2** (no Bootstrap)
- Ready for **Docker + Nginx deployment**
- Separate **dev** and **prod** configuration
- Database migrations via **Flask-Migrate**
- HTTPS support with self-signed or custom certificates

---

## Environment Setup

### `.env.example`

This file lists the required environment variables. Copy to `.env` and edit as needed:

```
API_KEY_BLAST=
VAPID_PUBLIC_KEY=
VAPID_PRIVATE_KEY=
MYSQL_ROOT_PASSWORD=
MYSQL_DATABASE=
MYSQL_USER=
MYSQL_PASSWORD=
SQLALCHEMY_DATABASE_URI_PROD=
SQLALCHEMY_DATABASE_URI_DEV=
```

**Usage:**

```bash
cp .env.example .env
```

Edit `.env` with your secret key and database URL. Do \*\*not commit \*\*\`\` to Git.

---

## Folder Structure & File Overview

```
simple-blog-flask/
├── app/
│   ├── __init__.py        # Initialize Flask app, register blueprints, DB, login manager
│   ├── models.py          # SQLAlchemy models: User, Post
│   ├── routes.py          # Flask routes and logic
│   └── templates/         # HTML templates
├── config/
│   ├── default.py         # Default configuration
│   ├── development.py             # Development configuration
│   └── production.py            # Production configuration
├── nginx/
│   └── default.conf       # Nginx reverse proxy configuration
├── .dockerignore
├── .gitignore
├── Dockerfile              # Dockerfile for Flask app
├── docker-compose.yml
├── generate_vapid.py       # Optional: generate VAPID keys
├── requirements.txt
├── wsgi.py
└── .env.example
```

---

## Running the Project

### 1️⃣ Clone the repository

```bash
git clone https://github.com/MuhammadMuhidin/simple-blog-flask.git
cd simple-blog-flask
```

### 2️⃣ Pull latest changes

```bash
git pull origin main
```

### 3️⃣ Start Docker containers

```bash
docker-compose up --build
```

This starts:

- **Flask app container**
- **Nginx container** (reverse proxy)

---

### 4️⃣ Development Environment Setup

1. Enter the **Flask container**:

```bash
docker exec -it <flask_container_name> bash
```

2. Initialize the database:

```bash
flask db init
flask db migrate
flask db upgrade
```

3. Access the app at `http://localhost` (HTTP) or `https://localhost` if using certificates.

---

### 5️⃣ Production Environment Setup

1. Enter the **Flask container**:

```bash
docker exec -it <flask_container_name> bash
```

2. Upgrade the database:

```bash
flask db upgrade
```

3. Access the app via **Nginx** at `https://your-domain`.

---

### 6️⃣ HTTPS Setup

To make the HTTPS certificate trusted:

1. Place your `.crt` and `.key` files (self-signed or CA-signed).
2. Update Nginx config (`nginx/default.conf`) to point to these certificate files.
3. Reload Nginx inside the container:

```bash
docker exec -it <nginx_container_name> nginx -s reload
```

4. Optionally, add your certificate to **trusted root CA** in your OS/browser for self-signed certs.

---

## Database Migrations

- **Development (**\`\`**)**: full migration workflow (`init`, `migrate`, `upgrade`)
- **Production (**\`\`**)**: only `upgrade` to apply pending migrations

> This ensures your database is in sync with your models.

---

## Contributing

1. Fork the repository
2. Create a new branch for your feature/fix
3. Commit changes
4. Submit a pull request

Use `.env.example` to guide environment variable setup.

---

## Acknowledgments

- Flask framework
- SQLAlchemy ORM
- Docker + Nginx deployment setup
- Flask-Migrate for database migrations """
