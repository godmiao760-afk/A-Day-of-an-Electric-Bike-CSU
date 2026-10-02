"""Serve the game locally and open it in a browser."""

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
import threading
from urllib.request import urlopen
import webbrowser


ROOT = Path(__file__).resolve().parent


class GameHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Browser refreshes should pick up the latest edited scripts and art.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


class GameServer(ThreadingHTTPServer):
    allow_reuse_address = False


def main():
    parser = argparse.ArgumentParser(description="Run 小电驴的一天 locally")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()

    handler = partial(GameHandler, directory=str(ROOT))
    url = f"http://127.0.0.1:{args.port}/"
    try:
        server = GameServer(("127.0.0.1", args.port), handler)
    except OSError as exc:
        try:
            with urlopen(url, timeout=2) as response:
                existing_page = response.read(4096).decode("utf-8", errors="replace")
            if "<title>小电驴的一天</title>" in existing_page and "vendor/phaser.min.js" in existing_page:
                print(f"游戏服务器已经在运行：{url}")
                if not args.no_browser:
                    webbrowser.open(url)
                return 0
        except OSError:
            pass
        print(f"端口 {args.port} 无法使用：{exc}", file=sys.stderr)
        print("可以运行 python start_game.py --port 8766 换一个端口。", file=sys.stderr)
        return 1

    print(f"游戏地址：{url}", flush=True)
    print("保持此窗口打开；按 Ctrl+C 停止服务器。", flush=True)
    if not args.no_browser:
        threading.Timer(0.5, webbrowser.open, args=(url,)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止。")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
