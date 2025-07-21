import time

import pytest


@pytest.mark.parametrize("delay", [1, 0.8, 0.6, 0.4, 0.2])
@pytest.mark.parametrize("logToFile", [True, False])
def test_debug_attach(fake_vscode_server, free_tcp_port, delay: int, logToFile: bool):
    """
    Test the debug attach functionality.
    """
    server = fake_vscode_server
    assert server is not None, "Server should not be None"

    # Setup the server for testing
    # Ensure clean state at start of test
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
    # print("attach + run_single()")
    # client.set_breakpoints(
    #     source={"name": "target.py", "path": "/home/jos/mp_debugpy/src/target.py"},
    #     breakpoints=[{"line": 78}, {"line": 89}, {"line": 90}],
    #     lines=[78, 89, 90],
    #     source_modified=False,
    # )
    server.run_single()
    time.sleep(delay / 2)
    server.run_single()
    time.sleep(delay / 2)
    for _ in range(5):
        time.sleep(0.01)
        server.run_single()

    last_msg = server.rcv_messages[-1] if server.rcv_messages else None
    assert last_msg is not None, "Last message should not be None"
    assert last_msg.type == "response", f"Expected response message, got {last_msg.type}"
    assert last_msg.command == "attach", f"Expected command 'attach', got {last_msg.command}"
