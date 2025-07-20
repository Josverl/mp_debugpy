import pytest


def test_debug_launcher_default_params(micropython_debuggee, tgt_module):
    """
    Test with default parameters.
    """
    process, port = micropython_debuggee

    assert process is not None, "Process should not be None"
    assert tgt_module == "target", f"Expected default module 'target', got {tgt_module}"
    print(
        f"Debugpy process started with PID: {process.pid} on port {port} for module {tgt_module}"
    )


@pytest.mark.parametrize("tgt_module", ["foobar"], indirect=True)
def test_debug_launcher_custom_params(micropython_debuggee, tgt_module):
    """
    Test with custom parameters for module and port.
    """
    process, port = micropython_debuggee

    assert process is not None, "Process should not be None"
    assert isinstance(port, int), f"Expected port to be an integer, got {port}"
    assert tgt_module == "foobar", f"Expected module 'foobar', got {tgt_module}"
    print(
        f"Debugpy process started with PID: {process.pid} on port {port} for module {tgt_module}"
    )
