import os
import sys

# Add the tests directory to sys.path to enable absolute imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import time
from pathlib import Path
from typing import List

import pytest
from helpers import PerfServer


# simple fixtures to provide defaults
@pytest.fixture
def local_root(request):
    # attach
    if hasattr(request, "param"):
        yield request.param
    else:
        # Default value if not parameterized
        yield "./src"


@pytest.fixture
def remote_root(request):
    # attach
    if hasattr(request, "param"):
        yield request.param
    else:
        # Default value if not parameterized
        yield "./src"


@pytest.fixture
def attach_server(
    fake_vscode_server: PerfServer,
    free_tcp_port: int,
    logToFile: bool,
    local_root: str,
    remote_root: str,
):
    """
    Setup the fake_vscode_server for testing
    Ensure clean state at start of test

    This fixture initializes the PerfServer with the host and port from the fake_vscode_server fixture.
    It can be parameterized with:
    - attach_delay: The delay to wait before running the server.
    - logToFile: Whether to log to file.
    - free_tcp_port: The port to bind the server to.
    """
    server = fake_vscode_server
    assert server is not None, "Server should not be None"

    server.clear_messages()

    server.start()
    for _ in range(5):
        time.sleep(0.01)
        server.run_single()

    client = server.client

    # Start of test
    client.send_request(
        "attach",
        {
            "name": "Attach to MicroPython",
            # "preLaunchTask": "foo_bar",
            "type": "debugpy",
            "request": "attach",
            "connect": {"host": "localhost", "port": free_tcp_port},
            "pathMappings": [
                {
                    "localRoot": local_root,
                    "remoteRoot": remote_root,
                }
            ],
            "workspaceFolder": "/home/jos/mp_debugpy",
            "justMyCode": True,
            "logToFile": logToFile,
            # "__configurationTarget": 6,
            "clientOS": "unix",
            "debugOptions": [
                "RedirectOutput",
                "ShowReturnValue",
            ],
            "showReturnValue": True,
            "__sessionId": "11976c7b-f770-484d-a445-115e82e3abcb",
        },
    )
    # do not add a wait or processing at this point
    yield server

