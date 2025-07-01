"""
Simple test script to verify DAP setVariable functionality
"""

def test_dap_setvariable():
    """Test function for DAP setVariable debugging"""
    # Local variables to test
    string_var = "hello"
    number_var = 42
    list_var = [1, 2, 3]
    
    # Global variable to test
    global global_test_var
    global_test_var = "global_value"
    
    print(f"Initial values:")
    print(f"  string_var: {string_var}")
    print(f"  number_var: {number_var}")
    print(f"  list_var: {list_var}")
    print(f"  global_test_var: {global_test_var}")
    
    # Breakpoint here - debugger can test setVariable
    # Set breakpoint on this line and test:
    # 1. Setting string_var to "modified_string"
    # 2. Setting number_var to 999
    # 3. Setting list_var to [4, 5, 6]
    # 4. Setting global_test_var to "modified_global"
    breakpoint_line = True  # <-- Set breakpoint here
    
    print(f"Final values:")
    print(f"  string_var: {string_var}")
    print(f"  number_var: {number_var}")
    print(f"  list_var: {list_var}")
    print(f"  global_test_var: {global_test_var}")

if __name__ == "__main__":
    test_dap_setvariable()
