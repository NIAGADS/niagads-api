#! /usr/bin/env sh
set -e

export APP_MODULE=api.main:app

if [ "$BUILD_ENV" = "dev" ]
then
    LOG_LEVEL="debug"
else
    LOG_LEVEL="info"
fi

echo "Build: $BUILD_ENV / Log Level: ${LOG_LEVEL}"

# Start Uvicorn with live reload
# --host 0.0.0.0 tells uvicorn to ignore host machine IP
exec uvicorn --app-dir /app --host 0.0.0.0 --port 8000 --reload --reload-dir /app/api --log-level $LOG_LEVEL "$APP_MODULE" 

