"""Start the MicroPython debug server for VS Code debugging."""

import sys

# Set sys.path to include the scratch/launcher directory.
sys.path.insert(0, '.')
sys.path.insert(1, 'micropython-lib/python-ecosys/debugpy')
import debugpy


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

    # Start debug server
    try:
        debugpy.listen()
        print("Debug server attached on 127.0.0.1:5678")
        print("Connecting back to VS Code debugger now...")
        import target as target_main
        debugpy.breakpoint()

        debugpy.debug_this_thread()

        # Give VS Code a moment to set breakpoints after attach
        print("\nGiving VS Code time to set breakpoints...")
        import time
        time.sleep(2)

        # Call the debuggable code function so it gets traced
        result = target_main.main()

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
