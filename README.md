# Mattilda Project 🚀

A full-stack application for managing schools, students, and financial statements.

## Project Structure
```text
.
├── docker-compose.yml
├── requirements.txt
├── schema.prisma         # Backend Prisma Schema
├── frontend/             # React + Vite + TypeScript Frontend
│   ├── src/
│   ├── Dockerfile
│   └── nginx.conf
└── src/                  # Python + Flask Backend
    ├── app.py             # Main Entry Point
    ├── db.py              # Prisma Client Instance
    ├── api/               # API Route Handlers
    ├── repositories/      # Data Access Layer
    ├── use_cases/         # Business Logic Layer
    └── schemas/           # Pydantic Schemas
```

## Setup & Quick Start

### 1. Requirements
- Docker and Docker Compose installed.

### 2. Run with Docker (Recommended)
The entire stack (API, Frontend, Database) can be launched with one command:
```bash
docker-compose up --build
```

- **Frontend:** [http://localhost:5173](http://localhost:5173)
- **API Backend:** [http://localhost:5001](http://localhost:5001)
- **API Documentation (Swagger):** [http://localhost:5001/docs](http://localhost:5001/docs)

### 3. Seed Database
To populate the database with example schools and financial data:
```bash
docker-compose exec api python3 seed.py
```
*Note: Make sure your API container is running.*

---

## Frontend Documentation

The frontend is a modern dashboard built with **React**, **Vite**, and **TypeScript**.

### Features
- **School Navigation:** Browse and select schools from the sidebar.
- **Financial Analytics:** Real-time calculation of total billed, paid, and unpaid amounts.
- **Invoice Ledger:** Visual representation of student invoices with status badges.

### Local Development (Frontend only)
If you want to run the frontend locally without Docker:
```bash
cd frontend
npm install
npm run dev
```
*Note: Ensure the backend is running on port 5001.*

---

## Backend Documentation

The backend is built with **Flask**, **Flask-OpenAPI3**, and **Prisma ORM**.

### Architecture
- **API Layer:** Handles HTTP requests and Swagger documentation generation.
- **Use Cases:** Encapsulates business logic, making the code testable and reusable.
- **Repositories:** Handles data persistence using Prisma.
- **Validation:** Powered by Pydantic for robust request/response validation.
