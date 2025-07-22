import time
from typing import Dict, List

import pytest
from anyio import Path
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

# simple fixtures to provide defaults
@pytest.fixture
def attach_delay(request):
    # attach
    if hasattr(request, "param"):
        yield request.param
    else:
        # Default value if not parameterized
        yield 2

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


@pytest.fixture
def attach_server(fake_vscode_server, free_tcp_port, logToFile: bool, attach_delay: int):
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
                    "localRoot": "/home/jos/mp_debugpy",
                    "remoteRoot": ".",
                }
            ],
            "workspaceFolder": "/home/jos/mp_debugpy",
            "justMyCode": True,
            "logToFile": logToFile,
            "__configurationTarget": 6,
            "clientOS": "unix",
            "debugOptions": ["RedirectOutput", "ShowReturnValue"],
            "showReturnValue": True,
            "__sessionId": "11976c7b-f770-484d-a445-115e82e3abcb",
        },
    )
    server.run_single()
    time.sleep(attach_delay / 2)
    server.run_single()
    time.sleep(attach_delay / 2)
    for _ in range(5):
        time.sleep(0.1)
        server.run_single()

    yield server


@pytest.fixture
def set_breakpoints(attach_server, source_file: str, bp_lines: List):
    """Fixture to set breakpoints in the debug server.
    This fixture uses the attach_server fixture to set
    breakpoints in the debug server.
    It can be parameterized with:
    - source_file: The source file to set breakpoints in.
    - bp_lines: The lines to set breakpoints on.
    """
    server: PerfServer
    server = attach_server
    assert server is not None, "Server should not be None"
    assert server.running, "Server should be running"
    client = server.client

    #     interface SetBreakpointsArguments {
    #   /**
    #    * The source location of the breakpoints; either `source.path` or
    #    * `source.sourceReference` must be specified.
    #    */
    #   source: Source;

    #   /**
    #    * The code locations of the breakpoints.
    #    */
    #   breakpoints?: SourceBreakpoint[];

    #   /**
    #    * Deprecated: The code locations of the breakpoints.
    #    */
    #   lines?: number[];

    #   /**
    #    * A value of true indicates that the underlying source has been modified
    #    * which results in new breakpoint locations.
    #    */
    #   sourceModified?: boolean;
    # }

    # {
    #   "source": {
    #     "name": "target.py",
    #     "path": "/home/jos/mp_debugpy/src/target.py"
    #   },
    #   "lines": [
    #     79,
    #     81,
    #     86
    #   ],
    #   "breakpoints": [
    #     {
    #       "line": 79
    #     },
    #     {
    #       "line": 81
    #     },
    #     {
    #       "line": 86
    #     }
    #   ],
    #   "sourceModified": false
    # }

    breakpoints = [{"line": line} for line in bp_lines]
    client.set_breakpoints(
        source={"name": Path(source_file).name, "path": source_file},
        breakpoints=breakpoints,
        # lines=bp_lines,   # Deprecated
        source_modified=False,
    )
    # make sure that we give the server some time to process the request
    for _ in range(5):
        time.sleep(0.01)
        server.run_single()
    yield server, breakpoints
