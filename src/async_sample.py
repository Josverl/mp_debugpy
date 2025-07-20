import uasyncio as asyncio

counter = 0


async def add_to_counter():
    global counter
    for _ in range(10):
        counter += 1
        print(f"Add: Counter is now {counter}")
        await asyncio.sleep(0.1)


async def modulo_counter():
    global counter
    for _ in range(10):
        counter %= 5
        print(f"Modulo: Counter is now {counter}")
        await asyncio.sleep(3)


async def a_main():
    await asyncio.gather(add_to_counter(), modulo_counter())


def main():
    asyncio.run(a_main())


if __name__ == "__main__":
    main()
