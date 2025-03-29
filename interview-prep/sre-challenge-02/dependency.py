from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PORT = int(os.getenv("PORT", "8081"))

class DependencyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logger.info("Dependency service received request")
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Dependency service is up!")

def main():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, DependencyHandler)
    logger.info(f"Dependency service running on port {PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    main()