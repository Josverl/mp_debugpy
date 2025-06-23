try:
    import neopixel
    from machine import Pin
    np = neopixel.NeoPixel(Pin(15), 10)
except ImportError:
    print("neopixel module not found. Skipping NeoPixel initialization.")
    np = None

_on_fire = False  # Global variable to track fire status

class Building:

    @property
    def on_fire(self):
        """Property to check if the building is on fire."""
        global _on_fire
        return _on_fire
    
    @on_fire.setter
    def on_fire(self, value):
        global _on_fire
        _on_fire = value
        if _on_fire and np:
            np.fill((255, 0, 0))  # Set NeoPixels to red if on fire
            np.write()  # Update NeoPixels



class Door:
    def __init__(self):
        self.is_open = False
        self._is_locked = False
    @property
    def is_locked(self):
        # if _on_fire:
        #     print("Opening door because building is on fire." )
        #     if np:
        #         np.fill((0, 255, 0))
        #         np.write()
        #         return False
        return self._is_locked 

    @is_locked.setter
    def is_locked(self, value:bool):
        self._is_locked = value

    def open(self):
        if self.is_locked:
            print("Critical error: Cannot open: Door is locked.")
        else:
            self.is_open = True
            print("Door is now open.")

    def close(self):
        self.is_open = False
        print("Door is now closed.")

    def lock(self):
        if self.is_open:
            print("Cannot lock: Door is open.")
        else:
            self.is_locked = True
            print("Door is now locked.")

    def unlock(self):
        self.is_locked = False
        print("Door is now unlocked.")


class DoorController:
    def __init__(self, door):
        self.door = door

    def toggle(self):
        if self.door.is_open:
            self.door.close()
        else:
            self.door.open()
    
    def open_door(self):
        """Open the door."""
        self.door.open()
    
    def close_door(self):
        """Close the door."""
        self.door.close()
    
    def lock_door(self):
        """Lock the door."""
        self.door.lock()
    
    def unlock_door(self):
        """Unlock the door."""
        self.door.unlock()
    
    def get_status(self):
        """Get the current door status."""
        return check_door_status(self.door)


def check_door_status(door):
    return "open" if door.is_open else "closed"

def operate_door(controller):
    controller.toggle()
    return check_door_status(controller.door)



