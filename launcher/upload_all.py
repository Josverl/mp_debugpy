#!/usr/bin/env python3
"""
This script compiles the debugpy source files to .mpy format and installs the compiled files to the ESP32 device
using mpremote mip install.
It also uploads the source files to the device for debugging purposes.
"""

import subprocess
import sys
import compile_debugpy


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
    if compile_debugpy.main() != 0:
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

    return 0


if __name__ == "__main__":
    sys.exit(main())
