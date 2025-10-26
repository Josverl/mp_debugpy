import time
from pathlib import Path
from pickle import TRUE
from typing import Dict, List

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


def wait_for_msg(server, *, count=0, event="", response="", timeout=5):
    """Wait for a specific message, or number of messages, to be received."""
    t1 = time.time()
    server.run_single()
    while not server.rcv_messages and time.time() - t1 < timeout:
        time.sleep(0.1)
        server.run_single()
    if count > 0:
        while time.time() - t1 < timeout and len(server.rcv_messages) < count:
            time.sleep(0.1)
            server.run_single()
    elif event:
        while time.time() - t1 < timeout and not (
            server.rcv_messages[-1].type == "event" and server.rcv_messages[-1].event == event
        ):
            time.sleep(0.1)
            server.run_single()
    elif response:
        while time.time() - t1 < timeout and not (
            server.rcv_messages[-1].type == "response" and server.rcv_messages[-1].command == response
        ):
            time.sleep(0.1)
            server.run_single()
    return len(server.rcv_messages) >= count


def set_breakpoints(
    server: PerfServer,
    source_file: str,
    bp_lines: List[int],
    wait=False,
):
    """Set breakpoints in the debug server.
    This fixture uses the attach_server fixture to set
    breakpoints in the debug server.
    It can be parameterized with:
    - source_file: The source file to set breakpoints in.
    - bp_lines: The lines to set breakpoints on.
    """
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

    # Wait for the setBreakpoints response
    if not wait:
        return True
    return wait_for_msg(server, response="setBreakpoints")
