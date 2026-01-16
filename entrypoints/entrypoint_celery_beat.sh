#!/bin/bash
set -e

echo "Starting Celery beat..."
exec celery -A celery_app beat -l info