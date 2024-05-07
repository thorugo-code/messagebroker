import sys
from .settings import API_PORT
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        message = "GET response"
        self.wfile.write(bytes(message, "utf8"))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        message = "POST response"
        self.wfile.write(bytes(message, "utf8"))

    def do_PUT(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        message = "PUT response"
        self.wfile.write(bytes(message, "utf8"))


def start():
    try:
        with HTTPServer(('', API_PORT), Handler) as server:
            print(f"Server started on port {API_PORT}")
            server.serve_forever()

    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(5)
