# Migration Guide: Database with English Columns

This guide explains how to work with the database that uses English column names from the start.

## 📋 Current Status

The database now has an **initial migration** (`fc568cf57513_initial_migration_english_columns`) that creates tables directly with English names:

- `name` (instead of `nombre`)
- `active` (instead of `activo`)
- `created_at` (instead of `fecha_creacion`)
- `updated_at` (instead of `fecha_actualizacion`)

## 🚀 Quick Start

### 1. **Delete Container Volume (Optional)**

If you want to start completely from scratch and delete all data:

```bash
# Stop and remove containers and volumes
docker-compose down -v

# Or only delete the specific volume
docker volume rm python-example_postgres_data
```

### 2. **Start the Database**

```bash
docker-compose up -d
```

### 3. **Apply Initial Migration**

```bash
source venv/Scripts/activate
alembic upgrade head
```

This will create the `users` table with all columns in English.

### 4. **Verify Migration**

```bash
alembic current
```

You should see: `fc568cf57513 (head)`

## 🔄 Reset Database

If you need to completely reset the database (delete tables and migrations):

### Delete Docker Volume

```bash
# Stop containers and delete volumes (this deletes ALL data)
docker-compose down -v

# Restart
docker-compose up -d

# Apply migrations
source venv/Scripts/activate
alembic upgrade head
```

**Note:** This will delete all data in the database. Use with caution!

## 📝 Migration Structure

The initial migration (`fc568cf57513_initial_migration_english_columns.py`) creates:

```python
op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
)
op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
```

## ✅ Verification

After applying the migration:

1. **Run tests:**
   ```bash
   pytest tests/ -v
   ```

2. **Verify API works:**
   ```bash
   uvicorn main:app --reload
   ```

3. **Test creating a user:**
   ```bash
   curl -X POST "http://localhost:8000/users" \
     -H "Content-Type: application/json" \
     -d '{"name": "John Doe", "email": "john@example.com", "active": true}'
   ```

## 🔍 Verify Database Changes

You can verify that columns are in English:

```sql
-- Connect to PostgreSQL
psql -U user -d db

-- View table structure
\d users

-- You should see:
-- Column     | Type                        | Nullable
-- -----------+-----------------------------+----------
-- id         | integer                     | not null
-- name       | character varying(255)      | not null
-- email      | character varying(255)      | not null
-- active     | boolean                     | not null
-- created_at | timestamp without time zone | not null
-- updated_at | timestamp without time zone | not null
```

## 📝 Changes Made

### Database Model

The `UserModel` uses English names directly:

```python
name = Column(String(255), nullable=False)
active = Column(Boolean, default=True, nullable=False)
created_at = Column(DateTime, default=utc_now, nullable=False)
updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)
```

### Alembic Migration

The initial migration `fc568cf57513_initial_migration_english_columns.py` was created that:
- Creates the `users` table with columns in English
- Includes indexes for `id` and `email`
- Includes `downgrade()` function to drop the table if needed

## 🆘 Troubleshooting

### Error: "Can't locate revision identified by '...'"

If you see this error, it means Alembic has a migration registered that no longer exists. Fix with:

```bash
# Reset database completely
docker-compose down -v
docker-compose up -d

# Create new migration
alembic revision --autogenerate -m "initial_migration_english_columns"
alembic upgrade head
```

### Error: "relation 'users' does not exist"

If the table doesn't exist, apply the migration:

```bash
alembic upgrade head
```

### Database connection error

Verify your `.env` file and make sure credentials are correct:

```env
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### Error: "Table already exists"

If the table already exists but with Spanish names, you need:

1. **Delete container volume:**
   ```bash
   docker-compose down -v
   docker-compose up -d
   ```

2. **Or reset with Docker:**
   ```bash
   docker-compose down -v
   docker-compose up -d
   alembic upgrade head
   ```

## 📚 Useful Commands

```bash
# View current migration status
alembic current

# View migration history
alembic history

# Apply migration
alembic upgrade head

# Revert last migration
alembic downgrade -1

# Create new migration (autogenerate)
alembic revision --autogenerate -m "description"

# Create new migration (manual)
alembic revision -m "description"
```

## 🎯 Summary

- ✅ Initial migration created with English names
- ✅ Model updated to use English names directly
- ✅ All tests pass with new structure
