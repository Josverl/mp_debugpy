#!/usr/bin/env python3
"""
Test script for DAP setVariable integration with our C-level local variable modification.
"""

import sys

# Test our implementation
def test_setvariable_integration():
    print("Testing setVariable integration...")
    
    # Test 1: Check if our C function is available
    print(f"1. sys._set_local_var available: {hasattr(sys, '_set_local_var')}")
    
    # Test 2: Test local variable modification
    def test_function():
        local_var = "original_value"
        another_var = 42
        
        print(f"   Before: local_var={local_var}, another_var={another_var}")
        
        # Get current frame
        frame = sys._getframe()
        
        # Test modifying string variable
        sys._set_local_var(frame, "local_var", "modified_value")
        
        # Test modifying integer variable
        sys._set_local_var(frame, "another_var", 999)
        
        print(f"   After: local_var={local_var}, another_var={another_var}")
        print(f"   f_locals: {frame.f_locals}")
        
        return local_var == "modified_value" and another_var == 999
    
    print("2. Testing local variable modification:")
    success = test_function()
    print(f"   Result: {'SUCCESS' if success else 'FAILED'}")
    
    # Test 3: Test with global variables
    global_var = "global_original"
    print(f"3. Testing global variable modification:")
    print(f"   Before: global_var={global_var}")
    
    # Modify global
    globals()['global_var'] = "global_modified"
    print(f"   After: global_var={global_var}")
    
    # Test 4: Test error handling
    print("4. Testing error handling:")
    try:
        frame = sys._getframe()
        sys._set_local_var(frame, "nonexistent_var", "value")
        print("   ERROR: Should have raised exception for nonexistent variable")
    except Exception as e:
        print(f"   SUCCESS: Correctly caught error: {e}")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    test_setvariable_integration()
