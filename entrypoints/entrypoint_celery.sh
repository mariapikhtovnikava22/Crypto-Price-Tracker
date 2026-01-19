#!/bin/bash
set -e

echo "Starting Celery worker..."
exec celery -A celery_app worker -l info 