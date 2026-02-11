#!/usr/bin/env python3
"""Cross-compile MicroPython source files to .mpy format."""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


class Colors:
    """ANSI color codes for terminal output."""

    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"  # No Color


def find_mpy_cross() -> Path:
    """Find the mpy-cross executable."""
    # Check environment variable first
    if mpy_cross_env := os.environ.get("MPY_CROSS"):
        mpy_cross = Path(mpy_cross_env)
        if mpy_cross.exists():
            return mpy_cross

    # Check standard location in workspace
    workspace_mpy_cross = Path("../micropython/mpy-cross/build/mpy-cross")
    if workspace_mpy_cross.exists():
        return workspace_mpy_cross

    # Check if mpy-cross is in PATH
    try:
        result = subprocess.run(["which", "mpy-cross"], capture_output=True, text=True)
        if result.returncode == 0:
            return Path(result.stdout.strip())
    except Exception:
        pass

    return None


def get_files_from_manifest(manifest_path: Path) -> List[Tuple[str, str]]:
    """Extract file paths from the debugpy.json manifest.

    Returns list of tuples: (target_path, source_path)
    """
    try:
        with open(manifest_path, "r") as f:
            manifest = json.load(f)

        files = []
        for url_entry in manifest.get("urls", []):
            if len(url_entry) == 2:
                target_path, source_path = url_entry
                # Only include .py files (not the compiled .mpy)
                if target_path.endswith(".py"):
                    files.append((target_path, source_path))

        return files
    except Exception as e:
        print(f"{Colors.RED}Error reading manifest: {e}{Colors.NC}")
        return []


def compile_file(mpy_cross: Path, source_file: Path, output_file: Path) -> bool:
    """Compile a single Python file to .mpy format."""
    try:
        # Create output directory if it doesn't exist
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Run mpy-cross
        result = subprocess.run(
            [str(mpy_cross), "-o", str(output_file), str(source_file), "-O2"],
            capture_output=True,
            text=True,
        )

        return result.returncode == 0
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.NC}")
        return False


def main():
    """Main entry point."""
    print(f"{Colors.BLUE}MicroPython Cross-Compiler for debugpy{Colors.NC}")
    print("=" * 50)

    # Configuration (script is in launcher folder)
    script_dir = Path(__file__).parent
    output_dir = script_dir / "compiled"
    output_dir.mkdir(exist_ok=True)
    manifest_path = script_dir / "debugpy.json"

    # Find mpy-cross
    mpy_cross = find_mpy_cross()
    if not mpy_cross:
        print(f"{Colors.RED}Error: mpy-cross not found{Colors.NC}")
        print("Please build mpy-cross first:")
        print("  cd micropython/mpy-cross && make")
        print("\nOr install via: uv tool install mpy-cross")
        print("Or set MPY_CROSS environment variable")
        return 1

    print(f"Using mpy-cross: {mpy_cross}")

    # Check source directory
    if not (script_dir / "debugpy.json").exists():
        print(f"{Colors.RED}Error: Manifest not found in launcher directory{Colors.NC}")
        return 1

    # Check manifest
    if not manifest_path.exists():
        print(f"{Colors.RED}Error: Manifest not found: {manifest_path}{Colors.NC}")
        return 1

    # Get files from manifest
    files = get_files_from_manifest(manifest_path)
    if not files:
        print(f"{Colors.YELLOW}Warning: No files found in manifest{Colors.NC}")
        return 1

    print(f"Found {len(files)} files to compile\n")

    # Compile each file
    success_count = 0
    fail_count = 0
    results: List[Tuple[str, bool, str]] = []

    for target_path, source_path in files:
        # Resolve source path relative to manifest location
        source_file = (script_dir / source_path).resolve()
        # Output uses target path
        output_file = output_dir / target_path.replace(".py", ".mpy")

        print(f"Compiling {target_path}... ", end="", flush=True)

        if not source_file.exists():
            print(f"{Colors.YELLOW}SKIPPED (not found){Colors.NC}")
            results.append((target_path, False, "Source not found"))
            fail_count += 1
            continue

        success = compile_file(
            mpy_cross,
            source_file,
            output_file,
        )

        if success:
            print(f"{Colors.GREEN}OK{Colors.NC}")
            results.append((target_path, True, "Success"))
            success_count += 1
        else:
            print(f"{Colors.RED}FAILED{Colors.NC}")
            results.append((target_path, False, "Compilation failed"))
            fail_count += 1

    # Summary
    print("\n" + "=" * 50)
    print("Compilation complete:")
    print(f"  {Colors.GREEN}{success_count} succeeded{Colors.NC}")
    if fail_count > 0:
        print(f"  {Colors.RED}{fail_count} failed{Colors.NC}")

    if fail_count > 0:
        print(f"\n{Colors.YELLOW}Failed files:{Colors.NC}")
        for file, success, message in results:
            if not success:
                print(f"  - {file}: {message}")
        return 1

    print(f"\n{Colors.GREEN}All files compiled successfully!{Colors.NC}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
