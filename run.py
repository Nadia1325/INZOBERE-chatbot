import http.server,socketserver,webbrowser,os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
P=8000
with socketserver.TCPServer(("",P),http.server.SimpleHTTPRequestHandler) as s:
    print(f"Inzobere running -> http://localhost:{P}  (Ctrl+C to stop)")
    webbrowser.open(f"http://localhost:{P}/index.html"); s.serve_forever()
