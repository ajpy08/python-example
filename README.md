# Usuarios API - CRUD con Clean Architecture

API REST para gestión de usuarios implementada con **FastAPI**, **PostgreSQL** y siguiendo los principios de **Clean Architecture** y **Arquitectura Hexagonal**.

## 📋 Características

- ✅ CRUD completo de usuarios (Create, Read, Update, Delete, List)
- ✅ Arquitectura Clean Architecture + Hexagonal (Ports & Adapters)
- ✅ Separación estricta de capas (Core e Infrastructure)
- ✅ Documentación automática con Swagger/OpenAPI
- ✅ Tests unitarios y de integración
- ✅ PostgreSQL con Docker Compose
- ✅ Type hints exhaustivos
- ✅ Validación de datos con Pydantic

## 🏗️ Arquitectura

El proyecto sigue una arquitectura en capas estricta:

```
project/
├── core/                    # Capa de dominio y aplicación (sin dependencias de infra)
│   ├── domain/              # Entidades, Value Objects, Domain Services
│   └── application/         # Use Cases, Ports (interfaces), DTOs
├── infrastructure/          # Capa de infraestructura (depende de core)
│   ├── adapters/           # Implementaciones de puertos (repositorios, servicios externos)
│   ├── api/                 # FastAPI routers, schemas, controllers
│   ├── database/            # SQLAlchemy models, session management
│   └── config/              # Configuración (settings)
└── tests/                   # Tests unitarios e integración
```

### Principios

- **Core nunca depende de Infrastructure**: El dominio y los casos de uso son independientes de la infraestructura
- **Ports & Adapters**: Las interfaces (ports) están en `core/application/ports`, las implementaciones (adapters) en `infrastructure/adapters`
- **Dependency Inversion**: Los use cases dependen de abstracciones (ports), no de implementaciones concretas

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.9+
- Docker y Docker Compose
- pip

### Pasos

1. **Clonar el repositorio** (si aplica)

2. **Crear entorno virtual**

```bash
python -m venv venv

# Activar entorno virtual:
# - En Linux/Mac o Git Bash (Windows): 
source venv/bin/activate
# - En Git Bash (Windows) también puedes usar:
source venv/Scripts/activate
# - En CMD (Windows):
venv\Scripts\activate.bat
# - En PowerShell (Windows):
venv\Scripts\Activate.ps1
```

3. **Instalar dependencias**

Primero actualiza pip (recomendado):

```bash
python -m pip install --upgrade pip
```

Luego instala las dependencias:

```bash
pip install -r requirements.txt
```

**Nota:** Este proyecto usa `psycopg` (psycopg3) que tiene mejor soporte multiplataforma, incluyendo Windows.

4. **Configurar variables de entorno**

Copia el archivo de ejemplo y ajusta según necesites:

```bash
cp env.example .env
```

O crea manualmente un archivo `.env` en la raíz del proyecto:

```env
# Database Configuration
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=usuarios_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Application Configuration
APP_NAME=Usuarios API
APP_VERSION=1.0.0
DEBUG=True
```

5. **Iniciar PostgreSQL con Docker Compose**

```bash
docker-compose up -d
```

6. **Inicializar la base de datos**

Es necesario crear las tablas antes de usar la API. Ejecuta:

```bash
python -c "from infrastructure.database.init_db import init_db; init_db()"
```

O usando el script de Python directamente:

```bash
python infrastructure/database/init_db.py
```

**Nota:** Este paso solo es necesario la primera vez o después de eliminar el volumen de Docker. Si ya tienes las tablas creadas, puedes omitir este paso.

7. **Ejecutar la aplicación**

```bash
uvicorn main:app --reload
```

La API estará disponible en `http://localhost:8000`

## 📚 Documentación API

Una vez que la aplicación esté corriendo, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔌 Endpoints

### Usuarios

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/usuarios` | Crear un nuevo usuario |
| GET | `/usuarios` | Listar todos los usuarios (con paginación) |
| GET | `/usuarios/{id}` | Obtener un usuario por ID |
| PUT | `/usuarios/{id}` | Actualizar un usuario |
| DELETE | `/usuarios/{id}` | Eliminar un usuario |

### Ejemplos de uso

#### Crear usuario

```bash
curl -X POST "http://localhost:8000/usuarios" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "activo": true
  }'
```

#### Listar usuarios

```bash
curl "http://localhost:8000/usuarios?skip=0&limit=10"
```

#### Obtener usuario por ID

```bash
curl "http://localhost:8000/usuarios/1"
```

#### Actualizar usuario

```bash
curl -X PUT "http://localhost:8000/usuarios/1" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez Actualizado",
    "activo": false
  }'
```

#### Eliminar usuario

```bash
curl -X DELETE "http://localhost:8000/usuarios/1"
```

## 🧪 Testing

### Ejecutar todos los tests

```bash
pytest
```

### Ejecutar con cobertura

```bash
pytest --cov=core --cov=infrastructure --cov-report=html
```

### Ejecutar tests específicos

```bash
# Tests del dominio
pytest tests/core/domain/

# Tests de casos de uso
pytest tests/core/application/

