"""Start the MicroPython debug server for VS Code debugging."""
import argparse
import sys
import time

import debugpy

# Set sys.path to include the scratch/launcher directory.
sys.path.insert(0, '.')
sys.path.insert(1, "micropython-lib/python-ecosys/debugpy")

_banner = r"""
 _____  _______ ______ _______ _______ ______ ___ ___
|     \|    ___|   __ \   |   |     __|   __ \   |   |
|  --  |    ___|   __ <   |   |    |  |    __/\     /
|_____/|_______|______/_______|_______|___|    |___|
"""


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Start the MicroPython debug server and load a module for attach.")
    # Named arguments
    parser.add_argument("--module", default="main", dest="module", help="Target module to debug")
    parser.add_argument("--method", default="main", dest="method", help="Target method to call")
    parser.add_argument("--port", default=5678, dest="port", type=int, help="Port for debugpy server")
    parser.add_argument(
        "--delay", type=int, default=2, help="Delay in seconds before calling target method (default: 2)"
    )

    args = parser.parse_args()

    return args.module, args.method, args.port, args.delay


def waitfor_debugger():
    print(_banner)
    print("MicroPython VS Code Debugging Test")
    print("==================================")

    target_module, target_method, port, delay = parse_arguments()

    print(f"Target module: {target_module}")
    print(f"Target method: {target_method}")
    print(f"Listening port: {port}")
    print(f"Delay before execution: {delay} seconds")
    print("==================================")
    # Start debug server
    try:
        debugpy.listen(host="0.0.0.0", port=int(port))
        print(f"Debug server attached on 0.0.0.0:{port}")
        print("Connecting back to VS Code debugger now...")

        _target = __import__(target_module, None, None, ("*"))
        _method = getattr(_target, target_method, None)
        if _method is None:
            raise ImportError(f"Method '{target_method}' not found in module '{target_module}'")

        # import target as target_main
        print("waiting at debugpy.breakpoint()")
        debugpy.breakpoint()
        debugpy.debug_this_thread()

        # Give VS Code a moment to set breakpoints after attach
        print(f"\nGiving VS Code {delay} seconds to set breakpoints...")
        time.sleep(delay)

        _method = getattr(_target, target_method, None)
        if _method is None:
            raise ImportError(f"Method '{target_method}' not found in module '{target_module}'")

        # Call the debuggable code function so it gets traced
        result = _method()

        print("Target completed successfully!")
        if result is None:
            print("No result returned from target.my_code()")
        else:
            print("Result type:", type(result))
            print("Result:", result)

    except KeyboardInterrupt:
        print("\nDebugging interrupted by user")
    except Exception as e:
        print(f"Error: {e}")


waitfor_debugger()
