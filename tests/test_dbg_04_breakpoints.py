import time
from typing import List

import pytest


@pytest.mark.parametrize(
    "source_file, bp_lines",
    [
        ("/home/jos/mp_debugpy/src/target.py", [78, 89, 90]),
        ("./target.py", [78, 89, 90]),
        ("src/target.py", [78, 89, 90]),
    ],
    indirect=True,
)


def test_debug_breakpoints(
    set_breakpoints,
    source_file: str,
    bp_lines: List,
    micropython_debuggee,
):
    """
    Test the debug breakpoints functionality.
    """
    server, breakpoints = set_breakpoints

    # Check that the debugee responds to the setBreakpoints request
    responses = [msg for msg in server.rcv_messages if msg.type == "response" and msg.command == "setBreakpoints"]
    assert len(responses) == 1, f"Expected 1 setBreakpoints response, got {len(responses)}"
    bp_response = responses[0]
    assert bp_response.type == "response", f"Expected response message, got {bp_response.type}"
    assert bp_response.command == "setBreakpoints", f"Expected command 'setBreakpoints', got {bp_response.command}"

    breakpoints_set = bp_response.body["breakpoints"]
    assert len(breakpoints_set) == len(breakpoints), (
        f"Expected {len(breakpoints)} breakpoints, got {len(breakpoints_set)}"
    )
    # check that each of the breakpoints is verified and in the correct source file
    for bp in breakpoints_set:
        assert bp["line"] in bp_lines, f"Unexpected breakpoint line: {bp['line']}"
        assert bp["verified"] is True, f"Breakpoint at line {bp['line']} should be verified"
        assert bp["source"]["path"] == source_file, f"Breakpoint at line {bp['line']} should be in {source_file}"


@pytest.mark.parametrize(
    "source_file, bp_lines",
    [
        ("/home/jos/mp_debugpy/src/target.py", [78, 89, 90]),
    ],
    indirect=True,
)
def test_debug_breakpoints_duplicate(set_breakpoints, source_file: str, bp_lines: List):
    """
    Test what happens if we set the more breakpoints in the same file.
    This should not cause any issues, and the server should respond with the
    breakpoints that were set.
    Only the last breakpoints should be considered, as the previous ones
    should be overwritten.
    """
    server, breakpoints = set_breakpoints
    client = server.client
    bp_lines_2 = [10, 9, 8]  # New lines to set breakpoints on
    breakpoints_2 = [{"line": line} for line in bp_lines_2]
    client.set_breakpoints(
        source={"name": source_file, "path": source_file},
        breakpoints=breakpoints_2,
        # lines=bp_lines,   # Deprecated
        source_modified=False,
    )
    # make sure that we give the server some time to process the request
    for _ in range(5):
        time.sleep(0.01)
        server.run_single()

    # Check that the debugee responds to the setBreakpoints request
    responses = [msg for msg in server.rcv_messages if msg.type == "response" and msg.command == "setBreakpoints"]
    assert len(responses) == 2, f"Expected 2 setBreakpoints response, got {len(responses)}"
    bp_response = responses[-1]
    assert bp_response.type == "response", f"Expected response message, got {bp_response.type}"
    assert bp_response.command == "setBreakpoints", f"Expected command 'setBreakpoints', got {bp_response.command}"

    breakpoints_set = bp_response.body["breakpoints"]
    assert len(breakpoints_set) == len(breakpoints_2), (
        f"Expected {len(breakpoints_2)} breakpoints, got {len(breakpoints_set)}"
    )
    # check that each of the breakpoints is verified and in the correct source file
    for bp in breakpoints_set:
        assert bp["line"] in bp_lines_2, f"Unexpected breakpoint line: {bp['line']}"
        assert bp["verified"] is True, f"Breakpoint at line {bp['line']} should be verified"
        assert bp["source"]["path"] == source_file, f"Breakpoint at line {bp['line']} should be in {source_file}"