# Tests de infraestructura
pytest tests/infrastructure/
```

## 📁 Estructura del Código

### Domain Layer (`core/domain`)

- **Entities**: `Usuario` - Entidad de dominio pura
- **Value Objects**: `EmailAddress` - Value object inmutable con validación

### Application Layer (`core/application`)

- **Ports**: `UsuarioRepositoryPort` - Interfaz del repositorio
- **Use Cases**:
  - `CreateUsuarioUseCase`
  - `GetUsuarioUseCase`
  - `ListUsuariosUseCase`
  - `UpdateUsuarioUseCase`
  - `DeleteUsuarioUseCase`
- **DTOs**: DTOs para transferencia de datos entre capas

### Infrastructure Layer (`infrastructure`)

- **Adapters**: `UsuarioRepositoryPostgresAdapter` - Implementación PostgreSQL del repositorio
- **API**: Routers FastAPI, schemas Pydantic
- **Database**: SQLAlchemy models, session management
- **Config**: Settings con Pydantic Settings

## 🔧 Configuración de Desarrollo

### Code Quality

El proyecto incluye configuración para:

- **flake8**: Linting
- **mypy**: Type checking
- **black**: Code formatting (opcional, no configurado en CI)
- **pytest**: Testing con cobertura

### Ejecutar linters

```bash
# Flake8
flake8 core infrastructure tests

# MyPy
mypy core infrastructure
```

### Corrección automática de errores

Para corregir automáticamente la mayoría de errores de flake8 (líneas largas, espacios en blanco, etc.), puedes usar:

#### Opción 1: autopep8 (recomendado)

```bash
# Instalar autopep8 si no está instalado
pip install autopep8

# Corregir automáticamente todos los errores corregibles
autopep8 --in-place --aggressive --aggressive -r core infrastructure tests

# Ver qué cambios haría sin aplicarlos
autopep8 --diff -r core infrastructure tests
```

#### Opción 2: black (formateador automático)

```bash
# Instalar black si no está instalado
pip install black

# Formatear todo el código (puede cambiar el estilo)
black core infrastructure tests

# Ver qué cambios haría sin aplicarlos
black --diff core infrastructure tests
```

#### Opción 3: Corrección manual de errores comunes

```bash
# Eliminar líneas en blanco al final de archivos (W391)
# En Linux/Mac:
find . -name "*.py" -exec sed -i '' -e :a -e '/^\n*$/{$d;N;ba' -e '}' {} \;

# En Windows (Git Bash):
find . -name "*.py" -exec sed -i -e :a -e '/^\n*$/{$d;N;ba' -e '}' {} \;
```

**Nota:** `autopep8` es más conservador y solo corrige errores de flake8, mientras que `black` reformatea todo el código según su propio estilo. Se recomienda usar `autopep8` para mantener el estilo actual del proyecto.

## 🐳 Docker

### Iniciar PostgreSQL

```bash
docker-compose up -d
```

### Detener PostgreSQL

```bash
docker-compose down
```

### Ver logs

```bash
docker-compose logs -f postgres
```

### Eliminar volúmenes (⚠️ elimina datos)

```bash
docker-compose down -v
```

## 📝 Convenciones de Naming

Siguiendo las reglas del proyecto:

- **Entities**: PascalCase singular (`Usuario`)
- **Value Objects**: PascalCase (`EmailAddress`)
- **Ports**: Sufijo `Port` (`UsuarioRepositoryPort`)
- **Adapters**: Sufijo `Adapter` con tecnología (`UsuarioRepositoryPostgresAdapter`)
- **Use Cases**: Sufijo `UseCase` (`CreateUsuarioUseCase`)
- **DTOs**: Sufijo `Dto` (`CreateUsuarioDto`)
- **Schemas**: Sufijo `Schema` (`CreateUsuarioSchema`)

## 🔒 Validaciones

- **Email**: Formato válido y único en la base de datos
- **Nombre**: No vacío, máximo 255 caracteres
- **ID**: Validación de existencia en operaciones de actualización/eliminación

## 🚨 Manejo de Errores

- **400 Bad Request**: Validación fallida o reglas de negocio violadas
- **404 Not Found**: Recurso no encontrado
- **500 Internal Server Error**: Errores del servidor

## 📦 Dependencias Principales

- **FastAPI**: Framework web
- **SQLAlchemy**: ORM
- **Pydantic**: Validación y configuración
- **psycopg** (psycopg3): Driver PostgreSQL moderno con mejor soporte multiplataforma
- **pytest**: Testing framework

## 🤝 Contribuir

1. Seguir las convenciones de naming establecidas
2. Mantener la separación de capas (core no depende de infrastructure)
3. Escribir tests para nuevas funcionalidades
4. Asegurar que todos los tests pasen antes de hacer commit

## 📄 Licencia

Este proyecto es un PoC/ejemplo educativo.

## 🆘 Troubleshooting

### Error de conexión a la base de datos

- Verificar que PostgreSQL esté corriendo: `docker-compose ps`
- Verificar variables de entorno en `.env`
- Verificar que el puerto 5432 no esté ocupado

### Error al crear tablas

- Verificar permisos de la base de datos
- Verificar que la base de datos exista
- Revisar logs: `docker-compose logs postgres`

### Tests fallan

- Verificar que las dependencias estén instaladas: `pip install -r requirements.txt`
- Ejecutar tests con `-v` para más detalles: `pytest -v`

