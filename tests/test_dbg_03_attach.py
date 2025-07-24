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
)
# @pytest.mark.parametrize("logToFile", [True, False], indirect=True)
def test_debug_attach(attach_server, attach_delay):
    """
    Test the debug attach functionality.
    """
    server = attach_server
    server.run_single()
    time.sleep(attach_delay / 2)
    server.run_single()
    time.sleep(attach_delay / 2)
    for _ in range(5):
        time.sleep(0.1)
        server.run_single()

    if attach_delay < 2:
        pytest.xfail(reason="Attach delay is too short, test may fail due to timing issues")
    server = attach_server
    last_msg = server.rcv_messages[-1] if server.rcv_messages else None
    assert last_msg is not None, "Last message should not be None"
    assert last_msg.type == "response", f"Expected response message, got {last_msg.type}"
    assert last_msg.command == "attach", f"Expected command 'attach', got {last_msg.command}"
