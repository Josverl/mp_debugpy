# Instructions for AI Assistant

## Writing Python Code
1. Write clear and maintainable Python code.
2. Use descriptive variable and function names to improve readability.
3. Follow PEP 8 guidelines for code formatting.
4. Use static typing with type hints to ensure type safety and improve code clarity, but limit this to simple types (e.g., `int`, `str`, `list`, `dict`) to maintain compatibility with MicroPython.
5. Add meaningful comments and docstrings to explain the purpose of functions, classes, and complex logic.
6. Ensure the code is compatible with MicroPython, rather than CPython, and optimized for constrained devices with limited resources.



## running Micropython Code
1. Use the `firmware/unix_settrace_save_names/micropython` micropython binary for testing and verification of scripts and modules, as it includes `sys.settrace` support.
   usage: firmware/unix_settrace_save_names/micropython [-c <command> | -m <module> | <filename>]
   to runMicropython with all relevant sys.paths already configured, 
   use the docker image with the command : `docker run -it --rm -p 5678:5678 -v ./src:/usr/micropython -v ./launcher:/usr/lib/micropython -v ./micropython-lib/python-ecosys/debugpy:/root/.micropython/lib micropython/debugpy:0.3 -m <module>`.
   note that neither pytest not unit test are available in the container 

## Testing Micropython Python Code from micropython-lib or the src folder
1. Use the unittest framework for writing unit tests.
2. Ensure that each function or method has corresponding test cases.
3. Write tests to cover edge cases, invalid inputs, and expected outputs.
4. Use fixtures to set up reusable test data or configurations.
5. Mock external dependencies to isolate the functionality being tested.
6. Ensure tests are deterministic and do not depend on external factors like time or network.

## General Guidelines
1. Prioritize simplicity and readability over clever or overly complex solutions.
2. Avoid hardcoding values; use constants or configuration files where appropriate.
3. Ensure the code is modular and reusable by breaking it into smaller functions or classes.
4. Test the code thoroughly to ensure correctness and reliability.
5. Document any assumptions or limitations in the code or tests.
6. Ensure the code is distributed across different repositories in a way that promotes modularity and maintainability.
7. Optimize the code for constrained devices with limited memory and processing power.

## MicroPython and MicroPython-lib

MicroPython is a lean and efficient implementation of Python 3 designed for microcontrollers and constrained environments. It provides a subset of Python's standard library and is optimized for low memory usage and high performance. MicroPython is widely used in embedded systems, IoT devices, and other resource-constrained applications.

### Key Features of MicroPython
Micropython is checked out in the `./micropython` folder 
1. **Lightweight and Efficient**: Designed to run on devices with limited memory and processing power.
2. **Python Compatibility**: Implements a subset of Python 3, making it easy for Python developers to transition to embedded programming.

### MicroPython-lib
the most relevant part of Micropython-lib is checked out in the `./micropython-lib` folder 
MicroPython-lib is a collection of Python libraries specifically tailored for MicroPython. These libraries provide additional functionality while adhering to the constraints of MicroPython environments. Developers can use MicroPython-lib to extend the capabilities of their applications without compromising performance or memory efficiency.
one of the modules under development is `debugpy`, which implements the Debug Adapter Protocol (DAP) for MicroPython, enabling debugging capabilities similar to those available in CPython.

### Relevant References
1. **Optimizing Python Code for Speed**: Learn how to write efficient Python code for MicroPython environments. [Reference: Speed and Performance](https://docs.micropython.org/en/latest/reference/speed_python.html)
2. **MicroPython Development**: Explore the development process and best practices for working with MicroPython. [Reference: MicroPython Development](https://docs.micropython.org/en/latest/develop/index.html)
3. **Memory Management in MicroPython**: Understand how MicroPython handles memory and how to optimize memory usage in constrained environments. [Reference: Memory Management](https://docs.micropython.org/en/latest/develop/memorymgt.html)


## Relevant External Information on Debug Adapter Protocol (DAP)
The goal of this workspace is to implement a minimal Debug Adapter Protocol (DAP) for MicroPython, enabling debugging capabilities similar to those available in CPython. The implementation should be compatible with existing tools and libraries, such as `debugpy` and the Visual Studio Code Python debugger extension.

1. **Debug Adapter Protocol**: The Debug Adapter Protocol (DAP) is a standardized protocol for communication between development tools and debuggers. It is designed to enable interoperability between different debuggers and IDEs. 
 More information can be found at [Debug Adapter Protocol Documentation](https://microsoft.github.io/debug-adapter-protocol/).
2. **microsoft/debugpy**: `debugpy` is an implementation of the Debug Adapter Protocol for Python. It provides debugging capabilities for Python applications and is actively maintained by Microsoft. 
Repository: [microsoft/debugpy](https://github.com/microsoft/debugpy).
3. **microsoft/vscode-python-debugger**: This is the Python debugger extension for Visual Studio Code, built on top of `debugpy`. 
It integrates Python debugging into VS Code using the Debug Adapter Protocol. Repository: [microsoft/vscode-python-debugger](https://github.com/microsoft/vscode-python-debugger).