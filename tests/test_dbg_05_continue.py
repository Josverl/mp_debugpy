import time
from concurrent.futures import thread
from typing import TYPE_CHECKING, List

import pytest
from helpers import PerfServer, find_messages, set_breakpoints, wait_for_msg


@pytest.mark.parametrize(
    "in_terminal, logToFile",
    [
        (True, True),
    ],
    indirect=True,
)
@pytest.mark.parametrize(
    "tgt_src_folder, tgt_module, bp_lines",
    [
        ("", "basic", [20, 25]),
        ("", "target", [78, 89, 90]),
    ],
    indirect=True,
)
def test_debug_continue(
    attach_server,
    tgt_src_folder: str,
    tgt_module: str,
    bp_lines: List,
    micropython_debuggee,
):
    """
    Test the debug continue functionality,
    and stoping at the next breakpoint
    """
    server: PerfServer
    server = attach_server

    # Set breakpoints in the debug server
    source_file = f"{tgt_src_folder}/{tgt_module}.py"
    set_breakpoints(server, source_file, bp_lines)
    wait_for_msg(server, response="setBreakpoints")

    # Check that the debugee responds to the setBreakpoints request
    responses = find_messages(server, response="setBreakpoints")
    assert len(responses) == 1, f"Expected 1 setBreakpoints response, got {len(responses)}"

    # now we can continue the debugee
    client = server.client
    client.continue_(thread_id=1)  # Assuming threadId=1 is the main thread # TODO: Check this
    # server.clear_messages()
    # and wait for the next breakpoint to be hit
    bp_hit = wait_for_msg(server, event="stopped")

    # check for continue response
    responses = find_messages(server, response="continue")
    assert len(responses) == 1, f"Expected 1 continue response, got {len(responses)}"
    stopped_events = find_messages(server, event="stopped")
    assert len(stopped_events) == 2, f"Expected 2 stopped events, got {len(stopped_events)}"
    assert stopped_events[0].body["reason"] == "breakpoint", (
        f"Expected breakpoint hit, got {stopped_events[0].body['reason']}"
    )
    assert stopped_events[1].body["reason"] == "breakpoint", (
        f"Expected breakpoint hit, got {stopped_events[1].body['reason']}"
    )
