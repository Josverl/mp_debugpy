"""Demo script to test enhanced variable retrieval for complex types."""

def test_complex_variables():
    """Function with various complex variable types for debugging."""
    # Dictionary variables
    simple_dict = {"name": "John", "age": 30}
    nested_dict = {
        "user": {
            "profile": {
                "settings": ["dark_mode", "notifications"]
            }
        },
        "metadata": {"created": "2025-01-01"}
    }
    empty_dict = {}
    
    # List variables
    simple_list = [1, 2, 3, "hello", "world"]
    nested_list = [
        {"item": 1, "data": [10, 20, 30]},
        {"item": 2, "data": [40, 50, 60]},
        "simple_string"
    ]
    empty_list = []
    
    # Tuple variables
    simple_tuple = (1, "two", 3.0)
    nested_tuple = (
        {"key": "value"},
        [1, 2, 3],
        (4, 5, 6)
    )
    
    # Set variables
    simple_set = {1, 2, 3, 4, 5}
    mixed_set = {"apple", "banana", 42, 3.14}
    empty_set = set()
    
    # Mixed complex structure
    complex_structure = {
        "config": {
            "database": {
                "host": "localhost",
                "port": 5432,
                "credentials": ["user", "pass"]
            },
            "cache": {
                "enabled": True,
                "ttl": 3600,
                "backends": ["redis", "memcache"]
            }
        },
        "users": [
            {"id": 1, "name": "Alice", "roles": ["admin", "user"]},
            {"id": 2, "name": "Bob", "roles": ["user"]},
        ],
        "statistics": {
            "active_users": 150,
            "daily_requests": [1000, 1200, 900, 1500],
            "server_metrics": {
                "cpu": 45.2,
                "memory": 78.5,
                "disk": {"used": 120, "total": 500}
            }
        }
    }
    
    # Simple variables for comparison
    simple_int = 42
    simple_str = "Hello, MicroPython Debugger!"
    simple_float = 3.14159
    simple_bool = True
    simple_none = None
    
    # This is where we'll set a breakpoint for testing
    print("Complex variables created - set breakpoint here!")
    print(f"Dictionary count: {len(simple_dict)}")
    print(f"List count: {len(simple_list)}")
    print(f"Complex structure keys: {list(complex_structure.keys())}")
    
    return {
        "dicts": [simple_dict, nested_dict, empty_dict],
        "lists": [simple_list, nested_list, empty_list],
        "tuples": [simple_tuple, nested_tuple],
        "sets": [simple_set, mixed_set, empty_set],
        "complex": complex_structure,
        "simple": [simple_int, simple_str, simple_float, simple_bool, simple_none]
    }


def main():
    """Main function to run the demo."""
    print("Enhanced Variable Retrieval Demo")
    print("=" * 40)
    
    # Global variables for testing
    global_dict = {"global_key": "global_value", "global_list": [1, 2, 3]}
    global_list = ["global_item1", {"nested": "global"}]
    
    print("Starting complex variable test...")
    result = test_complex_variables()
    
    print("Demo completed!")
    print(f"Result keys: {list(result.keys())}")


if __name__ == "__main__":
    main()
