# Breakpoints: 20, 25
import sys
import time


def foo():
    """A simple function to demonstrate debugging."""
    print("Hello from foo!")
    return "foo result"


def bar(x):
    """A simple function to demonstrate debugging."""
    print(f"Hello from bar with argument {x}!")
    return f"bar result with {x}"


def main():
    """The actual code we want to debug"""
    print("Running debuggable code...")  # <-- Breakpoint
    for i in range(100):
        foo()
        x = bar(i)
        print(f"Iteration {i}: x = {x}")
    print("Done...")  # <-- Breakpoint


if __name__ == "__main__":
    main()
