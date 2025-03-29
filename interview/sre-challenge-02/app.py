import os
import time
import logging
import random
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import requests
import socket

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Environment variables for configuration
APP_MODE = os.getenv("APP_MODE", "normal")  # Options: normal, flaky, dependency_failure
DEPENDENCY_URL = os.getenv("DEPENDENCY_URL", "http://dependency-service:8081")  # Simulated dependency
PORT = int(os.getenv("PORT", "8080"))
HEALTH_CHECK_FAIL_RATE = float(os.getenv("HEALTH_CHECK_FAIL_RATE", "0.2"))  # 20% failure rate

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logger.info(f"Received GET request from {self.client_address}")
        
        if APP_MODE == "flaky" and random.random() < 0.5:
            logger.error("Simulating flaky behavior - returning 500")
            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Internal Server Error - Flaky mode!")
            return
        
        # Simulate dependency call
        try:
            if APP_MODE == "dependency_failure":
                raise requests.RequestException("Dependency unavailable")
            response = requests.get(DEPENDENCY_URL, timeout=2)
            if response.status_code != 200:
                raise requests.RequestException(f"Dependency returned {response.status_code}")
            message = f"Healthy response, dependency says: {response.text}"
        except requests.RequestException as e:
            logger.error(f"Dependency failure: {e}")
            self.send_response(503)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Service Unavailable - Dependency issue!")
            return
        
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(message.encode())

def health_check():
    """Periodic health check with configurable failure rate."""
    while True:
        if random.random() < HEALTH_CHECK_FAIL_RATE:
            logger.error("Health check failed intentionally!")
            with open("/health/status", "w") as f:
                f.write("unhealthy")
        else:
            logger.info("Health check passed")
            with open("/health/status", "w") as f:
                f.write("healthy")
        time.sleep(5)

def main():
    logger.info(f"Starting medium SRE test app with APP_MODE={APP_MODE} on port {PORT}")
    
    # Create health check file
    os.makedirs("/health", exist_ok=True)
    with open("/health/status", "w") as f:
        f.write("healthy")
    
    # Start health check thread
    health_thread = threading.Thread(target=health_check, daemon=True)
    health_thread.start()

    # Start HTTP server
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    logger.info(f"Server running on port {PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application crashed with error: {e}")
        sys.exit(1)