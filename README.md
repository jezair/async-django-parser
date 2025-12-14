# Async Parser Backend

Backend REST API for aggregating and monitoring data from external sources using an asynchronous parser with timeout control.

## About

This project demonstrates a production-like backend architecture where asynchronous parsers are executed in the background, their execution is controlled by timeouts, and the collected data is exposed via a REST API.

The system is designed to be scalable, fault-tolerant, and suitable for long-running parsing tasks.

## Tech Stack

- Python 3.11
- Django
- Django REST Framework
- PostgreSQL
- Asyncio
- JWT Authentication

## Architecture Overview

The application is split into logical layers:

- **API layer** — REST endpoints for managing data and parser execution
- **Service layer** — business logic and parser orchestration
- **Parsing layer** — asynchronous parsers with timeout and concurrency control
- **Persistence layer** — PostgreSQL database accessed via Django ORM

Parsers are executed asynchronously and wrapped by a manager that controls execution time and concurrency.

## Features

- Asynchronous data parsing with timeout control
- Configurable concurrency for parsers
- REST API for triggering and monitoring parser runs
- Data aggregation and storage
- JWT-based authentication
- Admin panel for monitoring parser runs

## API Overview

- `POST /api/auth/login/` — user authentication
- `POST /api/parsers/run/` — trigger parser execution
- `GET /api/parsers/status/` — parser execution status
- `GET /api/items/` — aggregated data with filtering and pagination

## Running Locally

```bash
git clone https://github.com/your-username/async-parser-backend.git
cd async-parser-backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
