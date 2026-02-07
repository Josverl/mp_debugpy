import fcntl
import os
import random
import socket
import subprocess
import time
from pathlib import Path

import pytest

random.seed()


@pytest.fixture()
def free_tcp_port(request):
    """
    Fixture to find a free TCP port on localhost starting from 5678 and increasing upward.
    Can be parameterized to use a specific port.
    """
    if hasattr(request, "param"):
        # Use parameterized port
        requested_port = request.param
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("localhost", requested_port))
                return requested_port
            except OSError:
                pytest.fail(f"Requested port {requested_port} is not available")

    # Default behavior - find free port
    min_port = 5678
    max_port = 8000
    base_port = min_port + random.randint(0, max_port - min_port)

    for port in range(base_port, max_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("localhost", port))
                return port
            except OSError:
                continue

    pytest.fail("Could not find a free TCP port in the range 5678-5999")


@pytest.fixture()
def micropython_debuggee(
    pytestconfig,
    tgt_src_folder: str,
    tgt_module: str,
    tgt_method: str,
    free_tcp_port: int,
    in_terminal: bool,
):
    """
    Fixture to start the debugpy executable in a separate process.
    can be parameterized with:
    - tgt_module: The target module to run.
    - tgt_method: The target method to run.
    - free_tcp_port: The port to bind the server to.
    """
    # Get the workspace root path using pytest configuration
    root_path = Path(pytestconfig.rootpath)

    # Construct absolute paths
    micropython_path = root_path / "firmware/unix_settrace_save_names/micropython"
    launcher_path = root_path / "launcher/start_debugpy.py"
    micropython_lib_path = root_path / "micropython-lib/python-ecosys/debugpy"
    src_path = root_path / tgt_src_folder

    # Ensure the paths exist
    if not micropython_path.exists():
        pytest.fail(f"MicroPython path does not exist: {micropython_path}")
    if not launcher_path.exists():
        pytest.fail(f"Launcher path does not exist: {launcher_path}")
    if not micropython_lib_path.exists():
        pytest.fail(f"MicroPython library path does not exist: {micropython_lib_path}")
    if not src_path.exists():
        pytest.fail(f"Source path does not exist: {src_path}")

    # Set up the environment
    env = os.environ.copy()
    env["MICROPYPATH"] = f"{src_path}:{micropython_lib_path}:~/.micropython/lib:/usr/lib/micropython"

    # Command to start the MicroPython process
    command = [
        str(micropython_path),
        str(launcher_path),
        "--module",
        tgt_module,
        "--method",
        tgt_method,
        "--port",
        str(free_tcp_port),
    ]

    if in_terminal:
        # Make the subprocess visible in a new terminal window
        terminal_command = [
            "x-terminal-emulator",
            "-e",
            " ".join(command),
        ]

        # Start the process in a new terminal
        process = subprocess.Popen(
            terminal_command,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # time.sleep(1)  # Give the terminal some time to open

    else:
        # cmd = " ".join(command)
        print(f"Running command: {command} / {' '.join(command)}")
        process = subprocess.Popen(
            command,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Set stdout and stderr to non-blocking mode
        if process.stdout:
            fcntl.fcntl(
                process.stdout.fileno(),
                fcntl.F_SETFL,
                fcntl.fcntl(process.stdout.fileno(), fcntl.F_GETFL) | os.O_NONBLOCK,
            )
        if process.stderr:
            fcntl.fcntl(
                process.stderr.fileno(),
                fcntl.F_SETFL,
                fcntl.fcntl(process.stderr.fileno(), fcntl.F_GETFL) | os.O_NONBLOCK,
            )

        # ======================================
        stdout_data = ""
        stderr_data = ""
        max_retries = 10

        # Verify all expected output lines are present
        expected_lines = [
            # "MicroPython VS Code Debugging Test",
            "==================================",
            f"Target module: {tgt_module}",
            f"Target method: {tgt_method}",
            "==================================",
            f"Debugpy listening on 0.0.0.0:{free_tcp_port}",
        ]

        for attempt in range(max_retries):
            print(f"Attempt {attempt + 1}/{max_retries} to read process output...")

            # Non-blocking read from stdout
            try:
                if process.stdout:
                    chunk = process.stdout.read(1024)
                    if chunk:
                        stdout_data += chunk
            except (BlockingIOError, OSError):
                pass  # No data available
            except Exception as e:
                print(f"Error reading stdout: {e}")

            # Non-blocking read from stderr
            try:
                if process.stderr:
                    chunk = process.stderr.read(1024)
                    if chunk:
                        stderr_data += chunk
            except (BlockingIOError, OSError):
                pass  # No data available
            except Exception as e:
                print(f"Error reading stderr: {e}")

            # Check if process has terminated
            if process.poll() is not None:
                print(f"Process terminated with exit code: {process.returncode}")
                break

            # Check if we have all expected lines
            if all(line.strip() in stdout_data for line in expected_lines):
                break

            time.sleep(0.1)

        # Check for errors in stderr
        if stderr_data.strip():
            pytest.fail(f"Process stderr contains errors: {stderr_data}")

        print("stdout_data:", stdout_data)

        for line in expected_lines:
            assert line in stdout_data, f"Expected line '{line}' not found in stdout. Got: {stdout_data}"

    # ======================================

    yield process

    # Terminate the process after the test if it's still running
    try:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=1)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=1)
    finally:
        # Ensure terminal process is terminated if started
        if in_terminal and process.poll() is None:
            process.kill()
            process.wait(timeout=1)
            process.terminate()
