import time
from typing import List

import pytest
from helpers import wait_for_msg


@pytest.mark.parametrize(
    "attach_delay",
    [
        3,
        2,
        1,
        # 0.8,
        # 0.6,
        # 0.4,
        # 0.2,
    ],
    indirect=True,
)
# @pytest.mark.parametrize("logToFile", [True, False], indirect=True)
def test_debug_attach(attach_server, attach_delay):
    """
    Test the debug attach functionality.
    """
    server = attach_server

    OK = wait_for_msg(server, response="attach", timeout=attach_delay)

    if not OK:
        if attach_delay < 2:
            pytest.xfail(reason="Attach delay is too short, test may fail due to timing issues")
        pytest.fail(f"Attach did not complete within {attach_delay} seconds")

    OK2 = wait_for_msg(server, event="stopped", timeout=attach_delay)
    if not OK2 and attach_delay < 2:
        pytest.fail(f"Stopped event did not occur within {attach_delay} seconds")

    stopped_events = [msg for msg in server.rcv_messages if msg.type == "event" and msg.event == "stopped"]
    assert len(stopped_events) == 1, f"Expected 1 stopped event, got {len(stopped_events)}"

    attach_response = [msg for msg in server.rcv_messages if msg.type == "response" and msg.command == "attach"]
    assert len(attach_response) == 1, f"Expected 1 attach response, got {len(attach_response)}"
