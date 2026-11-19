# Servidor local temporario que entrega so o .zip do jogo para a pagina do itch.io (com CORS).
import http.server, sys, os

ZIP = sys.argv[1]
ORIGIN = 'https://itch.io'


class H(http.server.BaseHTTPRequestHandler):
    def cors(self):
        self.send_header('Access-Control-Allow-Origin', ORIGIN)
        self.send_header('Access-Control-Allow-Private-Network', 'true')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')

    def do_OPTIONS(self):
        self.send_response(204); self.cors(); self.end_headers()

    def do_GET(self):
        if self.path.split('?')[0] != '/jogo-bruno-web.zip':
            self.send_response(404); self.cors(); self.end_headers(); return
        data = open(ZIP, 'rb').read()
        self.send_response(200); self.cors()
        self.send_header('Content-Type', 'application/zip')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers(); self.wfile.write(data)

    def log_message(self, *a):
        pass


http.server.ThreadingHTTPServer(('127.0.0.1', 8767), H).serve_forever()
