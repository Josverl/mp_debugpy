"""Start the MicroPython debug server for VS Code debugging."""


import sys

import network

try:
    sys.gettrace()  # Ensure sys.settrace is available
except AttributeError:
    print("sys.settrace is not available. You need a firmware compiled with debugging features.")
    sys.exit(1)

try:
    import debugpy
except ImportError:
    print("debugpy module not found. Make sure to install")
    sys.exit(1)

wlan = network.WLAN()

_banner = r"""
 _____  _______ ______ _______ _______ ______ ___ ___ 
|     \|    ___|   __ \   |   |     __|   __ \   |   |
|  --  |    ___|   __ <   |   |    |  |    __/\     / 
|_____/|_______|______/_______|_______|___|    |___|  
"""
def waitfor_debugger():
    print(_banner)
    print("MicroPython VS Code Debugging Test")
    print("==================================")
    nargs = len(sys.argv) - 1
    target_module = "target"
    target_method = "main"
    if nargs > 0:
        target_module = sys.argv[1]
        if nargs > 1:
            target_method = sys.argv[2]
            if nargs > 2:
                raise ValueError("Too many arguments provided. Usage: start_debugpy.py [target_module] [target_method]")
    print(f"Target module: {target_module}")
    print(f"Target method: {target_method}")
    try:
        print(f"mdns         : {wlan.config('dhcp_hostname')}.local")
    except Exception as e:
        print(f"ip           : {wlan.ipconfig('addr4')[0]}")
    print("==================================")
    # Start debug server
    try:
        ipv4 = wlan.ipconfig('addr4')[0]

        debugpy.listen(host=ipv4, port=5678)
        print("Debug server attached on 127.0.0.1:5678")
        print("Connecting back to VS Code debugger now...")

        # import target as _target
        _target = __import__(target_module, None, None, ("*"))

        debugpy.breakpoint()

        debugpy.debug_this_thread()

        # Give VS Code a moment to set breakpoints after attach
        print("\nGiving VS Code time to set breakpoints...")
        import time
        time.sleep(2)

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
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"Error: {e}")



waitfor_debugger()
