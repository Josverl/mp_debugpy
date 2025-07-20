import time
from typing import Dict, List

import pytest
from dap import ThreadedServer


class PerfServer(ThreadedServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rcv_messages: List[Dict] = []  # Instance variable, not class variable

    def handle_message(self, message):
        """Handle a message from the client or adapter."""
        self.rcv_messages.append(message)
        print("Message received:", message)

    def clear_messages(self):
        """Clear all received messages."""
        self.rcv_messages.clear()


@pytest.fixture
def fake_vscode_server(micropython_debuggee):
    """Fixture to start the debug server for testing.
    This fixture initializes the PerfServer with the host and port from the micropython_debuggee fixture.
    can be parameterized with:
    - tgt_module: The target module to run.
    - tgt_method: The target method to run.
    - free_tcp_port: The port to bind the server to.
    """
    process, port = micropython_debuggee
    assert process is not None, "Process should not be None"
    name = "debugpy"
    server = PerfServer(name, host="localhost", port=port)

    # Ensure clean state for each test
    server.clear_messages()

    yield server

    # Cleanup
    try:
        server.stop()
    except Exception as e:
        print(f"Error stopping server: {e}")
