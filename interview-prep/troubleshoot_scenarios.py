#!/usr/bin/env python3
import os
import sys
import time
import signal
import subprocess
from pathlib import Path

def simulate_oom():
    """Simulate out-of-memory condition"""
    print("Simulating out-of-memory condition")
    try:
        # Allocate memory aggressively
        import numpy as np
        print("Allocating memory using numpy...")
        chunks = []
        while True:
            chunks.append(np.zeros((1024, 1024)))  # Allocate 8MB chunks
            print(f"Allocated {len(chunks) * 8}MB so far...")
            time.sleep(0.1)
    except MemoryError:
        print("MemoryError occurred - OOM killer likely triggered")
        return 1
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

def simulate_missing_file():
    """Simulate missing file error"""
    print("Simulating missing file error")
    missing_file = "/problematic/missing-file"
    try:
        with open(missing_file, "r") as f:
            content = f.read()
        print("Unexpected success - file exists!")
        return 0
    except FileNotFoundError:
        print(f"FileNotFoundError: {missing_file} does not exist")
        return 1
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

def simulate_dns_issues():
    """Simulate DNS resolution problems"""
    print("Simulating DNS issues")
    
    # Backup original resolv.conf
    resolv_conf = Path("/etc/resolv.conf")
    if resolv_conf.exists():
        original_content = resolv_conf.read_text()
    else:
        original_content = ""
    
    try:
        # Write bad DNS config
        print("Overwriting /etc/resolv.conf with bad nameserver")
        resolv_conf.write_text("nameserver 10.255.255.1\n")
        
        # Try to resolve
        print("Current /etc/resolv.conf:")
        print(resolv_conf.read_text())
        
        print("Attempting to resolve kubernetes.default...")
        try:
            import socket
            print(socket.gethostbyname("kubernetes.default"))
        except Exception as e:
            print(f"Resolution failed: {str(e)}")
        
        return 1
    finally:
        # Restore original config if we modified it
        if original_content:
            print("Restoring original /etc/resolv.conf")
            resolv_conf.write_text(original_content)

def simulate_slow_start():
    """Simulate slow starting container"""
    print("Simulating slow starting container")
    time.sleep(300)
    print("Finally started after 5 minutes")
    return 0

def health_check():
    """Health check endpoint that can fail in various ways"""
    if Path("/tmp/fail-health-check").exists():
        print("Health check failing as requested by /tmp/fail-health-check")
        return 1
    
    hostname = os.getenv("HOSTNAME", "")
    if "unhealthy" in hostname.lower():
        print(f"Failing health check due to hostname: {hostname}")
        return 1
    
    print("Health check passed")
    return 0

def main():
    # Determine which mode to run in
    failure_mode = os.getenv("FAILURE_MODE", "").lower()
    
    if failure_mode == "oom":
        sys.exit(simulate_oom())
    elif failure_mode == "missing_file":
        sys.exit(simulate_missing_file())
    elif failure_mode == "dns":
        sys.exit(simulate_dns_issues())
    elif failure_mode == "slow_start":
        sys.exit(simulate_slow_start())
    elif failure_mode == "health_check":
        sys.exit(health_check())
    else:
        print("Running in healthy mode")
        while True:
            time.sleep(60)

if __name__ == "__main__":
    main()
