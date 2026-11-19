# Servidor local para testar o jogo no navegador e salvar capturas de tela.
import base64, functools, http.server, os, sys

PORT = int(sys.argv[1])
ROOT = sys.argv[2]
OUT = sys.argv[3]
os.makedirs(OUT, exist_ok=True)


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def do_POST(self):
        if not self.path.startswith('/snap'):
            self.send_error(404)
            return
        name = self.path.split('name=')[-1] if 'name=' in self.path else 'snap'
        name = ''.join(c for c in name if c.isalnum() or c in '-_') or 'snap'
        body = self.rfile.read(int(self.headers.get('Content-Length', 0))).decode()
        with open(os.path.join(OUT, name + '.png'), 'wb') as f:
            f.write(base64.b64decode(body.split(',', 1)[1]))
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'ok')

    def log_message(self, *args):
        pass


http.server.ThreadingHTTPServer(('127.0.0.1', PORT), functools.partial(Handler, directory=ROOT)).serve_forever()
