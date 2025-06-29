#!/bin/bash

# copy the debugpy module into the lib folder
mpremote resume mkdir lib 
# mpremote cp -r micropython-lib/python-ecosys/debugpy/debugpy :/lib

# copy the src directory to the root of the ESP32 filesystem
# workaround for windows issue with mpremote cp -r
cd src 
mpremote resume cp -r . :/
cd ..

# start the debugpy server on the ESP32
mpremote run launcher/start_debugpy_esp32.py 

# mpremote mount src + run launcher/start_debugpy_esp32.py 
