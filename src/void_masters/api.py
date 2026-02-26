import json
import threading
import uuid
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from datetime import datetime

from .tasks import TASKS, run_task_background


class CraftHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/craft":
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())
            return

        content_length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(content_length) if content_length > 0 else b""
        try:
            payload = json.loads(raw.decode("utf-8")) if raw else {}
        except Exception:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())
            return

        age = payload.get("age")
        names = payload.get("names")

        if not isinstance(names, list) or not all(isinstance(n, str) for n in names):
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "`names` must be an array of strings"}).encode())
            return

        if not isinstance(age, str):
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "`age` must be a string"}).encode())
            return

        inputs = {
            "age": age,
            "names": ", ".join(names),
            "names_array": names,
            "current_year": str(datetime.now().year),
        }

        # queue task
        task_id = uuid.uuid4().hex
        TASKS[task_id] = {"status": "queued", "created_at": datetime.now().isoformat(), "output_path": None}
        thread = threading.Thread(target=run_task_background, args=(task_id, inputs), daemon=True)
        thread.start()

        self._set_headers(202)
        self.wfile.write(json.dumps({"status": "accepted", "task_id": task_id}).encode())

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/craft/status":
            params = parse_qs(parsed.query)
            task_ids = params.get("task_id") or params.get("id")
            if not task_ids:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "task_id query parameter required"}).encode())
                return

            task_id = task_ids[0]
            task = TASKS.get(task_id)
            if not task:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "task not found"}).encode())
                return

            self._set_headers(200)
            safe = {k: (v if isinstance(v, (str, int, float, bool, type(None))) else str(v)) for k, v in task.items()}
            self.wfile.write(json.dumps({"task_id": task_id, "task": safe}).encode())
            return
        elif parsed.path == "/craft/download":
            params = parse_qs(parsed.query)
            task_ids = params.get("task_id") or params.get("id")
            if not task_ids:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "task_id query parameter required"}).encode())
                return

            task_id = task_ids[0]
            task = TASKS.get(task_id)
            if not task:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "task not found"}).encode())
                return

            path = task.get("output_path")
            if not path or not os.path.isfile(path):
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "output not available"}).encode())
                return

            try:
                with open(path, "rb") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/markdown")
                self.send_header("Content-Disposition", f"attachment; filename=\"{os.path.basename(path)}\"")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return

        # fallback
        self._set_headers(404)
        self.wfile.write(json.dumps({"error": "Not Found"}).encode())


def run_server(host: str = "0.0.0.0", port: int = 8000):
    server = HTTPServer((host, port), CraftHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    print(f"🚀 Serving /craft on http://{host}:{port}")
    try:
        thread.start()
        while thread.is_alive():
            thread.join(1)
    except KeyboardInterrupt:
        print("Shutting down server...")
        server.shutdown()
        server.server_close()
