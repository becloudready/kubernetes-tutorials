#!/bin/sh

# This script simulates various failure modes based on environment variables

# OOM Killer scenario
if [ "$FAILURE_MODE" = "oom" ]; then
    echo "Simulating out-of-memory condition"
    /consume-memory.sh
    exit 1
fi

# Missing file scenario
if [ "$FAILURE_MODE" = "missing_file" ]; then
    echo "Simulating missing file error"
    cat /problematic/missing-file
    exit 1
fi

# DNS issues scenario
if [ "$FAILURE_MODE" = "dns" ]; then
    echo "Simulating DNS issues"
    /dns-issues.sh
    exit 1
fi

# Scheduling problems (long startup)
if [ "$FAILURE_MODE" = "slow_start" ]; then
    echo "Simulating slow starting container"
    sleep 300
    echo "Finally started after 5 minutes"
    exec tail -f /dev/null
fi

# Healthy scenario
echo "Running in healthy mode"
exec tail -f /dev/null
