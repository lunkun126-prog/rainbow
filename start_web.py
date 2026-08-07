"""雨后的天空 · 彩虹 Demo 本地服务器 @ 8060"""
import http.server, socketserver, webbrowser, os

PORT = 8060
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):  # 安静一点
        pass

with socketserver.ThreadingTCPServer(("", PORT), Handler) as httpd:
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    url = f"http://localhost:{PORT}/index.html"
    print(f"🌈 雨后的天空: {url}")
    if os.environ.get("LP_NO_OPEN") != "1":  # launchpad 托管时由它统一开浏览器
        webbrowser.open(url)
    httpd.serve_forever()
