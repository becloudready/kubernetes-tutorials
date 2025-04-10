#!/usr/bin/env python3
import os
import sys
import socket
import requests
from pathlib import Path
import time

def print_result(success, message):
    color = "\033[32m" if success else "\033[31m"
    symbol = "✓" if success else "✗"
    print(f"{color}{symbol} {message}\033[0m")

def print_header(title):
    print(f"\n\033[1m=== {title} ===\033[0m")

def check_config_map():
    """Verify ConfigMap mounting and content"""
    print_header("ConfigMap Verification")
    config_path = "/etc/app/config.yaml"
    issues_found = 0

    # Check file existence and readability
    if not Path(config_path).exists():
        print_result(False, f"Config file missing at {config_path}")
        issues_found += 1
    else:
        try:
            with open(config_path) as f:
                content = f.read()
            print_result(True, f"Config file exists at {config_path}")
            print(f"Content:\n{content}")
        except Exception as e:
            print_result(False, f"Failed to read config - {str(e)}")
            issues_found += 1

    # Check actual mounted files
    print("\nMounted files in /etc/app:")
    try:
        for f in Path('/etc/app').iterdir():
            print(f"  - {f.name}")
    except Exception as e:
        print(f"Error reading directory: {str(e)}")

    return issues_found == 0

def check_dns_resolution():
    """Test DNS resolution with detailed diagnostics"""
    print_header("DNS Resolution Test")
    test_hosts = {
        "Cluster DNS": "kubernetes.default.svc.cluster.local",
        "Internet": "google.com",
        "Config Reference": "db-service",
        "External API": "api.github.com"
    }

    all_success = True
    for name, host in test_hosts.items():
        try:
            start = time.time()
            ip = socket.gethostbyname(host)
            latency = (time.time() - start) * 1000
            print_result(True, f"{name.ljust(20)} → {ip.ljust(15)} ({latency:.2f}ms)")
        except Exception as e:
            print_result(False, f"{name.ljust(20)} → Failed: {str(e)}")
            all_success = False

    if not all_success:
        print("\nDNS Troubleshooting Steps:")

    return all_success

def check_network_connectivity():
    """Verify HTTP connectivity"""
    print_header("Network Connectivity")
    test_urls = {
        "HTTP": "http://google.com",
        "HTTPS": "https://google.com",
        "Cluster API": "https://kubernetes.default.svc.cluster.local"
    }

    all_success = True
    for name, url in test_urls.items():
        try:
            start = time.time()
            r = requests.get(url, timeout=5, verify=False)
            latency = (time.time() - start) * 1000
            print_result(True, f"{name.ljust(15)} → {r.status_code} ({latency:.2f}ms)")
        except Exception as e:
            print_result(False, f"{name.ljust(15)} → Failed: {str(e)}")
            all_success = False

    return all_success

def gather_system_info():
    """Collect diagnostic information"""
    print_header("System Diagnostics")

    # DNS Configuration
    print("\n/etc/resolv.conf:")
    try:
        print(Path('/etc/resolv.conf').read_text())
    except Exception as e:
        print(f"Error: {str(e)}")

    # Mount Information
    print("\nActive Mounts:")
    try:
        print(Path('/proc/mounts').read_text())
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    print("\033[1m=== Kubernetes Troubleshooting Diagnostic ===\033[0m")

    # Run diagnostic checks
    config_ok = check_config_map()
    dns_ok = check_dns_resolution()
    network_ok = check_network_connectivity()

    # Show detailed info if any checks failed
    if not all([config_ok, dns_ok, network_ok]):
        gather_system_info()

        print("\n\033[1mTROUBLESHOOTING GUIDE:\033[0m")
        if not config_ok:
            print("\nConfigMap Issues Detected:")

        if not dns_ok or not network_ok:
            print("\nDNS/Network Issues Detected:")
        sys.exit(1)

    print("\nDiagnostic complete. Container will remain running...")
    while True:
        time.sleep(3600)  # Keep container alive

if __name__ == "__main__":
    main()

