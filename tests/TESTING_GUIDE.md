# Guía de Testing - Clean Architecture

## ¿Qué debe tener pruebas?

### ✅ DEBE tener pruebas

#### 1. **Core/Domain - Entities** ✅
- **Ubicación**: `tests/core/domain/entities/test_*.py`
- **Qué testear**: Validaciones, invariantes, métodos de negocio
- **Ejemplo**: `test_usuario.py`
- **Estado**: ✅ Completo

#### 2. **Core/Domain - Value Objects** ✅
- **Ubicación**: `tests/core/domain/value_objects/test_*.py`
- **Qué testear**: Validaciones, inmutabilidad, comparaciones
- **Ejemplo**: `test_email_address.py`
- **Estado**: ✅ Completo

#### 3. **Core/Domain - Domain Services** ✅
- **Ubicación**: `tests/core/domain/services/test_*.py`
- **Qué testear**: Lógica de negocio pura, reglas de negocio
- **Ejemplo**: `test_usuario_domain_service.py`
- **Estado**: ✅ Completo

#### 4. **Core/Application - Use Cases** ✅
- **Ubicación**: `tests/core/application/use_cases/test_*.py`
- **Qué testear**: Orquestación, flujos de negocio, casos de error
- **Ejemplo**: `test_create_usuario_use_case.py`
- **Estado**: ✅ Completo (todos los use cases tienen tests)

#### 5. **Infrastructure/Adapters - Repository Adapters** ✅
- **Ubicación**: `tests/infrastructure/adapters/test_*_adapter.py`
- **Qué testear**: Mapeo dominio ↔ infraestructura, operaciones CRUD
- **Ejemplo**: `test_usuario_repository_postgres_adapter.py`
- **Estado**: ✅ Completo

#### 6. **Infrastructure/API - Routers** ✅
- **Ubicación**: `tests/infrastructure/api/test_*_router.py`
- **Qué testear**: Endpoints HTTP, validación de schemas, códigos de estado
- **Ejemplo**: `test_usuario_router.py`
- **Estado**: ✅ Completo

### ❌ NO necesita pruebas directas

#### 1. **Core/Application - Ports (Interfaces)**
- **Razón**: Son `Protocol` (contratos), no tienen implementación
- **Cómo se testean**: Indirectamente a través de:
  - Tests de Use Cases (mockean los ports)
  - Tests de Adapters (implementan los ports)
- **Ejemplo**: `UsuarioRepositoryPort` - NO necesita test directo

#### 2. **Core/Application - DTOs**
- **Razón**: Son dataclasses simples, sin lógica
- **Cómo se testean**: Indirectamente a través de tests de Use Cases
- **Ejemplo**: `CreateUsuarioDto` - NO necesita test directo

#### 3. **Infrastructure/API - Schemas (Pydantic)**
- **Razón**: Pydantic valida automáticamente
- **Cómo se testean**: Indirectamente a través de tests de Routers
- **Ejemplo**: `CreateUsuarioSchema` - NO necesita test directo

#### 4. **Infrastructure/Database - Models (SQLAlchemy)**
- **Razón**: Son mapeos ORM, sin lógica de negocio
- **Cómo se testean**: Indirectamente a través de tests de Adapters
- **Ejemplo**: `UsuarioModel` - NO necesita test directo

#### 5. **Infrastructure/Config - Settings**
- **Razón**: Configuración simple, sin lógica
- **Cómo se testean**: Indirectamente a través de tests de integración
- **Ejemplo**: `Settings` - NO necesita test directo

## Resumen de Cobertura Actual

### ✅ Completo (con tests)
- ✅ **Entities**: `Usuario` - Tests completos
- ✅ **Value Objects**: `EmailAddress` - Tests completos
- ✅ **Domain Services**: `UsuarioDomainService` - Tests completos
- ✅ **Use Cases**: Todos los 5 use cases - Tests completos
  - `CreateUsuarioUseCase`
  - `GetUsuarioUseCase`
  - `ListUsuariosUseCase`
  - `UpdateUsuarioUseCase`
  - `DeleteUsuarioUseCase`
- ✅ **Adapters**: `UsuarioRepositoryPostgresAdapter` - Tests completos
- ✅ **Routers**: `usuario_router` - Tests completos

### ❌ No necesita tests directos (correcto)
- ❌ **Ports**: `UsuarioRepositoryPort` (Protocol, se testea indirectamente)
- ❌ **DTOs**: `CreateUsuarioDto`, `UpdateUsuarioDto`, etc. (sin lógica)
- ❌ **Schemas**: `CreateUsuarioSchema`, etc. (Pydantic valida automáticamente)
- ❌ **Models**: `UsuarioModel` (ORM, se testea indirectamente)

## Estrategia de Testing

### Tests Unitarios (Core)
```
tests/core/
├── domain/
│   ├── entities/
│   │   └── test_usuario.py                    ✅
│   ├── value_objects/
│   │   └── test_email_address.py              ✅
│   └── services/
│       └── test_usuario_domain_service.py     ✅
└── application/
    └── use_cases/
        ├── test_create_usuario_use_case.py    ✅
        ├── test_get_usuario_use_case.py       ✅
        ├── test_list_usuarios_use_case.py     ✅
        ├── test_update_usuario_use_case.py    ✅
        └── test_delete_usuario_use_case.py     ✅
```

**Características**:
- Sin dependencias de infraestructura
- Mocks de ports (no implementaciones reales)
- Tests rápidos y aislados

### Tests de Integración (Infrastructure)
```
tests/infrastructure/
├── adapters/
│   └── test_usuario_repository_postgres_adapter.py  ✅
└── api/
    └── test_usuario_router.py                       ✅
```

**Características**:
- Usan bases de datos reales (SQLite en memoria para tests)
- TestClient de FastAPI para tests E2E
- Verifican integración entre capas

## Conclusión

**Tu proyecto tiene cobertura completa de lo que debe tener pruebas.**

Los **Ports NO necesitan pruebas directas** porque:
1. Son interfaces (`Protocol`), no tienen implementación
2. Se testean indirectamente:
   - En Use Cases: se mockean los ports
   - En Adapters: se implementan los ports

Si quisieras validar que un adapter implementa correctamente un port, podrías usar **contract tests**, pero no es necesario para este proyecto.

