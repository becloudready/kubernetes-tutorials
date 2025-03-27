#!/bin/sh

# Script to simulate DNS issues
echo "Original /etc/resolv.conf:"
cat /etc/resolv.conf

echo "Overwriting /etc/resolv.conf with bad nameserver"
echo "nameserver 10.255.255.1" > /etc/resolv.conf

echo "New /etc/resolv.conf:"
cat /etc/resolv.conf

echo "Attempting to resolve kubernetes.default..."
nslookup kubernetes.default
