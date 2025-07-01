"""
Final verification test for DAP setVariable implementation
"""

def test_setvariable_complete():
    """Comprehensive test for setVariable functionality"""
    
    # Test data
    local_string = "original_string"
    local_number = 123
    local_list = [1, 2, 3]
    local_dict = {"key": "value"}
    
    # Global test data
    global test_global
    test_global = "original_global"
    
    print("=== DAP setVariable Test ===")
    print(f"Local variables before:")
    print(f"  local_string: {local_string}")
    print(f"  local_number: {local_number}")
    print(f"  local_list: {local_list}")
    print(f"  local_dict: {local_dict}")
    print(f"  test_global: {test_global}")
    
    # Manual test using our C function
    import sys
    frame = sys._getframe()
    
    print(f"\nTesting sys._set_local_var directly:")
    
    # Test 1: Modify string
    sys._set_local_var(frame, "local_string", "modified_string")
    print(f"  After modifying local_string: {local_string}")
    
    # Test 2: Modify number
    sys._set_local_var(frame, "local_number", 999)
    print(f"  After modifying local_number: {local_number}")
    
    # Test 3: Modify list
    sys._set_local_var(frame, "local_list", [7, 8, 9])
    print(f"  After modifying local_list: {local_list}")
    
    # Test 4: Modify dict
    sys._set_local_var(frame, "local_dict", {"new_key": "new_value"})
    print(f"  After modifying local_dict: {local_dict}")
    
    # Test 5: Test error handling
    try:
        sys._set_local_var(frame, "nonexistent_var", "value")
        print("  ERROR: Should have thrown exception")
    except Exception as e:
        print(f"  Error handling works: {e}")
    
    # Test 6: Global modification (traditional way)
    globals()['test_global'] = "modified_global"
    print(f"  After modifying global: {test_global}")
    
    print(f"\nFinal frame.f_locals: {frame.f_locals}")
    
    # Verification
    success = (
        local_string == "modified_string" and
        local_number == 999 and
        local_list == [7, 8, 9] and
        local_dict == {"new_key": "new_value"} and
        test_global == "modified_global"
    )
    
    print(f"\n=== RESULT: {'SUCCESS' if success else 'FAILED'} ===")
    return success

if __name__ == "__main__":
    test_setvariable_complete()
