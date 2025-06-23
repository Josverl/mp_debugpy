
flash using the following command:
```bash
# erase 
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
# flash
esptool.py --chip esp32 --port /dev/ttyUSB0 -b 921600 write_flash --flash_mode keep --flash_size detect --compress 0x1000 firmware/esp32_settrace_save_names/firmware.bin 
```