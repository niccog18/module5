# Module 5 Project — AI-Ready Task Manager API

## Project Overview

The AI-Ready Task Manager API is a production-style REST API built with FastAPI.

The application provides:

- JWT authentication (register, login, protected routes)
- Secure password hashing with bcrypt
- User-scoped task management
- SQLAlchemy database persistence
- User-task relationship
- Pydantic validation schemas
- Custom error handling
- CORS configuration
- Background task processing
- AI-ready placeholder endpoint for future AI model integration
- Automated pytest test suite
- Auto-generated Swagger documentation


---

# Features

## User Authentication

Users can:

- Register a new account
- Login and receive a JWT access token
- Access protected endpoints using Bearer authentication
- Retrieve their authenticated profile


## Task Management

Authenticated users can:

- Create tasks
- View their own tasks
- Retrieve individual tasks
- Update tasks with partial updates
- Delete tasks
- Request AI-powered task suggestions through a placeholder endpoint


## Security

The API includes:

- JWT tokens with expiration
- bcrypt password hashing
- Protected routes
- User-specific task ownership
- Environment-based configuration


---

# Setup Instructions

## 1. Clone the repository

```bash
git clone <repository-url>

cd taskmanagerAPI
```


## 2. Create a virtual environment

Windows:

```powershell
python -m venv venv

venv\Scripts\activate
```

Mac/Linux:

```bash
python -m venv venv

source venv/bin/activate
```


## 3. Install dependencies

```bash
pip install -r requirements.txt
```


## 4. Configure environment variables

Create a `.env` file from the example:

Windows:

```powershell
copy .env.example .env
```

Mac/Linux:

```bash
cp .env.example .env
```


Update `.env`:

```env
DATABASE_URL=sqlite:///./taskmanager.db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```


For production, replace `SECRET_KEY` with a long randomly generated value.


---

# Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```


The API will run at:

```
http://127.0.0.1:8000
```


Swagger documentation:

```
http://127.0.0.1:8000/docs
```


ReDoc documentation:

```
http://127.0.0.1:8000/redoc
```


---

# Running Tests

Run the pytest suite:

```bash
pytest tests/ -v
```


The test suite includes coverage for:

- Health check endpoint
- User registration
- Authentication requirements
- Creating tasks
- Listing tasks
- Retrieving tasks
- Error handling cases


Tests use an isolated SQLite test database and do not modify the development database.


---

# API Endpoints

## Authentication Routes

### Register User

```
POST /auth/register
```

Creates a new user account and returns an access token.


### Login

```
POST /auth/login
```

Validates credentials and returns a JWT token.


### Current User

```
GET /users/me
```

Returns the authenticated user's profile.

Requires:

```
Authorization: Bearer <token>
```


---

# Task Routes

All task routes require authentication.

## Create Task

```
POST /tasks
```


## List User Tasks

```
GET /tasks
```


## Get Task

```
GET /tasks/{id}
```


## Update Task

```
PATCH /tasks/{id}
```


## Delete Task

```
DELETE /tasks/{id}
```


## AI Suggestion Placeholder

```
POST /tasks/{id}/suggest
```

Returns a placeholder response that will later connect to an AI model.


---

# Project Structure

```
taskmanagerAPI/

├── app/
│
│   ├── main.py
│   │   └── FastAPI application, CORS, router registration
│   │
│   ├── database.py
│   │   └── SQLAlchemy engine, sessions, database dependency
│   │
│   ├── auth.py
│   │   └── JWT utilities and password hashing
│   │
│   ├── enums.py
│   │   └── Task priority enum
│   │
│   ├── models/
│   │   ├── user.py
│   │   └── task.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   └── task.py
│   │
│   └── routers/
│       ├── auth.py
│       └── tasks.py
│
├── tests/
│   ├── conftest.py
│   └── test_tasks.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```


---

# Database Models

## User

Fields:

- id
- username
- email
- hashed_password
- is_active
- created_at


## Task

Fields:

- id
- title
- description
- priority
- completed
- owner_id
- created_at
- updated_at


Relationship:

```
User
 |
 └── Tasks
```


---

# Environment Variables

The application uses:

| Variable | Purpose |
|---|---|
| DATABASE_URL | Database connection string |
| SECRET_KEY | JWT signing key |
| ALGORITHM | JWT algorithm |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token expiration time |


---

# Future AI Integration

The `/tasks/{id}/suggest` endpoint is a placeholder designed for future modules.

Possible future functionality:

- Task prioritization
- Productivity suggestions
- Deadline recommendations
- AI-generated task breakdowns


---

# Technologies Used

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT (`python-jose`)
- Passlib / bcrypt
- Pytest
- Uvicorn


---

# Author

Module 5 — Coding Temple FastAPI Project