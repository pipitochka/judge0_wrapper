#!/bin/sh
set -e

# Check if we're in debug mode (SQLite)
DEBUG="${TASK_CHECKER_DEBUG:-false}"
DEBUG_LOWER=$(echo "$DEBUG" | tr '[:upper:]' '[:lower:]')

if [ "$DEBUG_LOWER" = "true" ] || [ "$DEBUG_LOWER" = "1" ] || [ "$DEBUG_LOWER" = "t" ] || [ "$DEBUG_LOWER" = "y" ]; then
    echo "Running in debug mode with SQLite..."
else
    # Wait for PostgreSQL database to be ready
    DB_HOST="${DB_HOST:-task-checker-db}"
    DB_PORT="${DB_PORT:-5432}"
    
    echo "Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."
    
    # Simple wait loop using Python
    until python -c "
import socket
import sys
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect(('$DB_HOST', $DB_PORT))
    s.close()
    sys.exit(0)
except (socket.error, OSError):
    sys.exit(1)
" 2>/dev/null; do
        echo "Database is not ready yet. Waiting..."
        sleep 2
    done
    
    echo "Database is ready!"
    
    # Additional wait to ensure PostgreSQL is fully initialized
    sleep 3
fi

# Load fixtures only on first run (controlled by LOAD_FIXTURES env var, default: true)
# The load_fixture.py script checks if data already exists and skips if so
if [ "${LOAD_FIXTURES:-true}" = "true" ]; then
    echo "Checking and loading fixtures if needed..."
    if python src/load_fixture.py; then
        echo "Fixtures check completed"
    else
        echo "Fixtures loading failed"
    fi
fi

# Start the application
echo "Starting application..."
exec python src/app.py
