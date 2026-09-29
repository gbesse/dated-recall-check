import json
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from compare import recall


class HttpTest(unittest.TestCase):
    def test_hindsight_recall_request(self):
        seen = {}
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_): pass
            def do_POST(self):
                seen['path'] = self.path
                seen['body'] = json.loads(self.rfile.read(int(self.headers['content-length'])))
                payload = json.dumps({'results': [{'id': 'fact-1', 'text': 'Decision'}]}).encode()
                self.send_response(200); self.send_header('content-length', str(len(payload))); self.end_headers(); self.wfile.write(payload)
        server = HTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.handle_request); thread.start()
        try:
            ids = recall(f'http://127.0.0.1:{server.server_port}', 'bank one', {'query': 'When?', 'query_timestamp': '2026-09-01T00:00:00Z'})
        finally:
            thread.join(3); server.server_close()
        self.assertEqual(ids, ['fact-1'])
        self.assertEqual(seen['path'], '/v1/default/banks/bank%20one/memories/recall')
        self.assertEqual(seen['body']['query_timestamp'], '2026-09-01T00:00:00Z')
