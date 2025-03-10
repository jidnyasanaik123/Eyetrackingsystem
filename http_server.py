from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess

class RequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/start-tracking":
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")  # ✅ Fix CORS issue
            self.send_header("Content-type", "application/json")
            self.end_headers()
            
            subprocess.Popen(["python", "finaleyetrack.py"])  # ✅ Run eye tracking script
            self.wfile.write(b'{"message": "Eye tracking started!"}')

server_address = ("", 8000)
httpd = HTTPServer(server_address, RequestHandler)
print("✅ Server running on port 8000...")
httpd.serve_forever()
