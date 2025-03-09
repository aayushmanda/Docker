#!/bin/bash
set -e  # Exit on any error

echo "Starting PostgreSQL validation..."

# Start PostgreSQL in the background
docker-entrypoint.sh postgres &

# Wait for PostgreSQL to be ready
until pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  echo "Waiting for PostgreSQL to start..."
  sleep 2
done

echo "PostgreSQL is running!"



# Check if the database exists
DB_EXISTS=$(psql -U "$POSTGRES_USER" -tAc "SELECT 1 FROM pg_database WHERE datname='$POSTGRES_DB';")

if [ "$DB_EXISTS" != "1" ]; then
    echo "Database $POSTGRES_DB does not exist. Creating database..."
    psql -U "$POSTGRES_USER" -c "CREATE DATABASE $POSTGRES_DB;"
else
    echo "Database $POSTGRES_DB already exists."
fi



# Check if the table exists
TABLE_EXISTS=$(psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc "SELECT 1 FROM information_schema.tables WHERE table_name='users';")

if [ "$TABLE_EXISTS" != "1" ]; then
    echo "Table 'users' not found. Creating table..."
    psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /init.sql
else
    echo "Table already exists. Skipping initialization."
fi

echo "PostgreSQL setup complete. Running database service..."

# Bring PostgreSQL to the foreground so the container doesn't exit
wait -n
