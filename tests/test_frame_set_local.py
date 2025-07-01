"""Test frame.set_local method for setting local variables in MicroPython."""

import sys


def test_set_local():
    """Test setting local variables using frame.set_local."""
    x = 10
    y = 20
    z = "hello"
    
    print(f"Before: x={x}, y={y}, z={z}")
    
    # Get the current frame
    frame = sys._getframe()
    
    # Try to set local variables using frame._set_local
    try:
        print("Testing frame._set_local method:")
        frame._set_local("x", 100)
        frame._set_local("y", 200)
        frame._set_local("z", "world")
        print(f"After _set_local: x={x}, y={y}, z={z}")
        return True
    except AttributeError as e:
        print(f"AttributeError: {e}")
        print("frame._set_local method not available")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_nested_frame():
    """Test setting variables in a nested function."""
    def inner_func():
        a = 1
        b = 2
        print(f"Inner before: a={a}, b={b}")
        
        # Get the current frame
        frame = sys._getframe()
        try:
            frame._set_local("a", 10)
            frame._set_local("b", 20)
            print(f"Inner after: a={a}, b={b}")
            return True
        except Exception as e:
            print(f"Inner error: {e}")
            return False
    
    return inner_func()


if __name__ == "__main__":
    print("Testing frame._set_local method in MicroPython")
    print("=" * 50)
    
    # Test basic functionality
    success1 = test_set_local()
    print()
    
    # Test nested frame
    success2 = test_nested_frame()
    print()
    
    if success1 and success2:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
        
    # Also test if the method exists
    frame = sys._getframe()
    print(f"Frame object: {frame}")
    print(f"Frame dir: {dir(frame)}")
