#! /usr/bin/env sh
set -e

export APP_MODULE=api.main:app
LOG_LEVEL=${LOG_LEVEL}
BUILD=${BUILD_ENV:-dev}

# If there's a prestart.sh script in the /app directory or other path specified, run it before starting
PRE_START_PATH=/app/prestart.sh
echo "Checking for script in $PRE_START_PATH"
if [ -f $PRE_START_PATH ] ; then
    echo "Running script $PRE_START_PATH"
    . "$PRE_START_PATH"
else 
    echo "There is no script $PRE_START_PATH"
fi

# Start Uvicorn with live reload
exec uvicorn --reload --log-level $LOG_LEVEL "$APP_MODULE"

# Start nextjs app
exec npm run start-$BUILD