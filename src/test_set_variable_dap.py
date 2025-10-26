#!/usr/bin/env micropython
"""
Test script for DAP setVariable functionality.
This tests both global and local variable modification via the DAP protocol.
"""

import sys

# Global variable for testing
global_var = "initial_global_value"

def test_local_variables():
    """Test function with local variables to modify via DAP."""
    local_var1 = "initial_local_value1"
    local_var2 = 42
    local_var3 = [1, 2, 3]
    
    print(f"Before modification:")
    print(f"  local_var1 = {local_var1}")
    print(f"  local_var2 = {local_var2}")
    print(f"  local_var3 = {local_var3}")
    print(f"  global_var = {global_var}")
    
    # This is where we would set a breakpoint in DAP
    # and test the setVariable requests
    print("\n[BREAKPOINT] Set breakpoint here to test DAP setVariable")
    print("Test these DAP setVariable commands:")
    print("1. Set local_var1 to 'modified_by_dap'")
    print("2. Set local_var2 to 999")
    print("3. Set local_var3 to [4, 5, 6]")
    print("4. Set global_var to 'modified_global'")
    
    # Manual test using sys._set_local_var
    if hasattr(sys, '_set_local_var'):
        print("\n[MANUAL TEST] Testing sys._set_local_var directly:")
        frame = sys._getframe()
        
        try:
            sys._set_local_var(frame, "local_var1", "manually_modified")
            sys._set_local_var(frame, "local_var2", 777)
            print("Manual modification successful!")
        except Exception as e:
            print(f"Manual modification failed: {e}")
    
    print(f"\nAfter manual modification:")
    print(f"  local_var1 = {local_var1}")
    print(f"  local_var2 = {local_var2}")
    print(f"  local_var3 = {local_var3}")
    print(f"  global_var = {global_var}")

def test_nested_function():
    """Test nested function to ensure frame handling works correctly."""
    outer_var = "outer_value"
    
    def inner_function():
        inner_var = "inner_value"
        print(f"\n[NESTED] Inner function variables:")
        print(f"  inner_var = {inner_var}")
        print(f"  outer_var = {outer_var}")
        print(f"  global_var = {global_var}")
        
        # Another breakpoint location for testing
        print("[BREAKPOINT] Test setVariable in nested function")
        
        return inner_var
    
    result = inner_function()
    print(f"\nOuter function after inner call:")
    print(f"  outer_var = {outer_var}")
    print(f"  result = {result}")

def main():
    """Main test function."""
    print("=== DAP setVariable Test Script ===")
    print("This script tests the Debug Adapter Protocol setVariable functionality.")
    print("Set breakpoints at the marked locations and test variable modification.")
    
    # Test basic local variable modification
    test_local_variables()
    
    # Test nested function variable modification
    test_nested_function()
    
    print("\n=== Test Complete ===")
    print("Global variable final value:", global_var)

if __name__ == "__main__":
    main()
