# Factory Manager - Docker Setup Guide

## Quick Start

### First Time Setup

1. **Start all services** (this will automatically initialize everything):
   ```bash
   docker-compose up --build
   ```

   The startup process will automatically:
   - ✅ Create database tables
   - ✅ Import database objects (views, functions, stored procedures)
   - ✅ Apply database privileges
   - ✅ Populate initial data
   - ✅ Run Django migrations
   - ✅ Create Django superuser
   - ✅ Seed MongoDB
   - ✅ Start the Django development server

2. **Access the application**:
   - URL: http://localhost:8000
   - Admin user: `admin` (default)
   - Password: `adminpass` (default)

### Reset Everything

If you need to completely reset the database and start fresh:

```bash
# Stop containers and remove volumes
docker-compose down -v

# Start fresh (will reinitialize everything)
docker-compose up --build
```

## Configuration

### Environment Variables

Create a `.env` file in the project root to customize settings:

```env
# PostgreSQL
POSTGRES_DB=factorydb
POSTGRES_USER=factoryuser
POSTGRES_PASSWORD=factorypass
POSTGRES_HOST=db
POSTGRES_PORT=5432

# MongoDB
MONGO_URI=mongodb://mongo:27017/
MONGO_DB_NAME=projetofinal

# Django Superuser
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=adminpass
```

## Initialization Process

The `scripts/init_database.sh` script runs automatically and performs these steps:

1. **Wait for PostgreSQL** - Ensures database is ready
2. **Create Tables** - Runs DDL script to create all tables
3. **Import Objects** - Creates views, functions, and stored procedures
4. **Apply Privileges** - Sets up database permissions
5. **Populate Data** - Inserts initial/test data
6. **Import Test Data** - Loads sample data from Objects folders
7. **Verify Setup** - Checks that views were created successfully

After database initialization, Django performs:
- Database migrations
- Superuser creation
- MongoDB seeding

## Manual Commands

### View Logs
```bash
docker-compose logs -f web
```

### Access PostgreSQL
```bash
docker-compose exec db psql -U factoryuser -d factorydb
```

### Access MongoDB
```bash
docker-compose exec mongo mongosh projetofinal
```

### Run Django Management Commands
```bash
docker-compose exec web python3 manage.py <command>
```

### Manually Re-run Database Initialization
```bash
docker-compose exec web bash /app/scripts/init_database.sh
```

### Manually Import Database Objects
```bash
docker-compose exec web python3 /app/scripts/import_objects.py
```

## Troubleshooting

### Database Connection Issues
If you see "PostgreSQL is unavailable" messages for more than 30 seconds:
1. Check if the database container is running: `docker-compose ps`
2. View database logs: `docker-compose logs db`
3. Restart services: `docker-compose restart`

### Missing Views/Functions
If pages show empty tables or errors about missing views:
1. Check initialization logs: `docker-compose logs web | grep "Importing database objects"`
2. Manually run: `docker-compose exec web bash /app/scripts/init_database.sh`
3. Verify views exist: `docker-compose exec db psql -U factoryuser -d factorydb -c "\dv"`

### ReverseMatch Errors
These have been fixed in the code. If you still see them:
1. Ensure you're using the latest code
2. Rebuild containers: `docker-compose up --build`

## Architecture

### Services
- **db** - PostgreSQL 15 database
- **mongo** - MongoDB 6 for equipment data
- **web** - Django application server

### Volumes
- `postgres_data` - Persistent PostgreSQL data
- `mongo_data` - Persistent MongoDB data

### Ports
- `5432` - PostgreSQL
- `27017` - MongoDB
- `8000` - Django web server

## Development

### Stop Services
```bash
docker-compose down
```

### Stop and Remove Data
```bash
docker-compose down -v
```

### Rebuild Containers
```bash
docker-compose up --build
```

### View All Running Containers
```bash
docker-compose ps
```

## Files Modified

Recent fixes applied:
- ✅ Fixed URL naming conflicts (supplier and user apps)
- ✅ Fixed database error handling (all database.py files)
- ✅ Added comprehensive initialization script
- ✅ Updated docker-compose for automated setup
- ✅ Added PostgreSQL client to web container

See `FIXES_APPLIED.md` for detailed information about the fixes.
