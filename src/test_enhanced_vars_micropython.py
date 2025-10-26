"""MicroPython-compatible tests for enhanced variable retrieval."""
import sys
import os

# Simple test framework for MicroPython
class SimpleTest:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0
        
    def assert_equal(self, actual, expected, message=""):
        """Simple assertion for equality."""
        self.tests_run += 1
        if actual == expected:
            self.tests_passed += 1
            print(f"✅ PASS: {message}")
        else:
            self.tests_failed += 1
            print(f"❌ FAIL: {message}")
            print(f"   Expected: {expected}")
            print(f"   Actual: {actual}")
    
    def assert_true(self, condition, message=""):
        """Simple assertion for truth."""
        self.tests_run += 1
        if condition:
            self.tests_passed += 1
            print(f"✅ PASS: {message}")
        else:
            self.tests_failed += 1
            print(f"❌ FAIL: {message}")
            print(f"   Expected: True")
            print(f"   Actual: {condition}")
    
    def assert_greater_equal(self, actual, expected, message=""):
        """Simple assertion for greater than or equal."""
        self.tests_run += 1
        if actual >= expected:
            self.tests_passed += 1
            print(f"✅ PASS: {message}")
        else:
            self.tests_failed += 1
            print(f"❌ FAIL: {message}")
            print(f"   Expected >= {expected}")
            print(f"   Actual: {actual}")
    
    def assert_in(self, item, container, message=""):
        """Simple assertion for membership."""
        self.tests_run += 1
        if item in container:
            self.tests_passed += 1
            print(f"✅ PASS: {message}")
        else:
            self.tests_failed += 1
            print(f"❌ FAIL: {message}")
            print(f"   Expected '{item}' in {container}")
    
    def summary(self):
        """Print test summary."""
        print("\n" + "="*50)
        print(f"Test Summary:")
        print(f"  Total tests: {self.tests_run}")
        print(f"  Passed: {self.tests_passed}")
        print(f"  Failed: {self.tests_failed}")
        if self.tests_failed == 0:
            print("🎉 All tests passed!")
        else:
            print(f"⚠️  {self.tests_failed} test(s) failed")
        print("="*50)


def test_variable_reference_cache():
    """Test the VariableReferenceCache class."""
    print("\n📋 Testing VariableReferenceCache...")
    test = SimpleTest()
    
    # Import our enhanced classes - adjusted path for MicroPython
    import sys
    sys.path.append('micropython-lib/python-ecosys/debugpy')
    from debugpy.server.pdb_adapter import VariableReferenceCache, VARREF_COMPLEX_BASE
    
    # Test basic functionality
    cache = VariableReferenceCache(max_size=5)
    test_dict = {"key": "value"}
    ref_id = cache.add_variable(test_dict)
    
    test.assert_greater_equal(ref_id, VARREF_COMPLEX_BASE, 
                             "Reference ID should be >= VARREF_COMPLEX_BASE")
    test.assert_equal(cache.get_variable(ref_id), test_dict, 
                     "Retrieved variable should match original")
    
    # Test cache size limit
    refs = []
    for i in range(10):
        ref_id = cache.add_variable({"item": i})
        refs.append(ref_id)
    
    test.assert_true(len(cache.cache) <= cache.max_size, 
                    "Cache should respect size limits")
    test.assert_equal(cache.get_variable(refs[0]), None, 
                     "Oldest entries should be cleaned up")
    test.assert_true(cache.get_variable(refs[-1]) is not None, 
                    "Newest entries should still exist")
    
    # Test cache cleanup
    ref_id = cache.add_variable({"test": "data"})
    test.assert_true(cache.get_variable(ref_id) is not None, 
                    "Variable should exist before cleanup")
    cache.clear()
    test.assert_equal(cache.get_variable(ref_id), None, 
                     "Variable should be None after cleanup")
    test.assert_equal(len(cache.cache), 0, 
                     "Cache should be empty after clear")
    
    return test


