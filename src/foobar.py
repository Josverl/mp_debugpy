def greet(name):
    print(f"Hello, {name}!")

def add(a, b):
    result = a + b
    print(f"The sum of {a} and {b} is {result}")
    return result

def main():
    print("Starting demo app...")
    greet("Alice")
    total = add(3, "x")
    print(f"Total calculated: {total}")
    print("Demo app finished.")

if __name__ == "__main__":
    main()