#!/bin/sh

# Health check script that fails in various ways
if [ -f "/tmp/fail-health-check" ]; then
    echo "Health check failing as requested"
    exit 1
fi

if [ "$(hostname)" = "unhealthy-pod" ]; then
    echo "Failing health check due to hostname"
    exit 1
fi

exit 0