def test_enhanced_variable_retrieval():
    """Test the enhanced variable retrieval functionality."""
    print("\n🔍 Testing Enhanced Variable Retrieval...")
    test = SimpleTest()
    
    # Import our enhanced classes - adjusted path for MicroPython
    import sys
    sys.path.append('micropython-lib/python-ecosys/debugpy')
    from debugpy.server.pdb_adapter import PdbAdapter, VARREF_COMPLEX_BASE
    
    pdb_adapter = PdbAdapter()
    
    # Test expandable type detection
    test.assert_true(pdb_adapter._is_expandable({"key": "value"}), 
                    "Dict should be expandable")
    test.assert_true(pdb_adapter._is_expandable([1, 2, 3]), 
                    "List should be expandable")
    test.assert_true(pdb_adapter._is_expandable((1, 2, 3)), 
                    "Tuple should be expandable")
    test.assert_true(pdb_adapter._is_expandable({1, 2, 3}), 
                    "Set should be expandable")
    test.assert_true(not pdb_adapter._is_expandable("string"), 
                    "String should not be expandable")
    test.assert_true(not pdb_adapter._is_expandable(42), 
                    "Int should not be expandable")
    
    # Test simple variable info
    info = pdb_adapter._get_variable_info("test_var", 42)
    test.assert_equal(info["name"], "test_var", "Variable name should match")
    test.assert_equal(info["value"], "42", "Variable value should be stringified")
    test.assert_equal(info["type"], "int", "Variable type should be correct")
    test.assert_equal(info["variablesReference"], 0, "Simple var should have no reference")
    
    # Test string variable info
    info = pdb_adapter._get_variable_info("test_str", "hello world")
    test.assert_equal(info["name"], "test_str", "String variable name should match")
    test.assert_equal(info["value"], "'hello world'", "String should be repr-formatted")
    test.assert_equal(info["type"], "str", "String type should be correct")
    
    # Test None variable info
    info = pdb_adapter._get_variable_info("test_none", None)
    test.assert_equal(info["name"], "test_none", "None variable name should match")
    test.assert_equal(info["value"], "None", "None should be represented as 'None'")
    test.assert_equal(info["type"], "NoneType", "None type should be correct")
    
    # Test dictionary variable info
    test_dict = {"key1": "value1", "key2": "value2"}
    info = pdb_adapter._get_variable_info("test_dict", test_dict)
    test.assert_equal(info["name"], "test_dict", "Dict variable name should match")
    test.assert_true("key1" in str(info["value"]) or "key2" in str(info["value"]), "Dict should show actual content")
    test.assert_equal(info["type"], "dict", "Dict type should be correct")
    test.assert_greater_equal(info["variablesReference"], VARREF_COMPLEX_BASE, 
                             "Dict should have complex reference")
    test.assert_equal(info["namedVariables"], 2, "Dict should have 2 named variables")
    test.assert_equal(info["indexedVariables"], 0, "Dict should have 0 indexed variables")
    
    # Test empty dictionary
    empty_dict = {}
    info = pdb_adapter._get_variable_info("empty_dict", empty_dict)
    test.assert_true("dict(empty)" in str(info["value"]), "Empty dict should show as empty")
    test.assert_equal(info["namedVariables"], 0, "Empty dict should have 0 named variables")
    
    # Test list variable info
    test_list = [1, 2, 3, "hello"]
    info = pdb_adapter._get_variable_info("test_list", test_list)
    test.assert_equal(info["name"], "test_list", "List variable name should match")
    test.assert_true("1" in str(info["value"]) or "hello" in str(info["value"]), "List should show actual content")
    test.assert_equal(info["type"], "list", "List type should be correct")
    test.assert_greater_equal(info["variablesReference"], VARREF_COMPLEX_BASE, 
                             "List should have complex reference")
    test.assert_equal(info["indexedVariables"], 4, "List should have 4 indexed variables")
    test.assert_equal(info["namedVariables"], 0, "List should have 0 named variables")
    
    return test


