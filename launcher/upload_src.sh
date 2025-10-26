#!/bin/bash

# copy the debugpy module into the lib folder
mpremote mkdir lib 

# NOTE: commented to reduce launch time
mpremote cp -r micropython-lib/python-ecosys/debugpy/debugpy :/lib

# copy the src directory to the root of the ESP32 filesystem
mpremote cp -r src/* :/

# start the debugpy server on the ESP32
mpremote run launcher/start_debugpy_esp32.py 


