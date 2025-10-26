import os
import sys

# Add the tests directory to sys.path to enable absolute imports
tests_dir = os.path.dirname(os.path.dirname(__file__))
if tests_dir not in sys.path:
    sys.path.insert(0, tests_dir)

import time
from typing import Dict, List

import pytest
from anyio import Path
from helpers import PerfServer



@pytest.fixture
def logToFile(request):
    # attach
    if hasattr(request, "param"):
        yield request.param
    else:
        # Default value if not parameterized
        yield False


@pytest.fixture
def source_file(request):
    # set_breakpoints
    if hasattr(request, "param"):
        yield request.param
    else:
        # Default value if not parameterized
        yield "target.py"


@pytest.fixture
def bp_lines(request):
    # set_breakpoints
    if hasattr(request, "param"):
        yield request.param
    else:
        # Default value if not parameterized
        yield [78, 89, 90]


@pytest.fixture
def fake_vscode_server(micropython_debuggee, free_tcp_port):
    """Fixture to start the debug server for testing.
    This fixture initializes the PerfServer with the host and port from the micropython_debuggee fixture.
    can be parameterized with:
    - tgt_module: The target module to run.
    - tgt_method: The target method to run.
    - free_tcp_port: The port to bind the server to.
    """
    process = micropython_debuggee
    assert process is not None, "Process should not be None"
    name = "debugpy"
    server = PerfServer(name, host="localhost", port=free_tcp_port)

    # Ensure clean state for each test
    server.clear_messages()

    yield server

    # Cleanup
    try:
        server.stop()
    except Exception as e:
        print(f"Error stopping server: {e}")
