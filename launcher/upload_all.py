#!/usr/bin/env python3
"""Upload source files and debugpy to ESP32 device."""

import subprocess
import sys
import do_mpy_cross


def run_command(cmd: list[str] | str, use_shell: bool = False) -> int:
    """Run a command and return the exit code."""
    if use_shell:
        print(f"Running: {cmd}")
    else:
        print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, shell=use_shell)
    return result.returncode


def main():
    """Upload debugpy and source files to ESP32."""
    # TODO: Only compile and upload files that have changed since last upload
    if do_mpy_cross.main() != 0:
        print("Error: Failed to compile files", file=sys.stderr)
        return 1

    # Install debugpy using mip
    package_path = "launcher/debugpy_mpy.json"
    if run_command(["mpremote", "mip", "install", package_path]) != 0:
        print("Error: Failed to install debugpy", file=sys.stderr)
        return 1

    # Copy the src directory to the root of the ESP32 filesystem
    if run_command("mpremote cp -r src/ :/", use_shell=True) != 0:
        print("Error: Failed to copy source files", file=sys.stderr)
        return 1

    # Start the debugpy server on the ESP32
    if run_command(["mpremote", "run", "launcher/start_debugpy_esp32.py"]) != 0:
        print("Error: Failed to start debugpy server", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
