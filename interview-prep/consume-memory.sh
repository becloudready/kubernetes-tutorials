#!/bin/sh

# Script to consume memory and trigger OOM killer
echo "Allocating memory to trigger OOM killer..."
stress-ng --vm 1 --vm-bytes 90% -t 60s
