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
    print_header("ConfigMap Verification")
    config_path = "/etc/app/config.yaml"
    issues_found = 0
    
    # Check if file exists
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
    
    return issues_found == 0

def check_dns():
    """Check DNS resolution with detailed diagnostics"""
    print_header("DNS Resolution")
    test_hosts = {
        "Cluster Service": "kubernetes.default.svc.cluster.local",
        "Internet": "google.com",
        "Cluster Shortname": "kubernetes.default",
        "Config Reference": "db-service"  # From our config
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
    
    
    return all_success

def gather_diagnostics():
    """Collect system information for troubleshooting"""
    print_header("System Diagnostics")
    
    print("\nDNS Configuration:")
    try:
        print(Path('/etc/resolv.conf').read_text())
    except Exception as e:
        print(f"Error reading resolv.conf: {str(e)}")
    
    print("\nVolume Mounts:")
    try:
        print(Path('/proc/mounts').read_text())
    except Exception as e:
        print(f"Error reading mounts: {str(e)}")
    
    print("\nConfigMap Directory Contents:")
    try:
        for f in Path('/etc/app').iterdir():
            print(f"  - {f.name}")
    except Exception as e:
        print(f"Error reading directory: {str(e)}")

def main():
    print("\033[1m=== Kubernetes Troubleshooting Interview ===\033[0m")
    
    # Run all checks
    config_ok = check_config_map()
    dns_ok = check_dns()
    
    # Show diagnostics if any checks failed
    if not config_ok or not dns_ok:
        gather_diagnostics()
        
        print("\n\033[1mTroubleshooting Summary:\033[0m")
        if not config_ok:
            print("- ConfigMap issue detected (mount or content)")
        if not dns_ok:
            print("- DNS resolution problem")
        
        print("\nInvestigation Path:")
        print("config1.yaml does not exist")
        print("Examine the pod DNS configuration")

if __name__ == "__main__":
    main()
