#!/usr/bin/env python3
import os
import sys
import time
import signal
import subprocess
from pathlib import Path

## Try to open a file inside the container
## Have that file mounted using configmap with small typo 
## Ensure that configmap is defined into the deployment file


def simulate_missing_file():
    missing_file = "/problematic/missing-file1"
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

### Ensure you give wrong nameserver in the deployment file
### In this function try to curl using python request open google.com and throw error message detail enough
### someone can troubleshoot

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



def main():
    # Determine which mode to run in


if __name__ == "__main__":
    main()
