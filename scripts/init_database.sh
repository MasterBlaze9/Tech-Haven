#!/usr/bin/env bash
set -e

echo "=========================================="
echo "Factory Manager - Database Initialization"
echo "=========================================="

# Database connection parameters
PGHOST="${POSTGRES_HOST:-db}"
PGPORT="${POSTGRES_PORT:-5432}"
PGDATABASE="${POSTGRES_DB:-factorydb}"
PGUSER="${POSTGRES_USER:-factoryuser}"
export PGPASSWORD="${POSTGRES_PASSWORD:-factorypass}"

# Wait for PostgreSQL to be ready
echo ""
echo "[1/7] Waiting for PostgreSQL to be ready..."
until psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -c '\q' 2>/dev/null; do
  echo "  PostgreSQL is unavailable - sleeping"
  sleep 2
done
echo "  ✓ PostgreSQL is ready!"

# Create tables from DDL script
echo ""
echo "[2/7] Creating database tables..."
if [ -f "/app/Resources/DDL Database/create_tables_script_final.sql" ]; then
  psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f "/app/Resources/DDL Database/create_tables_script_final.sql" -v ON_ERROR_STOP=0
  echo "  ✓ Tables created!"
else
  echo "  ⚠ DDL script not found at /app/Resources/DDL Database/create_tables_script_final.sql"
fi

# Import database objects (views, functions, procedures)
echo ""
echo "[3/7] Importing database objects (views, functions, procedures)..."
if [ -d "/app/Resources/Objects" ]; then
  for sql_file in /app/Resources/Objects/*/*.sql; do
    if [ -f "$sql_file" ]; then
      # Skip test data files for now
      if [[ ! "$sql_file" =~ insert.*test.*data ]]; then
        echo "  Processing: $(basename $sql_file)"
        psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f "$sql_file" -v ON_ERROR_STOP=0 2>&1 | grep -v "NOTICE:" | grep -v "already exists" || true
      fi
    fi
  done
  echo "  ✓ Database objects imported!"
else
  echo "  ⚠ Objects directory not found at /app/Resources/Objects"
fi

# Apply database privileges
echo ""
echo "[4/7] Applying database privileges..."
if [ -f "/app/Resources/database_privileges.sql" ]; then
  psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f /app/Resources/database_privileges.sql -v ON_ERROR_STOP=0 2>&1 | grep -v "NOTICE:" || true
  echo "  ✓ Privileges applied!"
else
  echo "  ⚠ Privileges script not found"
fi

# Populate tables with initial data
echo ""
echo "[5/7] Populating tables with initial data..."
if [ -f "/app/Resources/DDL Database/populate_tables.sql" ]; then
  psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f "/app/Resources/DDL Database/populate_tables.sql" -v ON_ERROR_STOP=0 2>&1 | grep -v "duplicate key" | grep -v "already exists" || true
  echo "  ✓ Initial data populated!"
else
  echo "  ⚠ Populate script not found at /app/Resources/DDL Database/populate_tables.sql"
fi

# Import test data from Objects folders
echo ""
echo "[6/7] Importing test data..."
if [ -d "/app/Resources/Objects" ]; then
  for sql_file in /app/Resources/Objects/*/insert_test_data*.sql; do
    if [ -f "$sql_file" ]; then
      echo "  Processing: $(basename $sql_file)"
      psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f "$sql_file" -v ON_ERROR_STOP=0 2>&1 | grep -v "duplicate key" | grep -v "already exists" || true
    fi
  done
  echo "  ✓ Test data imported!"
else
  echo "  ⚠ No test data files found"
fi

# Verify database setup
echo ""
echo "[7/7] Verifying database setup..."
echo "  Checking for required views..."
VIEWS=$(psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -t -c "SELECT COUNT(*) FROM information_schema.views WHERE table_schema = 'public' AND table_name LIKE 'viewget%';")
echo "  Found $VIEWS views"

if [ "$VIEWS" -gt 0 ]; then
  echo "  ✓ Database setup complete!"
else
  echo "  ⚠ Warning: Some views may not have been created"
fi

echo ""
echo "=========================================="
echo "Database initialization finished!"
echo "=========================================="
