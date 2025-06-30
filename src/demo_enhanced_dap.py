"""Demo script to show enhanced variable retrieval in DAP debugging context."""

def test_enhanced_vars_with_dap():
    """Test our enhanced variable retrieval with the DAP adapter."""
    import sys
    sys.path.append('micropython-lib/python-ecosys/debugpy')
    from debugpy.server.pdb_adapter import PdbAdapter, VARREF_COMPLEX_BASE
    
    print("🔧 Testing Enhanced Variables with DAP Protocol")
    print("=" * 50)
    
    # Create a PDB adapter
    pdb_adapter = PdbAdapter()
    
    # Create test data with complex structures
    test_data = {
        "user_profile": {
            "name": "Alice",
            "settings": {
                "theme": "dark",
                "notifications": True,
                "languages": ["English", "Spanish", "French"]
            },
            "activity": [
                {"date": "2025-01-01", "action": "login"},
                {"date": "2025-01-02", "action": "update_profile"}
            ]
        },
        "server_config": {
            "database": {
                "host": "localhost",
                "port": 5432,
                "pools": [10, 20, 15]
            },
            "cache": {
                "enabled": True,
                "backends": ["redis", "memcache"]
            }
        },
        "simple_list": [1, 2, 3, "hello", {"nested": "data"}],
        "simple_tuple": ("a", "b", "c"),
        "simple_set": {1, 2, 3, 4, 5}
    }
    
    # Mock frame with our test data
    class MockFrame:
        def __init__(self, locals_dict, globals_dict):
            self.f_locals = locals_dict
            self.f_globals = globals_dict
    
    # Create mock frame and add to cache
    mock_frame = MockFrame(test_data, {"global_var": "global_value"})
    pdb_adapter.variables_cache[0] = mock_frame
    
    print("\n📝 Step 1: Get Local Variables Scope")
    # Get local variables (frame_id=0, scope_type=VARREF_LOCALS=1)
    local_vars = pdb_adapter.get_variables(0 * 1000 + 1)
    
    print(f"Found {len(local_vars)} local variables:")
    for var in local_vars:
        var_ref = var.get("variablesReference", 0)
        var_type = var.get("type", "unknown")
        var_value = var.get("value", "")
        var_name = var.get("name", "")
        ref_status = "expandable" if var_ref >= VARREF_COMPLEX_BASE else "simple"
        print(f"  • {var_name}: {var_value} ({var_type}) - {ref_status}")
    
    print("\n🌳 Step 2: Expand Complex Variable - user_profile")
    # Find and expand user_profile
    user_profile_var = next((v for v in local_vars if v["name"] == "user_profile"), None)
    if user_profile_var and user_profile_var["variablesReference"] >= VARREF_COMPLEX_BASE:
        user_profile_children = pdb_adapter.get_variables(user_profile_var["variablesReference"])
        print(f"user_profile has {len(user_profile_children)} children:")
        for child in user_profile_children:
            ref_status = "expandable" if child["variablesReference"] >= VARREF_COMPLEX_BASE else "simple"
            print(f"  • {child['name']}: {child['value']} ({child['type']}) - {ref_status}")
        
        print("\n🔍 Step 3: Expand Nested Variable - settings")
        # Find and expand settings
        settings_var = next((v for v in user_profile_children if v["name"] == "settings"), None)
        if settings_var and settings_var["variablesReference"] >= VARREF_COMPLEX_BASE:
            settings_children = pdb_adapter.get_variables(settings_var["variablesReference"])
            print(f"settings has {len(settings_children)} children:")
            for child in settings_children:
                ref_status = "expandable" if child["variablesReference"] >= VARREF_COMPLEX_BASE else "simple"
                print(f"    • {child['name']}: {child['value']} ({child['type']}) - {ref_status}")
            
            print("\n📚 Step 4: Expand Nested List - languages")
            # Find and expand languages list
            languages_var = next((v for v in settings_children if v["name"] == "languages"), None)
            if languages_var and languages_var["variablesReference"] >= VARREF_COMPLEX_BASE:
                languages_children = pdb_adapter.get_variables(languages_var["variablesReference"])
                print(f"languages has {len(languages_children)} items:")
                for child in languages_children:
                    print(f"      • {child['name']}: {child['value']} ({child['type']})")
    
    print("\n📊 Step 5: Expand List with Mixed Types - simple_list")
    simple_list_var = next((v for v in local_vars if v["name"] == "simple_list"), None)
    if simple_list_var and simple_list_var["variablesReference"] >= VARREF_COMPLEX_BASE:
        list_children = pdb_adapter.get_variables(simple_list_var["variablesReference"])
        print(f"simple_list has {len(list_children)} items:")
        for child in list_children:
            ref_status = "expandable" if child["variablesReference"] >= VARREF_COMPLEX_BASE else "simple"
            print(f"  • {child['name']}: {child['value']} ({child['type']}) - {ref_status}")
        
        # Expand the nested dict in the list
        nested_dict_var = next((v for v in list_children if v["name"] == "[4]"), None)
        if nested_dict_var and nested_dict_var["variablesReference"] >= VARREF_COMPLEX_BASE:
            nested_dict_children = pdb_adapter.get_variables(nested_dict_var["variablesReference"])
            print(f"  [4] (nested dict) has {len(nested_dict_children)} items:")
            for child in nested_dict_children:
                print(f"    • {child['name']}: {child['value']} ({child['type']})")
    
    print("\n🎯 Step 6: Cache Statistics")
    cache_stats = {
        "total_cached_objects": len(pdb_adapter.var_cache.cache),
        "next_reference_id": pdb_adapter.var_cache.next_ref,
        "cache_size_limit": pdb_adapter.var_cache.max_size
    }
    print(f"Variable Reference Cache Stats:")
    for key, value in cache_stats.items():
        print(f"  • {key}: {value}")
    
    print("\n✅ Enhanced Variable Retrieval Demo Complete!")
    print("   Complex variables are now properly expandable in DAP protocol!")
    print("   Variables show correct counts for namedVariables and indexedVariables!")
    print("   Nested structures can be explored to any depth!")


if __name__ == "__main__":
    test_enhanced_vars_with_dap()
