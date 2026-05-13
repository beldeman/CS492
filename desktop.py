import threading
import time
import socket

import webview
from werkzeug.serving import make_server
from server import app

HOST = "127.0.0.1"
PORT = 5000


def wait_for_server(host: str, port: int, timeout: float = 10.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError(f"Server did not start on {host}:{port} within {timeout} seconds")


def main() -> None:
    server = make_server(HOST, PORT, app)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    wait_for_server(HOST, PORT)

    webview.create_window("PizzaShop", f"http://{HOST}:{PORT}", width=1100, height=800)
    webview.start()

    server.shutdown()
    server_thread.join()


if __name__ == "__main__":
    main()
