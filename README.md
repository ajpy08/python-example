# Users API - CRUD with Clean Architecture

REST API for user management implemented with **FastAPI**, **PostgreSQL** following **Clean Architecture** and **Hexagonal Architecture** principles.

## 📋 Features

- ✅ Complete CRUD for users (Create, Read, Update, Delete, List)
- ✅ Clean Architecture + Hexagonal (Ports & Adapters)
- ✅ Strict layer separation (Core and Infrastructure)
- ✅ Automatic documentation with Swagger/OpenAPI
- ✅ Unit and integration tests
- ✅ PostgreSQL with Docker Compose
- ✅ Comprehensive type hints
- ✅ Data validation with Pydantic

## 🏗️ Architecture

The project follows a strict layered architecture:

```
project/
├── core/                    # Domain and application layer (no infra dependencies)
│   ├── domain/              # Entities, Value Objects, Domain Services
│   └── application/         # Use Cases, Ports (interfaces), DTOs
├── infrastructure/          # Infrastructure layer (depends on core)
│   ├── adapters/           # Port implementations (repositories, external services)
│   ├── api/                 # FastAPI routers, schemas, controllers
│   ├── database/            # SQLAlchemy models, session management
│   └── config/              # Configuration (settings)
└── tests/                   # Unit and integration tests
```

### Principles

- **Core never depends on Infrastructure**: Domain and use cases are independent of infrastructure
- **Ports & Adapters**: Interfaces (ports) are in `core/application/ports`, implementations (adapters) in `infrastructure/adapters`
- **Dependency Inversion**: Use cases depend on abstractions (ports), not concrete implementations

## 🚀 Installation and Setup

### Prerequisites

- Python 3.9+
- Docker and Docker Compose
- pip

### Steps

1. **Clone the repository** (if applicable)

2. **Create virtual environment**

```bash
python -m venv venv

# Activate virtual environment:
# - On Linux/Mac or Git Bash (Windows): 
source venv/bin/activate
# - On Git Bash (Windows) you can also use:
source venv/Scripts/activate
# - On CMD (Windows):
venv\Scripts\activate.bat
# - On PowerShell (Windows):
venv\Scripts\Activate.ps1
```

3. **Install dependencies**

First update pip (recommended):

```bash
python -m pip install --upgrade pip
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

**Note:** This project uses `psycopg` (psycopg3) which has better cross-platform support, including Windows.

4. **Configure environment variables**

Copy the example file and adjust as needed:

```bash
cp env.example .env
```

Or manually create a `.env` file in the project root:

```env
# Database Configuration
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=users_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Application Configuration
APP_NAME=Users API
APP_VERSION=1.0.0
DEBUG=True
```

5. **Start PostgreSQL with Docker Compose**

```bash
docker-compose up -d
```

6. **Initialize the database**

You need to create the tables before using the API. Run:

```bash
alembic upgrade head
```

**Note:** This step is only necessary the first time or after deleting the Docker volume. If you already have the tables created, you can skip this step.

7. **Run the application**

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔌 Endpoints

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users` | Create a new user |
| GET | `/users` | List all users (with pagination) |
| GET | `/users/{id}` | Get a user by ID |
| PUT | `/users/{id}` | Update a user |
| DELETE | `/users/{id}` | Delete a user |

### Usage Examples

#### Create user

```bash
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "active": true
  }'
```

#### List users

```bash
curl "http://localhost:8000/users?skip=0&limit=10"
```

#### Get user by ID

```bash
curl "http://localhost:8000/users/1"
```

#### Update user

```bash
curl -X PUT "http://localhost:8000/users/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe Updated",
    "active": false
  }'
```

#### Delete user

```bash
curl -X DELETE "http://localhost:8000/users/1"
```

## 🧪 Testing

### Run all tests

```bash
pytest
```

### Run with coverage

```bash
pytest --cov=core --cov=infrastructure --cov-report=html
```

### Run specific tests

```bash
# Domain tests
pytest tests/core/domain/

# Use case tests
pytest tests/core/application/

# Infrastructure tests
pytest tests/infrastructure/
```

## 📁 Code Structure

### Domain Layer (`core/domain`)

- **Entities**: `User` - Pure domain entity
- **Value Objects**: `EmailAddress` - Immutable value object with validation

