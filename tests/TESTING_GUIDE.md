# Testing Guide - Clean Architecture

## What Should Have Tests?

### ✅ MUST have tests

#### 1. **Core/Domain - Entities** ✅
- **Location**: `tests/core/domain/entities/test_*.py`
- **What to test**: Validations, invariants, business methods
- **Example**: `test_user.py`
- **Status**: ✅ Complete

#### 2. **Core/Domain - Value Objects** ✅
- **Location**: `tests/core/domain/value_objects/test_*.py`
- **What to test**: Validations, immutability, comparisons
- **Example**: `test_email_address.py`
- **Status**: ✅ Complete

#### 3. **Core/Domain - Domain Services** ✅
- **Location**: `tests/core/domain/services/test_*.py`
- **What to test**: Pure business logic, business rules
- **Example**: `test_user_domain_service.py`
- **Status**: ✅ Complete

#### 4. **Core/Application - Use Cases** ✅
- **Location**: `tests/core/application/use_cases/test_*.py`
- **What to test**: Orchestration, business flows, error cases
- **Example**: `test_create_user_use_case.py`
- **Status**: ✅ Complete (all use cases have tests)

#### 5. **Infrastructure/Adapters - Repository Adapters** ✅
- **Location**: `tests/infrastructure/adapters/test_*_adapter.py`
- **What to test**: Domain ↔ infrastructure mapping, CRUD operations
- **Example**: `test_user_repository_postgres_adapter.py`
- **Status**: ✅ Complete

#### 6. **Infrastructure/API - Routers** ✅
- **Location**: `tests/infrastructure/api/test_*_router.py`
- **What to test**: HTTP endpoints, schema validation, status codes
- **Example**: `test_user_router.py`
- **Status**: ✅ Complete

### ❌ Does NOT need direct tests

#### 1. **Core/Application - Ports (Interfaces)**
- **Reason**: They are `Protocol` (contracts), have no implementation
- **How they are tested**: Indirectly through:
  - Use Case tests (mock the ports)
  - Adapter tests (implement the ports)
- **Example**: `UserRepositoryPort` - Does NOT need direct test

#### 2. **Core/Application - DTOs**
- **Reason**: They are simple dataclasses, no logic
- **How they are tested**: Indirectly through Use Case tests
- **Example**: `CreateUserDto` - Does NOT need direct test

#### 3. **Infrastructure/API - Schemas (Pydantic)**
- **Reason**: Pydantic validates automatically
- **How they are tested**: Indirectly through Router tests
- **Example**: `CreateUserSchema` - Does NOT need direct test

#### 4. **Infrastructure/Database - Models (SQLAlchemy)**
- **Reason**: They are ORM mappings, no business logic
- **How they are tested**: Indirectly through Adapter tests
- **Example**: `UserModel` - Does NOT need direct test

#### 5. **Infrastructure/Config - Settings**
- **Reason**: Simple configuration, no logic
- **How they are tested**: Indirectly through integration tests
- **Example**: `Settings` - Does NOT need direct test

## Current Coverage Summary

### ✅ Complete (with tests)
- ✅ **Entities**: `User` - Complete tests
- ✅ **Value Objects**: `EmailAddress` - Complete tests
- ✅ **Domain Services**: `UserDomainService` - Complete tests
- ✅ **Use Cases**: All 5 use cases - Complete tests
  - `CreateUserUseCase`
  - `GetUserUseCase`
  - `ListUsersUseCase`
  - `UpdateUserUseCase`
  - `DeleteUserUseCase`
- ✅ **Adapters**: `UserRepositoryPostgresAdapter` - Complete tests
- ✅ **Routers**: `user_router` - Complete tests

### ❌ Does not need direct tests (correct)
- ❌ **Ports**: `UserRepositoryPort` (Protocol, tested indirectly)
- ❌ **DTOs**: `CreateUserDto`, `UpdateUserDto`, etc. (no logic)
- ❌ **Schemas**: `CreateUserSchema`, etc. (Pydantic validates automatically)
- ❌ **Models**: `UserModel` (ORM, tested indirectly)

## Testing Strategy

### Unit Tests (Core)
```
tests/core/
├── domain/
│   ├── entities/
│   │   └── test_user.py                    ✅
│   ├── value_objects/
│   │   └── test_email_address.py              ✅
│   └── services/
│       └── test_user_domain_service.py     ✅
└── application/
    └── use_cases/
        ├── test_create_user_use_case.py    ✅
        ├── test_get_user_use_case.py       ✅
        ├── test_list_users_use_case.py     ✅
        ├── test_update_user_use_case.py    ✅
        └── test_delete_user_use_case.py     ✅
```

**Characteristics**:
- No infrastructure dependencies
- Port mocks (no real implementations)
- Fast and isolated tests

### Integration Tests (Infrastructure)
```
tests/infrastructure/
├── adapters/
│   └── test_user_repository_postgres_adapter.py  ✅
└── api/
    └── test_user_router.py                       ✅
```

**Characteristics**:
- Use real databases (SQLite in memory for tests)
- FastAPI TestClient for E2E tests
- Verify integration between layers

## Conclusion

**Your project has complete coverage of what should have tests.**

**Ports do NOT need direct tests** because:
1. They are interfaces (`Protocol`), have no implementation
2. They are tested indirectly:
   - In Use Cases: ports are mocked
   - In Adapters: ports are implemented

If you wanted to validate that an adapter correctly implements a port, you could use **contract tests**, but it's not necessary for this project.
