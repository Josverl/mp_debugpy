"""
Direct test of pdb_adapter.set_variable method using frame.set_local.
This tests the implementation without going through the full DAP protocol.
"""

import sys
import os

# Add the debugpy module to the path
sys.path.insert(0, "./micropython-lib/python-ecosys/debugpy")

from debugpy.server.pdb_adapter import PdbAdapter

# Constants from pdb_adapter.py
VARREF_LOCALS = 1
VARREF_GLOBALS = 2

# Global variables for testing
test_global = "original_global"
test_global_num = 42


def test_set_variable():
    """Test the set_variable method directly."""

    def target_function():
        # Local variables for testing
        test_local = "original_local"
        test_local_num = 100

        print(f"Before modification:")
        print(f"  Global: test_global = {test_global}")
        print(f"  Global: test_global_num = {test_global_num}")
        print(f"  Local: test_local = {test_local}")
        print(f"  Local: test_local_num = {test_local_num}")

        # Get current frame
        frame = sys._getframe()

        # Create a simple PdbAdapter instance
        class MockDebugSession:
            def send_event(self, event_type, **kwargs):
                pass

            def send_response(self, request, **kwargs):
                pass

        adapter = PdbAdapter()
        adapter.debug_session = MockDebugSession()  # Set the debug session

        # Set up frame context for the adapter
        adapter.current_frame = frame

        try:
            print("\nTesting global variable modification:")

            # Test setting global variables (frame_id=0, scope_type=VARREF_GLOBALS)
            globals_ref = 0 * 1000 + VARREF_GLOBALS  # 2
            result = adapter.set_variable(globals_ref, "test_global", "'modified_global'")
            print(f"  Set test_global result: {result}")
            print(f"  New value: test_global = {test_global}")

            result = adapter.set_variable(globals_ref, "test_global_num", "999")
            print(f"  Set test_global_num result: {result}")
            print(f"  New value: test_global_num = {test_global_num}")

            print("\nTesting local variable modification:")

            # Test setting local variables (frame_id=0, scope_type=VARREF_LOCALS)
            locals_ref = 0 * 1000 + VARREF_LOCALS  # 1
            result = adapter.set_variable(locals_ref, "test_local", "'modified_local'")
            print(f"  Set test_local result: {result}")
            print(f"  New value: test_local = {test_local}")

            result = adapter.set_variable(locals_ref, "test_local_num", "888")
            print(f"  Set test_local_num result: {result}")
            print(f"  New value: test_local_num = {test_local_num}")

            print("\nFinal values:")
            print(f"  Global: test_global = {test_global}")
            print(f"  Global: test_global_num = {test_global_num}")
            print(f"  Local: test_local = {test_local}")
            print(f"  Local: test_local_num = {test_local_num}")

            # Verify that frame._set_local method exists
            if hasattr(frame, "_set_local"):
                print(f"\n✓ frame._set_local method is available")
            else:
                print(f"\n✗ frame._set_local method is NOT available")

            return True

        except Exception as e:
            print(f"\nError during test: {e}")
            import traceback

            traceback.print_exc()
            return False

    return target_function()


if __name__ == "__main__":
    print("Testing pdb_adapter.set_variable with frame._set_local")
    print("=" * 60)

    success = test_set_variable()

    if success:
        print("\n✓ Test completed successfully!")
    else:
        print("\n✗ Test failed!")
