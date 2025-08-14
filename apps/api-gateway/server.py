import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from prometheus_client import CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST

registry = CollectorRegistry()

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/metrics':
            data = generate_latest(registry)
            self.send_response(200)
            self.send_header('Content-Type', CONTENT_TYPE_LATEST)
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_response(404)
            self.end_headers()

def main():
    port = int(os.getenv('PORT', '8080'))
    HTTPServer(('', port), MetricsHandler).serve_forever()

if __name__ == '__main__':
    main()
