import sys
import time

implementation = sys.implementation
foo = 42
bar = "Hello, MicroPython!"
camelot = {"location": "England", "song": "We're knights of the round table"}


def fibonacci(n):
    """Calculate fibonacci number (iterative for efficiency)."""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def inspect_local_variables():
    __platform__ = sys.platform
    dead_parrot = "Norwegian Blue"
    cheese_shop = ["Cheddar", "Stilton", "Wensleydale"]
    cheese_market = cheese_shop.copy() * 40
    holy_grail = {"quest": "find", "knights": 12}
    black_knight = {"arms": 0, "legs": 2, "status": "It's just a flesh wound!"}
    spam = ["spam"] * 5
    silly_walk = lambda x: f"Walked {x} meters, very silly!"
    _lumberjack = {"job": "lumberjack", "location": "Canada"}
    __argument_clinic = {"minutes": 5, "type": "contradiction"}
    knights = ("Arthur", "Lancelot", ("sir", "Galahad"), "Bedevere")
    __foot__ = "In the clouds"
    spanish_inquisition = {"expected": False, "weapons": ["fear", "surprise", "ruthless efficiency"]}
    dead_bishop = "on the landing"
    upper_class_twit = {"name": "Vivian Smith-Smythe-Smith", "score": 0}
    ministry_of_silly_walks = True
    fish_slapping_dance = ["slap", "slap", "splash"]
    life_of_brian = 1979
    biggus_dickus = {"friend": "Incontinentia Buttocks"}
    mr_creosote = {"weight": 300, "last_meal": "wafer-thin mint"}
    knights_who_say_ni = ["Ni!", "Ekke Ekke Ekke Ekke Ptang Zoo Boing!"]
    holy_hand_grenade = {"count": 3, "instructions": "Three shall be the number thou shalt count"}
    rabbit_of_caerbannog = {"teeth": "sharp", "danger": True}
    if False:
        french_taunter = {"insults": ["Your mother was a hamster!", "I fart in your general direction!"]}
        brave_sir_robin = {"ran_away": True}
        tim_enchanter = {"magic": ["fireball", "explosion"]}
        coconuts = 2
        swallow_velocity = {"african": 11, "european": 10}
        ex_leper = {"status": "cured", "income": 0}
        confused_cat = "Meow?"
        mouse_organ = ["mouse1", "mouse2", "mouse3"]
        argument = "No it isn't!"
        cheese = "No cheese"
        penguin_on_tv = {"location": "top of the television"}
        exploding_blueprint = None
        gumby = {"name": "Mr. Gumby", "hat": True}
        spam_eggs = ["spam", "eggs"]
        norwegian_blue = {"color": "blue", "resting": True}
        camelot = {"location": "England", "song": "We're knights of the round table"}
        grail_quest = ["seek", "find", "bring back"]
        shrubbery = {"height": "medium", "delivered": True}
        blackadder = "Not Monty Python, but funny"
        argument_counter = 1
        silly = True
        parrot_owner = "Mr. Praline"
        cheese_monger = "Henry Wensleydale"
        dead_parrot_sketch = {"parrot": dead_parrot, "owner": parrot_owner}

        # NOTE: there is only room to keep names for 32 local variables (configurable)

    # Return a summary dictionary for demonstration
    return spanish_inquisition


def main():
    """The actual code we want to debug"""
    print("Running debuggable code...")
    x = 78

    for _ in range(3):

        loco = inspect_local_variables()  

        scanner()  # Scan WiFi networks
        # fire_drill()
        mathematics()

        print("Done...")
        print("Final")

def scanner():
    try:
        import wifi_scan
    except ImportError:
        print("wifi_scan module not found. Skipping WiFi scan.")
        return
    wifi_scan.run_scan()  # Scan WiFi networks   


def mathematics():
    # Test data - set breakpoint here (using smaller numbers to avoid slow fibonacci)
    global foo
    numbers = [3, 4, 5]
    for i, num in enumerate(numbers):
        
        print(f"Calculating fibonacci({num})...")
        result = fibonacci(num)  # <-- SET BREAKPOINT HERE (line 26)
        foo += result  # Modify foo to see if it gets traced
        print(f"fibonacci({num}) = {result}")
        print(sys.implementation)

def fire_drill():
    from building import Building, Door, DoorController

    # Create building and door instances
    building_instance = Building()
    door = Door()
    controller = DoorController(door)

    print("Initial door status:", controller.get_status())
    print("Operating door...")
    controller.toggle()
    print("Door status after operation:", controller.get_status())
    print("Operating door again...")
    controller.toggle()
    print("Door status after operation:", controller.get_status())
    controller.close_door()  # Ensure door is closed
    controller.lock_door()   # Lock the door

    # Building is on fire
    building_instance.on_fire = True
    print("Building on fire, trying to open door...")

    if building_instance.on_fire:
        while door.is_locked:
            door.open()
            if not door.is_open:
                print("Help cannot exit the building ! The door is locked!!!")
                time.sleep(1)
            else:
                print("Door is now open, exiting the building.")
                break



if __name__ == "__main__":
    main()
    print("Test completed successfully!")
