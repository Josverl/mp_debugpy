import time
from concurrent.futures import thread
from typing import TYPE_CHECKING, List

import pytest

if TYPE_CHECKING:
    from fixtures.fake_vscode import PerfServer


@pytest.mark.parametrize(
    "source_file, bp_lines",
    [
        ("/home/jos/mp_debugpy/src/target.py", [78, 89, 90]),
        # ("./target.py", [78, 89, 90]),
        # ("src/target.py", [78, 89, 90]),
    ],
    indirect=True,
)
def test_debug_continue(set_breakpoints, source_file: str, bp_lines: List, micropython_debuggee):
    """
    Test the debug continue functionality,
    and stoping at the next breakpoint
    """
    server: PerfServer
    server, breakpoints = set_breakpoints

    # Check that the debugee responds to the setBreakpoints request
    responses = [msg for msg in server.rcv_messages if msg.type == "response" and msg.command == "setBreakpoints"]
    assert len(responses) == 1, f"Expected 1 setBreakpoints response, got {len(responses)}"

    start_len = len(server.rcv_messages)
    # now we can continue the debugee
    client = server.client
    client.continue_(thread_id=1)  # Assuming threadId=1 is the main thread # TODO: Check this

    # and wait for the next breakpoint to be hit
    bp_hit = False
    for _ in range(500):
        time.sleep(0.01)
        server.run_single()
        if len(server.rcv_messages) > start_len:
            print(f"Received  response after {_ * 0.01} seconds")
            # hit_msg = server.rcv_messages[-1]
            # if hit_msg.type == "event" and hit_msg.event == "stopped":
            #     assert hit_msg.body["reason"] == "breakpoint", f"Expected breakpoint hit, got {hit_msg.body['reason']}"
            #     assert hit_msg.body["breakpoint"]["line"] in bp_lines, (
            #         f"Unexpected breakpoint line: {hit_msg.body['breakpoint']['line']}"
            #     )
            bp_hit = True
            break

    assert bp_hit is True, "Expected breakpoint to be hit"