def test_variable_expansion():
    """Test expanding complex variables."""
    print("\n🌳 Testing Variable Expansion...")
    test = SimpleTest()
    
    # Import our enhanced classes - adjusted path for MicroPython
    import sys
    sys.path.append('micropython-lib/python-ecosys/debugpy')
    from debugpy.server.pdb_adapter import PdbAdapter, VARREF_COMPLEX_BASE
    
    pdb_adapter = PdbAdapter()
    
    # Test dictionary expansion
    test_dict = {"key1": "value1", "key2": 42, "key3": [1, 2, 3]}
    ref_id = pdb_adapter.var_cache.add_variable(test_dict)
    children = pdb_adapter._expand_complex_variable(ref_id)
    
    test.assert_equal(len(children), 3, "Dict should expand to 3 children")
    child_names = [child["name"] for child in children]
    test.assert_in("key1", child_names, "Dict should contain key1")
    test.assert_in("key2", child_names, "Dict should contain key2")
    test.assert_in("key3", child_names, "Dict should contain key3")
    
    # Check nested list gets proper reference
    key3_child = None
    for child in children:
        if child["name"] == "key3":
            key3_child = child
            break
    
    if key3_child is not None:
        test.assert_greater_equal(key3_child["variablesReference"], VARREF_COMPLEX_BASE, 
                                 "Nested list should have complex reference")
        test.assert_equal(key3_child["indexedVariables"], 3, 
                         "Nested list should have 3 indexed variables")
    else:
        test.assert_true(False, "key3 child should exist")
    
    # Test list expansion
    test_list = ["item1", 42, {"nested": "dict"}]
    ref_id = pdb_adapter.var_cache.add_variable(test_list)
    children = pdb_adapter._expand_complex_variable(ref_id)
    
    test.assert_equal(len(children), 3, "List should expand to 3 children")
    child_names = [child["name"] for child in children]
    test.assert_in("[0]", child_names, "List should contain [0]")
    test.assert_in("[1]", child_names, "List should contain [1]")
    test.assert_in("[2]", child_names, "List should contain [2]")
    
    # Check nested dict gets proper reference
    dict_child = None
    for child in children:
        if child["name"] == "[2]":
            dict_child = child
            break
    
    if dict_child is not None:
        test.assert_greater_equal(dict_child["variablesReference"], VARREF_COMPLEX_BASE, 
                                 "Nested dict should have complex reference")
        test.assert_equal(dict_child["namedVariables"], 1, 
                         "Nested dict should have 1 named variable")
    else:
        test.assert_true(False, "Dict child should exist")
    
    # Test tuple expansion
    test_tuple = ("first", "second", 123)
    ref_id = pdb_adapter.var_cache.add_variable(test_tuple)
    children = pdb_adapter._expand_complex_variable(ref_id)
    
    test.assert_equal(len(children), 3, "Tuple should expand to 3 children")
    test.assert_equal(children[0]["name"], "[0]", "First tuple element should be [0]")
    test.assert_equal(children[1]["name"], "[1]", "Second tuple element should be [1]")
    test.assert_equal(children[2]["name"], "[2]", "Third tuple element should be [2]")
    test.assert_equal(children[0]["value"], "'first'", "First element value should match (repr format)")
    test.assert_equal(children[2]["value"], "123", "Third element value should match")
    
    # Test nonexistent reference
    children = pdb_adapter._expand_complex_variable(99999)
    test.assert_equal(children, [], "Nonexistent reference should return empty list")
    
    return test