### Application Layer (`core/application`)

- **Ports**: `UserRepositoryPort` - Repository interface
- **Use Cases**:
  - `CreateUserUseCase`
  - `GetUserUseCase`
  - `ListUsersUseCase`
  - `UpdateUserUseCase`
  - `DeleteUserUseCase`
- **DTOs**: DTOs for data transfer between layers

### Infrastructure Layer (`infrastructure`)

- **Adapters**: `UserRepositoryPostgresAdapter` - PostgreSQL repository implementation
- **API**: FastAPI routers, Pydantic schemas
- **Database**: SQLAlchemy models, session management
- **Config**: Settings with Pydantic Settings

## 🔧 Development Configuration

### Code Quality

The project includes configuration for:

- **flake8**: Linting
- **mypy**: Type checking
- **black**: Code formatting (optional, not configured in CI)
- **pytest**: Testing with coverage

### Run linters

```bash
# Flake8
flake8 core infrastructure tests

# MyPy
mypy core infrastructure
```

### Automatic error correction

To automatically fix most flake8 errors (long lines, whitespace, etc.), you can use:

#### Option 1: autopep8 (recommended)

```bash
# Install autopep8 if not installed
pip install autopep8

# Automatically fix all fixable errors
autopep8 --in-place --aggressive --aggressive -r core infrastructure tests

# See what changes it would make without applying them
autopep8 --diff -r core infrastructure tests
```

#### Option 2: black (automatic formatter)

```bash
# Install black if not installed
pip install black

# Format all code (may change style)
black core infrastructure tests

# See what changes it would make without applying them
black --diff core infrastructure tests
```

#### Option 3: Manual correction of common errors

```bash
# Remove trailing blank lines (W391)
# On Linux/Mac:
find . -name "*.py" -exec sed -i '' -e :a -e '/^\n*$/{$d;N;ba' -e '}' {} \;

# On Windows (Git Bash):
find . -name "*.py" -exec sed -i -e :a -e '/^\n*$/{$d;N;ba' -e '}' {} \;
```

**Note:** `autopep8` is more conservative and only fixes flake8 errors, while `black` reformats all code according to its own style. It's recommended to use `autopep8` to maintain the current project style.

## 🐳 Docker

### Start PostgreSQL

```bash
docker-compose up -d
```

### Stop PostgreSQL

```bash
docker-compose down
```

### View logs

```bash
docker-compose logs -f postgres
```

### Delete volumes (⚠️ deletes data)

```bash
docker-compose down -v
```

## 📝 Naming Conventions

Following project rules:

- **Entities**: Singular PascalCase (`User`)
- **Value Objects**: PascalCase (`EmailAddress`)
- **Ports**: `Port` suffix (`UserRepositoryPort`)
- **Adapters**: `Adapter` suffix with technology (`UserRepositoryPostgresAdapter`)
- **Use Cases**: `UseCase` suffix (`CreateUserUseCase`)
- **DTOs**: `Dto` suffix (`CreateUserDto`)
- **Schemas**: `Schema` suffix (`CreateUserSchema`)

## 🔒 Validations

- **Email**: Valid format and unique in database
- **Name**: Not empty, maximum 255 characters
- **ID**: Existence validation in update/delete operations

## 🚨 Error Handling

- **400 Bad Request**: Validation failed or business rules violated
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server errors

## 📦 Main Dependencies

- **FastAPI**: Web framework
- **SQLAlchemy**: ORM
- **Pydantic**: Validation and configuration
- **psycopg** (psycopg3): Modern PostgreSQL driver with better cross-platform support
- **pytest**: Testing framework

## 🤝 Contributing

1. Follow established naming conventions
2. Maintain layer separation (core does not depend on infrastructure)
3. Write tests for new features
4. Ensure all tests pass before committing

## 📄 License

This project is an educational PoC/example.

## 🆘 Troubleshooting

### Database connection error

- Verify PostgreSQL is running: `docker-compose ps`
- Verify environment variables in `.env`
- Verify port 5432 is not occupied

### Error creating tables

- Verify database permissions
- Verify database exists
- Check logs: `docker-compose logs postgres`

### Tests fail

- Verify dependencies are installed: `pip install -r requirements.txt`
- Run tests with `-v` for more details: `pytest -v`
