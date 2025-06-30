"""Unit tests for enhanced variable retrieval in MicroPython debugpy."""
import pytest
import sys
import os

# Add the debugpy package to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'micropython-lib', 'python-ecosys'))

from debugpy.server.pdb_adapter import PdbAdapter, VariableReferenceCache, VARREF_COMPLEX_BASE


class TestVariableReferenceCache:
    """Test the variable reference cache system."""
    
    @pytest.fixture
    def cache(self):
        """Create a cache instance for testing."""
        return VariableReferenceCache(max_size=5)
    
    def test_add_simple_variable(self, cache):
        """Test adding a simple variable to cache."""
        test_dict = {"key": "value"}
        ref_id = cache.add_variable(test_dict)
        
        assert ref_id >= VARREF_COMPLEX_BASE
        assert cache.get_variable(ref_id) is test_dict
    
    def test_cache_size_limit(self, cache):
        """Test that cache respects size limits."""
        # Add items beyond cache limit
        refs = []
        for i in range(10):
            ref_id = cache.add_variable({"item": i})
            refs.append(ref_id)
        
        # Cache should have cleaned up oldest entries
        assert len(cache.cache) <= cache.max_size
        
        # Oldest entries should be gone
        assert cache.get_variable(refs[0]) is None
        # Newest entries should still exist
        assert cache.get_variable(refs[-1]) is not None
    
    def test_cache_cleanup(self, cache):
        """Test manual cache cleanup."""
        ref_id = cache.add_variable({"test": "data"})
        assert cache.get_variable(ref_id) is not None
        
        cache.clear()
        assert cache.get_variable(ref_id) is None
        assert len(cache.cache) == 0


