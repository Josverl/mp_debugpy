# Copilot Instructions for mp_debugpy

## Repository Overview
This repository contains an experimental implementation of debugpy for MicroPython, enabling remote debugging with VS Code and other Debug Adapter Protocol (DAP) compatible debuggers. It allows developers to debug MicroPython code running on various platforms including Unix port and ESP32.

## Repository Structure
```
mp_debugpy/
├── .copilot/                    # Copilot instructions (this file)
├── .vscode/                     # VS Code configuration for debugging
├── README.md                    # Main documentation
├── pyproject.toml              # Python project configuration
├── src/                        # Example and test scripts
│   ├── test_vscode.py          # Main test script for VS Code debugging
│   ├── boot.py                 # MicroPython boot script
│   └── [other examples]        # Various demonstration scripts
├── python-ecosys/             # Core debugpy implementation
│   └── debugpy/               # Main debugpy module
│       ├── public_api.py      # Public API functions
│       ├── common/            # Common utilities and messaging
│       └── server/            # Debug session and PDB adapter
├── firmware/                  # Pre-built firmware with debug support
├── launcher/                  # Upload and deployment scripts
└── dockerfile                 # Docker configuration
```

## Core Concepts
- **debugpy**: MicroPython port of Microsoft's debugpy debugging library
- **DAP (Debug Adapter Protocol)**: Standard protocol for debugging communication
- **sys.settrace**: MicroPython's tracing mechanism for debugging support
- **Remote debugging**: Debug MicroPython code running on embedded devices

## Development Workflow

### Prerequisites
- MicroPython built with `MICROPY_PY_SYS_SETTRACE=1`
- Python 3.x for tooling and VS Code integration
- VS Code with Python extension for debugging

### Building MicroPython with Debug Support
For Unix port:
```bash
cd ports/unix
make CFLAGS_EXTRA="-DMICROPY_PY_SYS_SETTRACE=1"
```

For enhanced variable inspection:
```bash
make CFLAGS_EXTRA="-DMICROPY_PY_SYS_SETTRACE=1 -DMICROPY_PY_SYS_SETTRACE_SAVE_NAMES=1"
```

### Testing Changes
1. **Basic functionality test**:
   ```bash
   cd src/
   micropython test_vscode.py
   ```

2. **VS Code debugging test**:
   - Start the MicroPython script
   - Use VS Code "Attach to MicroPython" configuration
   - Set breakpoints and verify debugging works

3. **DAP protocol monitoring** (for debugging protocol issues):
   ```bash
   python3 python-ecosys/debugpy/dap_monitor.py
   ```

### Key Files to Understand

#### Core Implementation
- `python-ecosys/debugpy/public_api.py`: Main API functions (`listen()`, `debug_this_thread()`, etc.)
- `python-ecosys/debugpy/server/debug_session.py`: DAP protocol handler
- `python-ecosys/debugpy/server/pdb_adapter.py`: Bridge between trace system and debugger
- `python-ecosys/debugpy/common/messaging.py`: JSON/DAP message handling

#### Configuration
- `.vscode/launch.json`: VS Code debug configurations
- `.vscode/tasks.json`: Build and test tasks
- `pyproject.toml`: Python project settings and type checking

#### Examples and Tests
- `src/test_vscode.py`: Primary test script
- `python-ecosys/debugpy/demo.py`: Basic usage demonstration

## Coding Guidelines

### Python Code Style
- Follow MicroPython conventions for embedded code
- Use minimal imports and memory-efficient patterns
- Consider memory constraints on embedded targets

### Debugging Features
- Focus on core DAP protocol support
- Prioritize stability over advanced features
- Test on both Unix port and hardware targets

### Variable Inspection
The implementation supports variable inspection through MicroPython's `sys.settrace()`:
- Basic mode: Generic variable names (`local_01`, `local_02`)
- Enhanced mode: Real variable names when `MICROPY_PY_SYS_SETTRACE_SAVE_NAMES=1`

## Hardware Platforms

### Unix Port (Development)
- Primary development and testing platform
- Full debugging feature support
- Fast iteration cycle

### ESP32 
- Remote debugging over WiFi
- Custom firmware required
- Memory and performance constraints

## Common Tasks

### Adding New Debugging Features
1. Implement in `python-ecosys/debugpy/` modules
2. Update public API if needed
3. Test with `src/test_vscode.py`
4. Verify DAP protocol compliance

### Fixing Protocol Issues
1. Use DAP monitor: `python3 python-ecosys/debugpy/dap_monitor.py`
2. Enable VS Code verbose logging
3. Check DAP message sequence in logs
4. Reference `debug_session.py` for protocol handling

### Testing on Hardware
1. Build custom firmware with debug support
2. Upload using scripts in `launcher/`
3. Test remote debugging over network
4. Verify memory usage and performance

## Important Notes

### Limitations
- Single-threaded debugging only
- No conditional breakpoints
- Limited nested object expansion
- Maximum 32 local variables per frame (configurable)

### Memory Considerations
- Minimal overhead (~4 bytes per local variable mapping)
- Consider GC implications when debugging
- Test memory usage on target hardware

### Compatibility
- Works with or without variable name preservation
- Progressive enhancement as features are enabled
- Maintains backward compatibility

## Dependencies
- MicroPython with `sys.settrace` support
- Socket support for network communication
- JSON support for DAP message parsing
- VS Code Python extension for debugging

## Troubleshooting

### Common Issues
1. **Connection failures**: Ensure MicroPython is listening before connecting VS Code
2. **Breakpoint issues**: Verify `sys.settrace` support in firmware
3. **Variable inspection**: Check compilation flags for name preservation

### Debug Logging
- Enable VS Code DAP logging: set `debug.console.verbosity` to `verbose`
- Use DAP monitor for protocol analysis
- Check MicroPython console for debug output

## Contributing Guidelines
- Test changes on both Unix port and hardware
- Maintain minimal memory footprint
- Follow existing code patterns
- Update documentation for new features
- Ensure backward compatibility

Note: This repository does not contain git submodules, despite references in issues. The `python-ecosys` directory is a regular directory containing the core debugpy implementation.