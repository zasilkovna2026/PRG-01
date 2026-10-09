"""PRG-01 local bridge: run with python local/server.py while dump1090 --net runs."""
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.request import urlopen
import json

HERE = Path(__file__).resolve().parent
UPSTREAM = "http://127.0.0.1:8080"
PORT = 8765

def aircraft():
    for path in ("/data/aircraft.json", "/data.json", "/aircraft.json"):
        try:
            with urlopen(UPSTREAM + path, timeout=2) as response:
                obj = json.load(response)
            if isinstance(obj, dict):
                if isinstance(obj.get("aircraft"), list):
                    return obj["aircraft"]
                if isinstance(obj.get("ac"), list):
                    return obj["ac"]
            if isinstance(obj, list):
                return obj
        except (OSError, ValueError, KeyError):
            pass
    raise RuntimeError("No aircraft JSON available from dump1090 on port 8080")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?")[0] == "/api/aircraft":
            try:
                body = json.dumps({"aircraft": aircraft()}).encode()
                status = 200
            except Exception as error:
                body = json.dumps({"error": str(error)}).encode()
                status = 503
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
        elif self.path.split("?")[0] in ("/", "/index.html"):
            body = (HERE / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
        else:
            self.send_error(404)
            return
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

if __name__ == "__main__":
    print(f"PRG-01 LOCAL: http://localhost:{PORT}")
    print(f"Samsung (same Wi-Fi): http://192.168.0.164:{PORT}  [IP may change]")
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
