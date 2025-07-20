## Debugger Performance Impact 

There is a very significant performance impact when using the debugger.
Measyring the performance impact of the debugger on a simple benchmark like Pystone 
shows that the performance is reduced by a factor of 1380.


Perf test of the micropython-debugpy adapter using pystones/sec

Baseline with no debugger : 65437

 container/ backend |  with debugpy | factor  | commit msg
-----------------|------------------|------|--------
  micropython/debugpy:0.3 | ? | .  | python-ecosys/debugpy: Add VS Code debugging support for MicroPython.
 native unix   |  51.2821  | 1380 |
 native unix   |  51.2821  | 1167  |
  ? | 77.31| .  | debugpy: Improve variable retrievals.
 micropython/debugpy:0.3 | 78.18 | .  | debugpy: Enhance path mapping handling in PDB adapter and debug session.
 micropython/debugpy:0.3 | 70.44 | .  | debugpy: Enhance PDB adapter with special variable processing.
 micropython/debugpy:0.3 | 69.69 | .  | debugpy: Add type hints and improve path mapping logic in PDB adapter
 micropython/debugpy:0.3| 101.59  | 600 | debugpy: Refactor breakpoint storage to use sets for improved efficiency
 micropython/debugpy:0.3 |109.42 | 598  |
 micropython/debugpy:0.3 | 106.58 | .  | debugpy: Add complex variable handling and caching.
 micropython/debugpy:0.3 | 113.19 | .  | debugpy: Enhance breakpoint handling and path mapping in PdbAdapter
 micropython/debugpy:0.3 | 117.69 | .  | debugpy : Optimize memory management and performance in PDB adapter.
 micropython/debugpy:0.3 | 114.78 | .  | Merge branch 'pdb_support/perf2' into debugpy/performance
 micropython/debugpy:0.3 | 109.59  | .  | revert: Overly complex variable preview.
  micropython/debugpy:0.4 |-   | .  | merge: py/modsys: Add ._set_local_var()  to set local variable in top frame for debugging support.
  micropython/debugpy:0.4 |119.21  | 548  | python-ecosys/debugpy: Add local variable modification while debugging + 
 micropython/debugpy:0.3 |x | .  |
  micropython/debugpy:0.3 |x | .  |
 
 <!-- optimised should_stop | docker/unix | 120.42 | 544 -->
 


MicroPython v1.26.0-preview.272.ga7c7a75eef.dirty on 2025-06-19
Average Pystones: 109.42 stones/second over 3 runs with 50 loops each. 
Average Pystones: 120.42 stones/second over 3 runs with 50 loops each.


How to measure:

 - `./start_performance.sh` will start the docker container with the debugpy server.
 - open the VSCode debugger and select the "Attach" configuration, select localhost and port 5678
 - the debugger will break, then press F5/continue to continue the execution.
 - note down the average execution time and update the table above


```
docker run -it --rm -p 5678:5678 -v ./src:/usr/micropython -v ./launcher:/usr/lib/micropython -v ./micropython-lib/python-ecosys/debugpy:/root/.micropython/lib micropython/debugpy:latest -m start_debugpy run_pystone main 

 _____  _______ ______ _______ _______ ______ ___ ___
|     \|    ___|   __ \   |   |     __|   __ \   |   |
|  --  |    ___|   __ <   |   |    |  |    __/\     /
|_____/|_______|______/_______|_______|___|    |___|

MicroPython VS Code Debugging Test
==================================
Target module: run_pystone
Target method: main
==================================
Debugpy listening on 0.0.0.0:5678
Debugger connected from bytearray(b'\x02\x00\xe4H\xac\x11\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00')
[DAP] Waiting for initialize request...
[DAP] Initialize request handled - returning control immediately
[DAP] Debug session ready - all other messages will be handled in trace function
Debug server attached on 0.0.0.0:5678
Connecting back to VS Code debugger now...

Giving VS Code time to set breakpoints...
[DAP] Debug logging disabled (logToFile=False)
Running iteration 1 of Pystone benchmark...
Pystone(1.2) time for 50 passes = 0.434
This machine benchmarks at 115.207 pystones/second
Iteration 1 completed in 63.63 seconds
Running iteration 2 of Pystone benchmark...
Pystone(1.2) time for 50 passes = 0.401
This machine benchmarks at 124.688 pystones/second
Iteration 2 completed in 63.16 seconds
Running iteration 3 of Pystone benchmark...
Pystone(1.2) time for 50 passes = 0.412
This machine benchmarks at 121.359 pystones/second
Iteration 3 completed in 63.21 seconds
Average Pystones: 120.42 stones/second over 3 runs with 50 loops each.
Target completed successfully!
No result returned from target.my_code()
```
