#!/usr/bin/env python3
# JowOS 同步服务器（自托管版）
# 跑在安卓 Termux / Mac / 任意有 Python3 的机器上。
# 协议与 Cloudflare Worker 完全一致：GET 读 jowos-data.json，POST 写。
# JowOS 前端无需任何改动，只把「Worker 地址」指向本服务即可。
#
# 用法（Termux 里）：
#   export JOWOS_KEY="换成你自己的长随机口令"
#   python3 jowos-sync-server.py --host 0.0.0.0 --port 8765 --data $HOME/jowos-data.json
import os, json, argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

def load_key():
    env = os.environ.get("JOWOS_KEY")
    if env:
        return env
    # 同目录下的密钥文件（部署时由 setup 脚本写入，避免口令出现在命令行/进程列表）
    here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jowos-key.txt")
    try:
        with open(here, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return ""

KEY = load_key()
DATA = os.path.expanduser("~/jowos-data.json")
PORT = 8765
HOST = "0.0.0.0"

def parse_args():
    global PORT, HOST, DATA
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="0.0.0.0")
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--data", default="~/jowos-data.json")
    a = p.parse_args()
    HOST, PORT, DATA = a.host, a.port, os.path.expanduser(a.data)

class H(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "content-type,x-jowos-key")
    def _auth(self):
        return self.headers.get("x-jowos-key") == KEY
    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()
    def do_GET(self):
        if not self._auth():
            self.send_response(401); self._cors(); self.end_headers(); self.wfile.write(b"unauthorized"); return
        try:
            with open(DATA, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            content = "{}"
        self.send_response(200); self._cors()
        self.send_header("Content-Type", "application/json")
        self.end_headers(); self.wfile.write(content.encode("utf-8"))
    def do_POST(self):
        if not self._auth():
            self.send_response(401); self._cors(); self.end_headers(); self.wfile.write(b"unauthorized"); return
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            json.loads(body)  # 校验 JSON
        except Exception as e:
            self.send_response(400); self._cors(); self.end_headers(); self.wfile.write(("invalid json: "+str(e)).encode()); return
        try:
            d = os.path.dirname(DATA) or "."
            os.makedirs(d, exist_ok=True)
            with open(DATA, "w", encoding="utf-8") as f:
                f.write(body)
            self.send_response(200); self._cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers(); self.wfile.write(b'{"ok":true}')
        except Exception as e:
            self.send_response(500); self._cors(); self.end_headers(); self.wfile.write(("error: "+str(e)).encode())
    def log_message(self, *a):
        pass

if __name__ == "__main__":
    parse_args()
    if not KEY:
        print("❌ 未找到密钥：请设置 JOWOS_KEY 环境变量，或在脚本同目录放 jowos-key.txt")
        import sys
        sys.exit(1)
    print(f"JowOS sync server  ->  http://{HOST}:{PORT}   data={DATA}")
    ThreadingHTTPServer((HOST, PORT), H).serve_forever()