class TestEnhancedVariableRetrieval:
    """Test enhanced variable retrieval functionality."""
    
    @pytest.fixture
    def pdb_adapter(self):
        """Create a PdbAdapter instance for testing."""
        return PdbAdapter()
    
    def test_is_expandable(self, pdb_adapter):
        """Test expandable type detection."""
        assert pdb_adapter._is_expandable({"key": "value"}) is True
        assert pdb_adapter._is_expandable([1, 2, 3]) is True
        assert pdb_adapter._is_expandable((1, 2, 3)) is True
        assert pdb_adapter._is_expandable({1, 2, 3}) is True
        assert pdb_adapter._is_expandable("string") is False
        assert pdb_adapter._is_expandable(42) is False
    
    def test_get_variable_info_simple(self, pdb_adapter):
        """Test variable info for simple types."""
        info = pdb_adapter._get_variable_info("test_var", 42)
        
        assert info["name"] == "test_var"
        assert info["value"] == "42"
        assert info["type"] == "int"
        assert info["variablesReference"] == 0
    
    def test_get_variable_info_string(self, pdb_adapter):
        """Test variable info for string types."""
        info = pdb_adapter._get_variable_info("test_str", "hello world")
        
        assert info["name"] == "test_str"
        assert info["value"] == '"hello world"'
        assert info["type"] == "str"
        assert info["variablesReference"] == 0
    
    def test_get_variable_info_none(self, pdb_adapter):
        """Test variable info for None type."""
        info = pdb_adapter._get_variable_info("test_none", None)
        
        assert info["name"] == "test_none"
        assert info["value"] == "None"
        assert info["type"] == "NoneType"
        assert info["variablesReference"] == 0
    
    def test_get_variable_info_dict(self, pdb_adapter):
        """Test variable info for dictionary types."""
        test_dict = {"key1": "value1", "key2": "value2"}
        info = pdb_adapter._get_variable_info("test_dict", test_dict)
        
        assert info["name"] == "test_dict"
        assert "dict(2 items)" in info["value"]
        assert info["type"] == "dict"
        assert info["variablesReference"] >= VARREF_COMPLEX_BASE
        assert info["namedVariables"] == 2
        assert info["indexedVariables"] == 0
    
    def test_get_variable_info_empty_dict(self, pdb_adapter):
        """Test variable info for empty dictionary."""
        test_dict = {}
        info = pdb_adapter._get_variable_info("empty_dict", test_dict)
        
        assert info["name"] == "empty_dict"
        assert "dict(empty)" in info["value"]
        assert info["type"] == "dict"
        assert info["variablesReference"] >= VARREF_COMPLEX_BASE
        assert info["namedVariables"] == 0
    
    def test_get_variable_info_list(self, pdb_adapter):
        """Test variable info for list types."""
        test_list = [1, 2, 3, "hello"]
        info = pdb_adapter._get_variable_info("test_list", test_list)
        
        assert info["name"] == "test_list"
        assert "list(4 items)" in info["value"]
        assert info["type"] == "list"
        assert info["variablesReference"] >= VARREF_COMPLEX_BASE
        assert info["indexedVariables"] == 4
        assert info["namedVariables"] == 0
    
    def test_get_variable_info_tuple(self, pdb_adapter):
        """Test variable info for tuple types."""
        test_tuple = (1, 2, "hello")
        info = pdb_adapter._get_variable_info("test_tuple", test_tuple)
        
        assert info["name"] == "test_tuple"
        assert "tuple(3 items)" in info["value"]
        assert info["type"] == "tuple"
        assert info["variablesReference"] >= VARREF_COMPLEX_BASE
        assert info["indexedVariables"] == 3
    
    def test_get_variable_info_set(self, pdb_adapter):
        """Test variable info for set types."""
        test_set = {1, 2, 3}
        info = pdb_adapter._get_variable_info("test_set", test_set)
        
        assert info["name"] == "test_set"
        assert "set(3 items)" in info["value"]
        assert info["type"] == "set"
        assert info["variablesReference"] >= VARREF_COMPLEX_BASE
        assert info["indexedVariables"] == 3
    
    def test_expand_dict_variable(self, pdb_adapter):
        """Test expanding a dictionary variable."""
        test_dict = {"key1": "value1", "key2": 42, "key3": [1, 2, 3]}
        ref_id = pdb_adapter.var_cache.add_variable(test_dict)
        
        children = pdb_adapter._expand_complex_variable(ref_id)
        
        assert len(children) == 3
        child_names = [child["name"] for child in children]
        assert "key1" in child_names
        assert "key2" in child_names
        assert "key3" in child_names
        
        # Check that nested list gets proper variable reference
        key3_child = next(child for child in children if child["name"] == "key3")
        assert key3_child["variablesReference"] >= VARREF_COMPLEX_BASE
        assert key3_child["indexedVariables"] == 3
    
    def test_expand_list_variable(self, pdb_adapter):
        """Test expanding a list variable."""
        test_list = ["item1", 42, {"nested": "dict"}]
        ref_id = pdb_adapter.var_cache.add_variable(test_list)
        
        children = pdb_adapter._expand_complex_variable(ref_id)
        
        assert len(children) == 3
        child_names = [child["name"] for child in children]
        assert "[0]" in child_names
        assert "[1]" in child_names
        assert "[2]" in child_names
        
        # Check that nested dict gets proper variable reference
        dict_child = next(child for child in children if child["name"] == "[2]")
        assert dict_child["variablesReference"] >= VARREF_COMPLEX_BASE
        assert dict_child["namedVariables"] == 1
    
    def test_expand_tuple_variable(self, pdb_adapter):
        """Test expanding a tuple variable."""
        test_tuple = ("first", "second", 123)
        ref_id = pdb_adapter.var_cache.add_variable(test_tuple)
        
        children = pdb_adapter._expand_complex_variable(ref_id)
        
        assert len(children) == 3
        assert children[0]["name"] == "[0]"
        assert children[1]["name"] == "[1]"
        assert children[2]["name"] == "[2]"
        assert children[0]["value"] == '"first"'
        assert children[2]["value"] == "123"
    
    def test_expand_set_variable(self, pdb_adapter):
        """Test expanding a set variable."""
        test_set = {3, 1, 2}  # Will be sorted for display
        ref_id = pdb_adapter.var_cache.add_variable(test_set)
        
        children = pdb_adapter._expand_complex_variable(ref_id)
        
        assert len(children) == 3
        # Check that elements are displayed with <index> notation
        child_names = [child["name"] for child in children]
        assert "<0>" in child_names
        assert "<1>" in child_names
        assert "<2>" in child_names
    
    def test_expand_nested_structures(self, pdb_adapter):
        """Test expanding deeply nested structures."""
        nested_data = {
            "level1": {
                "level2": {
                    "level3": ["deep", "list"]
                }
            },
            "simple": "value"
        }
        ref_id = pdb_adapter.var_cache.add_variable(nested_data)
        
        # Expand first level
        level1_children = pdb_adapter._expand_complex_variable(ref_id)
        assert len(level1_children) == 2
        
        # Find and expand the nested dict
        level1_child = next(child for child in level1_children if child["name"] == "level1")
        level1_ref = level1_child["variablesReference"]
        
        level2_children = pdb_adapter._expand_complex_variable(level1_ref)
        assert len(level2_children) == 1
        assert level2_children[0]["name"] == "level2"
    
    def test_expand_nonexistent_reference(self, pdb_adapter):
        """Test expanding a nonexistent variable reference."""
        children = pdb_adapter._expand_complex_variable(99999)
        assert children == []
    
    def test_get_variables_complex_expansion(self, pdb_adapter):
        """Test the full get_variables flow with complex variable expansion."""
        # Create a test dict and add it to cache
        test_dict = {"key1": "value1", "key2": [1, 2, 3]}
        ref_id = pdb_adapter.var_cache.add_variable(test_dict)
        
        # Test that get_variables handles complex variable references
        variables = pdb_adapter.get_variables(ref_id)
        
        assert len(variables) == 2
        child_names = [var["name"] for var in variables]
        assert "key1" in child_names
        assert "key2" in child_names


