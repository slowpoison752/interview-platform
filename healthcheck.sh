#!/bin/sh

# Health check script for Railway
# This script checks if the application is responding

echo "Performing health check..."

# Wait a bit for the application to start
sleep 5

# Check if the application is responding
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Health check passed - Application is running"
    exit 0
else
    echo "❌ Health check failed - Application is not responding"
    exit 1
fi 