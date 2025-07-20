"""
Simple test to debug the frame._set_local variable assignment issue.
"""


def debug_set_local():
    """Debug frame._set_local variable assignment."""

    # Simple local variables
    var_a = "original_a"
    var_b = 100
    var_c = [1, 2, 3]

    print("=== BEFORE ===")
    print(f"var_a = {var_a}")
    print(f"var_b = {var_b}")
    print(f"var_c = {var_c}")

    # Get frame and show locals
    import sys

    frame = sys._getframe()

    print("\n=== FRAME LOCALS ===")
    frame_locals = frame.f_locals
    for name, value in frame_locals.items():
        print(f"{name} = {value}")

    print("\n=== TESTING SET_LOCAL ===")
    print(dir(frame))
    # Test setting one by one
    print("Setting var_a...")
    frame._set_local("var_a", "modified_a")
    print(f"After setting var_a: {var_a}")

    print("Setting var_b...")
    frame._set_local("var_b", 999)
    print(f"After setting var_b: {var_b}")

    print("Setting var_c...")
    frame._set_local("var_c", [7, 8, 9])
    print(f"After setting var_c: {var_c}")

    print("\n=== FINAL FRAME LOCALS ===")
    frame_locals = frame.f_locals
    for name, value in frame_locals.items():
        print(f"{name} = {value}")

    print("\n=== FINAL VALUES ===")
    print(f"var_a = {var_a}")
    print(f"var_b = {var_b}")
    print(f"var_c = {var_c}")


if __name__ == "__main__":
    debug_set_local()
