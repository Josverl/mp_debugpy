import pytest


def test_debug_launcher_default_params(micropython_debuggee, tgt_module, free_tcp_port):
    """
    Test with default parameters.
    """
    process = micropython_debuggee

    assert process is not None, "Process should not be None"
    assert tgt_module == "basic", f"Expected default module 'basic', got {tgt_module}"
    print(f"Debugpy process started with PID: {process.pid} on port {free_tcp_port} for module {tgt_module}")


@pytest.mark.parametrize(
    "tgt_src_folder, tgt_module",
    [
        ("", "foobar"),
        ("", "basic"),
        ("tests/data/performance", "run_pystone"),
    ],
    indirect=True,
)
def test_debug_launcher_custom_params(micropython_debuggee, tgt_module, free_tcp_port):
    """
    Test with custom parameters for module and port.
    """
    process = micropython_debuggee

    assert process is not None, "Process should not be None"
    assert process.pid > 0, "Process PID should be greater than 0"
    assert isinstance(free_tcp_port, int), f"Expected port to be an integer, got {free_tcp_port}"
    print(f"Debugpy process started with PID: {process.pid} on port {free_tcp_port} for module {tgt_module}")
