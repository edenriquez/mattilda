# Mattilda API 🚀

## Project Structure
```text
.
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── schema.prisma         # Prisma Schema
├── .env
└── src/
    ├── app.py             # Main Entry Point
    ├── db.py              # Prisma Client Instance
    ├── api/
    │   └── routes.py      # API Endpoints (Swagger documented)
    ├── schemas/
    │   └── schemas.py     # Pydantic validation/response schemas
    └── services/
        └── services.py    # Business Logic / Data Access
```

## Setup & Quick Start

### 1. Requirements
- Docker and Docker Compose installed.

### 2. Run with Docker
Everything is packed! Simply run:
```bash
docker-compose up --build
```

The API will be available at [http://localhost:5001](http://localhost:5001).

### 3. API Documentation (Swagger)
Once the server is running, you can view the interactive Swagger documentation at:
👉 **[http://localhost:5001/openapi/swagger](http://localhost:5001/openapi/swagger)**

