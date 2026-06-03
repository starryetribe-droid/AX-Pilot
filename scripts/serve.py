import os, http.server, socketserver
os.chdir(os.path.expanduser(os.environ.get('CHATBOT_OUT', '~/Downloads/SB_챗봇')))
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(('127.0.0.1', 8765), http.server.SimpleHTTPRequestHandler) as h:
    h.serve_forever()
