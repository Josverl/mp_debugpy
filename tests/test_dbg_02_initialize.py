import time

import pytest


def test_debug_initialize(fake_vscode_server, tgt_module):
    """
    Test with default parameters.
    """
    server = fake_vscode_server
    assert server is not None, "Server should not be None"

    # Ensure clean state at start of test
    server.clear_messages()

    print("start()")
    server.start()
    # process the initial DAP messages
    for _ in range(5):
        time.sleep(0.01)
        server.run_single()

    client = server.client
    assert server is not None, "Server should not be None"
    assert server.running == True, "Server should be running"  # noqa: E712
    assert client is not None, "Client should not be None"

    # should have 3 messages
    assert len(server.rcv_messages) == 3, f"Expected 3 messages, got {len(server.rcv_messages)}"

    # check initialize response
    init_response = [msg for msg in server.rcv_messages if msg.type == "response" and msg.command == "initialize"]
    assert len(init_response) == 1, f"Expected 1 initialize response, got {len(init_response)}"
    # check reported capabilities
    # todo : add more checks
    assert init_response[0].body["supportsSetVariable"]

    # check event : stopped
    stopped_events = [msg for msg in server.rcv_messages if msg.type == "event" and msg.event == "stopped"]
    assert len(stopped_events) == 1, f"Expected 1 stopped event, got {len(stopped_events)}"
    assert stopped_events[0].body["reason"] == "breakpoint", (
        f"Expected reason 'breakpoint', got {stopped_events[0].body['reason']}"
    )


@pytest.mark.parametrize(
    "tgt_module, tgt_method",
    [
        ("notexistent", "main"),
        ("target", "not_a_method"),
    ],
    indirect=True,
)
def test_debug_initialize_non_existent(fake_vscode_server, tgt_module, tgt_method):
    """
    Attempt to debug a non-existent module.
    """
    server = fake_vscode_server
    assert server is not None, "Server should not be None"

    # Ensure clean state at start of test
    server.clear_messages()

    print("start()")
    server.start()
    # process the initial DAP messages
    for _ in range(5):
        time.sleep(0.01)
        server.run_single()

    client = server.client
    assert server is not None, "Server should not be None"
    assert server.running == True, "Server should be running"  # noqa: E712
    assert client is not None, "Client should not be None"

    # check initialize response
    init_response = [msg for msg in server.rcv_messages if msg.type == "response" and msg.command == "initialize"]
    assert len(init_response) == 1, f"Expected 1 initialize response, got {len(init_response)}"
    # check reported capabilities
    # todo : add more checks
    assert init_response[0].body["supportsSetVariable"]

    # check event : stopped
    stopped_events = [msg for msg in server.rcv_messages if msg.type == "event" and msg.event == "stopped"]
    assert len(stopped_events) == 0, f"Expected 0 stopped events, got {len(stopped_events)}"

    # should have only 2 messages
    assert len(server.rcv_messages) == 2, f"Expected 2 messages, got {len(server.rcv_messages)}"