class TestIntegrationWithFrames:
    """Test integration with actual frame variables."""
    
    @pytest.fixture
    def pdb_adapter_with_frame(self):
        """Create a PdbAdapter with a mock frame for testing."""
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
        return pdb_adapter
    
    def test_get_locals_with_complex_variables(self, pdb_adapter_with_frame):
        """Test getting local variables with complex types."""
        # Request local variables (frame_id=0, scope_type=VARREF_LOCALS=1)
        variables = pdb_adapter_with_frame.get_variables(0 * 1000 + 1)
        
        # Should have Special folder plus regular variables
        var_names = [var["name"] for var in variables]
        assert "Special" in var_names
        assert "simple_var" in var_names
        assert "dict_var" in var_names
        assert "list_var" in var_names
        assert "__special__" not in var_names  # Should be in Special folder
        
        # Check that complex variables have proper references
        dict_var = next(var for var in variables if var["name"] == "dict_var")
        assert dict_var["variablesReference"] >= VARREF_COMPLEX_BASE
        assert dict_var["namedVariables"] == 2
        
        list_var = next(var for var in variables if var["name"] == "list_var")
        assert list_var["variablesReference"] >= VARREF_COMPLEX_BASE
        assert list_var["indexedVariables"] == 3
    
    def test_get_globals_with_complex_variables(self, pdb_adapter_with_frame):
        """Test getting global variables with complex types."""
        # Request global variables (frame_id=0, scope_type=VARREF_GLOBALS=2)
        variables = pdb_adapter_with_frame.get_variables(0 * 1000 + 2)
        
        var_names = [var["name"] for var in variables]
        assert "Special" in var_names
        assert "global_dict" in var_names
        assert "global_simple" in var_names
        
        # Check complex global variable
        global_dict = next(var for var in variables if var["name"] == "global_dict")
        assert global_dict["variablesReference"] >= VARREF_COMPLEX_BASE


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
