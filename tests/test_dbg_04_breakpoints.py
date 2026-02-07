import time
from typing import List

import pytest
from helpers import find_messages, set_breakpoints, wait_for_msg


@pytest.mark.parametrize(
    "tgt_src_folder, tgt_module, bp_lines",
    [
        ("", "basic", [20, 25]),
        ("", "target", [78, 89, 90]),
    ],
    indirect=True,
)
def test_debug_breakpoints(
    attach_server,
    tgt_src_folder: str,
    tgt_module: str,
    bp_lines: List,
    micropython_debuggee,
):
    """
    Test the debug breakpoints functionality.
    """
    server = attach_server
    source_file = f"{tgt_src_folder}/{tgt_module}.py"
    set_breakpoints(server, source_file, bp_lines)
    wait_for_msg(server, response="setBreakpoints")

    # Check that the debugee responds to the setBreakpoints request
    responses = find_messages(server, response="setBreakpoints")
    assert len(responses) == 1, f"Expected 1 setBreakpoints response, got {len(responses)}"

    # check which breakpoints have been set
    bp_response = responses[0]
    breakpoints_set = bp_response.body["breakpoints"]
    assert len(breakpoints_set) == len(bp_lines), f"Expected {len(bp_lines)} breakpoints, got {len(breakpoints_set)}"
    # check that each of the breakpoints is verified and in the correct source file
    for bp in breakpoints_set:
        assert bp["line"] in bp_lines, f"Unexpected breakpoint line: {bp['line']}"
        assert bp["verified"] is True, f"Breakpoint at line {bp['line']} should be verified"
        assert bp["source"]["path"] == source_file, f"Breakpoint at line {bp['line']} should be in {source_file}"

    wait_for_msg(server, event="stopped")
    stopped_events = find_messages(server, event="stopped")
    assert len(stopped_events) == 1, f"Expected 1 stopped event, got {len(stopped_events)}"
    assert stopped_events[0].body["reason"] == "breakpoint"

    # TODO: check which breakpoint is hit by requesting a stack trace

