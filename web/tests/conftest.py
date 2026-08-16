import socket
import threading

import pytest
from werkzeug.serving import make_server

import app as app_module


def _free_port() -> int:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


@pytest.fixture(scope="session")
def live_server_url():
    """
    Runs the real Flask app (app.py, unmodified) in a background thread,
    so tests drive the same server a developer running `python3 app.py`
    would get - just on an ephemeral port instead of 5000.
    """
    port = _free_port()
    server = make_server("127.0.0.1", port, app_module.app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    yield f"http://127.0.0.1:{port}"

    server.shutdown()
    thread.join()


@pytest.fixture
def cube_page(page, live_server_url):
    """
    A Page loaded against a freshly-reset cube (the server holds one
    shared cube globally, so tests reset it via the real /api/reset
    endpoint rather than assuming test order).
    """
    page.request.post(f"{live_server_url}/api/reset")
    page.goto(live_server_url)
    page.wait_for_selector(".move-btn")
    yield page
