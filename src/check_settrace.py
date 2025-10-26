import sys
from collections import OrderedDict as OD

try:
    import neopixel
    from machine import Pin
    np = neopixel.NeoPixel(Pin(15), 10)
except ImportError:
    print("neopixel module not found. Skipping NeoPixel initialization.")
    np = None

import asyncio

def tracer(frame, event, arg):
    try:
        try:
            filename = frame.f_code.co_filename
            co_name = frame.f_code.co_name
        except:
            filename = "<unknown>"
            co_name = "<unknown>"
        print(f"[{event:<10}] ({filename} {co_name} {frame.f_lineno} , {frame.f_lasti} ) ")
        # f_locals = OD(sorted(frame.f_locals.items()))
        # print("            ",f_locals)
        # del f_locals
        print("            ",frame.f_locals.items())
    except Exception as e:
        pass
    return tracer

def f_normal(n):
    i = 0
    while i < n:
        print(i)
        i += 1



async def blink(num, period_ms):
    while True and np:
        np[num] = (255, 0, 0)
        np.write()
        await asyncio.sleep_ms(period_ms)
        np[num] = (0, 0, 0)
        np.write()
        await asyncio.sleep_ms(period_ms)

async def a_main():
    asyncio.create_task(blink(1, 700))
    asyncio.create_task(blink(2, 1700))
    await asyncio.sleep_ms(10_000)

def call_frozen(n):
    if np:
        np.fill((0, 0, 0))
        np.write()
    print("*" * 40)
    asyncio.run(a_main())


print("="*40)
print("Tracing normal function")
print("="*40)
sys.settrace(tracer)
# f_normal(1)
call_frozen(1)

sys.settrace(None)
print("="*40)