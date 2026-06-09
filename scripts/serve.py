import os, http.server, socketserver
os.chdir(os.path.expanduser(os.environ.get('CHATBOT_OUT', '~/Downloads/SB_챗봇')))

class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with Server(('127.0.0.1', 8765), http.server.SimpleHTTPRequestHandler) as h:
    h.serve_forever()