def test_integration_with_mock_frames():
    """Test integration with mock frame variables."""
    print("\n🔗 Testing Integration with Mock Frames...")
    test = SimpleTest()
    
    # Import our enhanced classes - adjusted path for MicroPython
    import sys
    sys.path.append('micropython-lib/python-ecosys/debugpy')
    from debugpy.server.pdb_adapter import PdbAdapter, VARREF_COMPLEX_BASE
    
    pdb_adapter = PdbAdapter()
    
    # Create a mock frame-like object
    class MockFrame:
        def __init__(self):
            self.f_locals = {
                "simple_var": 42,
                "dict_var": {"key1": "value1", "key2": [1, 2, 3]},
                "list_var": ["item1", "item2", {"nested": "value"}],
                "__special__": "special_value"
            }
            self.f_globals = {
                "global_dict": {"global_key": "global_value"},
                "global_simple": "simple_global"
            }
    
    mock_frame = MockFrame()
    pdb_adapter.variables_cache[0] = mock_frame
    
    # Test local variables (frame_id=0, scope_type=VARREF_LOCALS=1)
    variables = pdb_adapter.get_variables(0 * 1000 + 1)
    
    var_names = [var["name"] for var in variables]
    test.assert_in("Special", var_names, "Should have Special folder")
    test.assert_in("simple_var", var_names, "Should have simple_var")
    test.assert_in("dict_var", var_names, "Should have dict_var")
    test.assert_in("list_var", var_names, "Should have list_var")
    test.assert_true("__special__" not in var_names, 
                    "__special__ should be in Special folder")
    
    # Check complex variables have proper references
    dict_var = None
    list_var = None
    for var in variables:
        if var["name"] == "dict_var":
            dict_var = var
        elif var["name"] == "list_var":
            list_var = var
    
    if dict_var is not None:
        test.assert_greater_equal(dict_var["variablesReference"], VARREF_COMPLEX_BASE, 
                                 "dict_var should have complex reference")
        test.assert_equal(dict_var["namedVariables"], 2, 
                         "dict_var should have 2 named variables")
    else:
        test.assert_true(False, "dict_var should exist")
    
    if list_var is not None:
        test.assert_greater_equal(list_var["variablesReference"], VARREF_COMPLEX_BASE, 
                                 "list_var should have complex reference")
        test.assert_equal(list_var["indexedVariables"], 3, 
                         "list_var should have 3 indexed variables")
    else:
        test.assert_true(False, "list_var should exist")
    
    # Test global variables (frame_id=0, scope_type=VARREF_GLOBALS=2)
    variables = pdb_adapter.get_variables(0 * 1000 + 2)
    
    var_names = [var["name"] for var in variables]
    test.assert_in("Special", var_names, "Globals should have Special folder")
    test.assert_in("global_dict", var_names, "Should have global_dict")
    test.assert_in("global_simple", var_names, "Should have global_simple")
    
    # Check complex global variable
    global_dict = None
    for var in variables:
        if var["name"] == "global_dict":
            global_dict = var
            break
    
    if global_dict is not None:
        test.assert_greater_equal(global_dict["variablesReference"], VARREF_COMPLEX_BASE, 
                                 "global_dict should have complex reference")
    else:
        test.assert_true(False, "global_dict should exist")
    
    return test


def main():
    """Run all tests."""
    print("🧪 MicroPython Enhanced Variable Retrieval Tests")
    print("=" * 60)
    
    # Run all test suites
    tests = []
    tests.append(test_variable_reference_cache())
    tests.append(test_enhanced_variable_retrieval())
    tests.append(test_variable_expansion())
    tests.append(test_integration_with_mock_frames())
    
    # Calculate overall summary
    total_run = sum(t.tests_run for t in tests)
    total_passed = sum(t.tests_passed for t in tests)
    total_failed = sum(t.tests_failed for t in tests)
    
    print("\n" + "="*60)
    print("🏁 OVERALL TEST SUMMARY")
    print("="*60)
    print(f"  Total tests: {total_run}")
    print(f"  Passed: {total_passed}")
    print(f"  Failed: {total_failed}")
    
    if total_failed == 0:
        print("🎉 ALL TESTS PASSED! Enhanced variable retrieval is working correctly.")
    else:
        print(f"⚠️  {total_failed} test(s) failed. Please check the implementation.")
    
    print("="*60)
    
    return total_failed == 0


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
