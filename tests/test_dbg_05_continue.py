import time
from concurrent.futures import thread
from typing import TYPE_CHECKING, List

import pytest
from helpers import PerfServer, set_breakpoints, wait_for_msg


# TODO: run a micropython module from the test scripts folder.
@pytest.mark.parametrize(
    "source_file, bp_lines",
    [
        ("/home/jos/mp_debugpy/src/target.py", [78, 89, 90]),
    ],
    indirect=True,
)
def test_debug_continue(attach_server, source_file: str, bp_lines: List, micropython_debuggee):
    """
    Test the debug continue functionality,
    and stoping at the next breakpoint
    """
    server: PerfServer
    server = attach_server

    # Set breakpoints in the debug server
    set_breakpoints(server, source_file, bp_lines)
    wait_for_msg(server, response="setBreakpoints")

    # Check that the debugee responds to the setBreakpoints request
    responses = [msg for msg in server.rcv_messages if msg.type == "response" and msg.command == "setBreakpoints"]
    assert len(responses) == 1, f"Expected 1 setBreakpoints response, got {len(responses)}"

    # now we can continue the debugee
    client = server.client
    client.continue_(thread_id=1)  # Assuming threadId=1 is the main thread # TODO: Check this
    server.clear_messages()
    # and wait for the next breakpoint to be hit
    bp_hit = wait_for_msg(server, event="stopped")

    # check for continue response
    responses = [msg for msg in server.rcv_messages if msg.type == "response" and msg.command == "continue"]  # type: ignore
    assert len(responses) == 1, f"Expected 1 continue response, got {len(responses)}"

    assert bp_hit is True, "Expected breakpoint to be hit"
    hit_msg = server.rcv_messages[-1]
    assert hit_msg.body["reason"] == "breakpoint", f"Expected breakpoint hit, got {hit_msg.body['reason']}"  # type: ignore
