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
exec uvicorn --app-dir /app --reload --log-level $LOG_LEVEL "$APP_MODULE"

